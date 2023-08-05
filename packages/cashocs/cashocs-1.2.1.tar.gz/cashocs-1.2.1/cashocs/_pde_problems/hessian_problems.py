# Copyright (C) 2020-2021 Sebastian Blauth
#
# This file is part of CASHOCS.
#
# CASHOCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CASHOCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CASHOCS.  If not, see <https://www.gnu.org/licenses/>.

"""Abstract implementation of the Hessian problem.

This uses Krylov subspace methods to iteratively solve
the "Hessian problems" occurring in the truncated Newton
method.
"""

import fenics
import numpy as np
from petsc4py import PETSc

from .._loggers import debug
from .._exceptions import ConfigError, NotConvergedError, CashocsException
from ..utils import _assemble_petsc_system, _setup_petsc_options, _solve_linear_problem



class BaseHessianProblem:
	"""Base class for derived Hessian problems.

	"""

	def __init__(self, form_handler, gradient_problem):
		"""Initializes self.

		Parameters
		----------
		form_handler : cashocs._forms.ControlFormHandler
			The FormHandler object for the optimization problem.
		gradient_problem : cashocs._pde_problems.GradientProblem
			The GradientProblem object (this is needed for the computation
			of the Hessian).
		"""

		self.form_handler = form_handler
		self.gradient_problem = gradient_problem

		self.config = self.form_handler.config
		self.gradients = self.gradient_problem.gradients

		self.inner_newton = self.config.get('AlgoTNM', 'inner_newton', fallback='cr')
		self.max_it_inner_newton = self.config.getint('AlgoTNM', 'max_it_inner_newton', fallback=50)
		# TODO: Add absolute tolerance, too
		self.inner_newton_tolerance = self.config.getfloat('AlgoTNM', 'inner_newton_tolerance', fallback=1e-15)

		self.test_directions = self.form_handler.test_directions
		self.residual = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.delta_control = [fenics.Function(V) for V in self.form_handler.control_spaces]

		self.state_dim = self.form_handler.state_dim
		self.control_dim = self.form_handler.control_dim

		self.temp1 = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.temp2 = [fenics.Function(V) for V in self.form_handler.control_spaces]

		self.p = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.p_prev = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.p_pprev = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.s = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.s_prev = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.s_pprev = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.q = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.q_prev = [fenics.Function(V) for V in self.form_handler.control_spaces]

		self.hessian_actions = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.inactive_part = [fenics.Function(V) for V in self.form_handler.control_spaces]
		self.active_part = [fenics.Function(V) for V in self.form_handler.control_spaces]

		self.controls = self.form_handler.controls

		self.rtol = self.config.getfloat('StateSystem', 'picard_rtol', fallback=1e-10)
		self.atol = self.config.getfloat('StateSystem', 'picard_atol', fallback=1e-12)
		self.maxiter = self.config.getint('StateSystem', 'picard_iter', fallback=50)
		self.picard_verbose = self.config.getboolean('StateSystem', 'picard_verbose', fallback=False)

		self.no_sensitivity_solves = 0
		self.state_ksps = [PETSc.KSP().create() for i in range(self.form_handler.state_dim)]
		_setup_petsc_options(self.state_ksps, self.form_handler.state_ksp_options)
		self.adjoint_ksps = [PETSc.KSP().create() for i in range(self.form_handler.state_dim)]
		_setup_petsc_options(self.adjoint_ksps, self.form_handler.adjoint_ksp_options)

		# Initialize the PETSc Krylov solver for the Riesz projection problems
		self.ksps = [PETSc.KSP().create() for i in range(self.control_dim)]

		option = [
			['ksp_type', 'cg'],
			['pc_type', 'hypre'],
			['pc_hypre_type', 'boomeramg'],
			['pc_hypre_boomeramg_strong_threshold', 0.7],
			['ksp_rtol', 1e-16],
			['ksp_atol', 1e-50],
			['ksp_max_it', 100]
		]
		self.riesz_ksp_options = []
		for i in range(self.control_dim):
			self.riesz_ksp_options.append(option)

		_setup_petsc_options(self.ksps, self.riesz_ksp_options)
		for i, ksp in enumerate(self.ksps):
			ksp.setOperators(self.form_handler.riesz_projection_matrices[i])



	def hessian_application(self, h, out):
		r"""Computes the application of the Hessian to some element

		This is needed in the truncated Newton method where we solve the system

		.. math:: J''(u) [\Delta u] = - J'(u)

		via iterative methods (conjugate gradient or conjugate residual method)

		Parameters
		----------
		h : list[dolfin.function.function.Function]
			A function to which we want to apply the Hessian to.
		out : list[dolfin.function.function.Function]
			A list of functions into which the result is saved.

		Returns
		-------
		None
		"""

		for i in range(self.control_dim):
			self.test_directions[i].vector()[:] = h[i].vector()[:]

		self.states_prime = self.form_handler.states_prime
		self.adjoints_prime = self.form_handler.adjoints_prime
		self.bcs_list_ad = self.form_handler.bcs_list_ad

		if not self.form_handler.state_is_picard or self.form_handler.state_dim == 1:

			for i in range(self.state_dim):
				A, b = _assemble_petsc_system(self.form_handler.sensitivity_eqs_lhs[i], self.form_handler.sensitivity_eqs_rhs[i], self.bcs_list_ad[i])
				_solve_linear_problem(self.state_ksps[i], A, b, self.states_prime[i].vector().vec(), self.form_handler.state_ksp_options[i])
				self.states_prime[i].vector().apply('')

			for i in range(self.state_dim):
				A, b = _assemble_petsc_system(self.form_handler.adjoint_sensitivity_eqs_lhs[-1 - i], self.form_handler.w_1[-1 - i], self.bcs_list_ad[-1 - i])
				_solve_linear_problem(self.adjoint_ksps[-1 - i], A, b, self.adjoints_prime[-1 - i].vector().vec(), self.form_handler.adjoint_ksp_options[-1 - i])
				self.adjoints_prime[-1 - i].vector().apply('')

		else:
			for i in range(self.maxiter + 1):
				res = 0.0
				for j in range(self.form_handler.state_dim):
					res_j = fenics.assemble(self.form_handler.sensitivity_eqs_picard[j])
					[bc.apply(res_j) for bc in self.form_handler.bcs_list_ad[j]]
					res += pow(res_j.norm('l2'), 2)

				if res==0:
					break

				res = np.sqrt(res)

				if i==0:
					res_0 = res

				if self.picard_verbose:
					print('Picard Sensitivity 1 Iteration ' + str(i) + ': ||res|| (abs): ' + format(res, '.3e') + '   ||res|| (rel): ' + format(res/res_0, '.3e'))

				if res/res_0 < self.rtol or res < self.atol:
					break

				if i==self.maxiter:
					raise NotConvergedError('Picard iteration for the computation of the state sensitivity', 'Maximum number of iterations were exceeded.')

				for j in range(self.form_handler.state_dim):
					A, b = _assemble_petsc_system(self.form_handler.sensitivity_eqs_lhs[j], self.form_handler.sensitivity_eqs_rhs[j], self.bcs_list_ad[j])
					_solve_linear_problem(self.state_ksps[j], A, b, self.states_prime[j].vector().vec(), self.form_handler.state_ksp_options[j])
					self.states_prime[j].vector().apply('')

			if self.picard_verbose:
				print('')

			for i in range(self.maxiter + 1):
				res = 0.0
				for j in range(self.form_handler.state_dim):
					res_j = fenics.assemble(self.form_handler.adjoint_sensitivity_eqs_picard[j])
					[bc.apply(res_j) for bc in self.form_handler.bcs_list_ad[j]]
					res += pow(res_j.norm('l2'), 2)

				if res==0:
					break

				res = np.sqrt(res)

				if i==0:
					res_0 = res

				if self.picard_verbose:
					print('Picard Sensitivity 2 Iteration ' + str(i) + ': ||res|| (abs): ' + format(res, '.3e') + '   ||res|| (rel): ' + format(res/res_0, '.3e'))

				if res/res_0 < self.rtol or res < self.atol:
					break

				if i==self.maxiter:
					raise NotConvergedError('Picard iteration for the computation of the adjoint sensitivity', 'Maximum number of iterations were exceeded.')

				for j in range(self.form_handler.state_dim):
					A, b = _assemble_petsc_system(self.form_handler.adjoint_sensitivity_eqs_lhs[-1 - j], self.form_handler.w_1[-1 - j], self.bcs_list_ad[-1 - j])
					_solve_linear_problem(self.adjoint_ksps[-1 - j], A, b, self.adjoints_prime[-1 - j].vector().vec(), self.form_handler.adjoint_ksp_options[-1 - j])
					self.adjoints_prime[-1 - j].vector().apply('')

			if self.picard_verbose:
				print('')

		for i in range(self.control_dim):
			b = fenics.as_backend_type(fenics.assemble(self.form_handler.hessian_rhs[i])).vec()

			_solve_linear_problem(self.ksps[i], b=b, x=out[i].vector().vec(), ksp_options=self.riesz_ksp_options[i])
			out[i].vector().apply('')

		self.no_sensitivity_solves += 2



	def newton_solve(self, idx_active=None):

		self.gradient_problem.solve()
		self.form_handler.compute_active_sets()

		for j in range(self.control_dim):
			self.delta_control[j].vector()[:] = 0.0

		if self.inner_newton == 'cg':
			self.cg(idx_active)
		elif self.inner_newton == 'cr':
			self.cr(idx_active)
		else:
			raise ConfigError('AlgoTNM', 'inner_newton', 'Not a valid choice. Needs to be either \'cg\' or \'cr\'.')

		return self.delta_control



	def cg(self, idx_active=None):
		pass



	def cr(self, idx_active=None):
		pass





class HessianProblem(BaseHessianProblem):
	"""PDE Problem used to solve the (reduced) Hessian problem.

	"""

	def __init__(self, form_handler, gradient_problem):
		"""Initializes self.

		Parameters
		----------
		form_handler : cashocs._forms.ControlFormHandler
			The FormHandler object for the optimization problem.
		gradient_problem : cashocs._pde_problems.GradientProblem
			The GradientProblem object (this is needed for the computation
			of the Hessian).
		"""

		BaseHessianProblem.__init__(self, form_handler, gradient_problem)



	def reduced_hessian_application(self, h, out):

		for j in range(self.control_dim):
			out[j].vector()[:] = 0.0

		self.form_handler.restrict_to_inactive_set(h, self.inactive_part)
		self.hessian_application(self.inactive_part, self.hessian_actions)
		self.form_handler.restrict_to_inactive_set(self.hessian_actions, self.inactive_part)
		self.form_handler.restrict_to_active_set(h, self.active_part)

		for j in range(self.control_dim):
			out[j].vector()[:] = self.active_part[j].vector()[:] + self.inactive_part[j].vector()[:]



	def newton_solve(self, idx_active=None):

		if idx_active is not None:
			raise CashocsException('Must not pass idx_active to HessianProblem.')

		return BaseHessianProblem.newton_solve(self)



	def cg(self, idx_active=None):

		for j in range(self.control_dim):
			self.residual[j].vector()[:] = -self.gradients[j].vector()[:]
			self.p[j].vector()[:] = self.residual[j].vector()[:]

		self.rsold = self.form_handler.scalar_product(self.residual, self.residual)
		self.eps_0 = np.sqrt(self.rsold)

		for i in range(self.max_it_inner_newton):

			self.reduced_hessian_application(self.p, self.q)

			self.form_handler.restrict_to_active_set(self.p, self.temp1)
			sp_val1 = self.form_handler.scalar_product(self.temp1, self.temp1)

			self.form_handler.restrict_to_inactive_set(self.p, self.temp1)
			self.form_handler.restrict_to_inactive_set(self.q, self.temp2)
			sp_val2 = self.form_handler.scalar_product(self.temp1, self.temp2)
			sp_val = sp_val1 + sp_val2
			self.alpha = self.rsold / sp_val

			for j in range(self.control_dim):
				self.delta_control[j].vector()[:] += self.alpha * self.p[j].vector()[:]
				self.residual[j].vector()[:] -= self.alpha * self.q[j].vector()[:]

			self.rsnew = self.form_handler.scalar_product(self.residual, self.residual)
			self.eps = np.sqrt(self.rsnew)
			debug('Residual of the CG method: ' + format(self.eps / self.eps_0, '.3e') + ' (relative)')
			if self.eps / self.eps_0 < self.inner_newton_tolerance:
				break

			self.beta = self.rsnew / self.rsold

			for j in range(self.control_dim):
				self.p[j].vector()[:] = self.residual[j].vector()[:] + self.beta * self.p[j].vector()[:]

			self.rsold = self.rsnew



	def cr(self, idx_active=None):

		for j in range(self.control_dim):
			self.residual[j].vector()[:] = -self.gradients[j].vector()[:]
			self.p[j].vector()[:] = self.residual[j].vector()[:]

		self.eps_0 = np.sqrt(self.form_handler.scalar_product(self.residual, self.residual))

		self.reduced_hessian_application(self.residual, self.s)

		for j in range(self.control_dim):
			self.q[j].vector()[:] = self.s[j].vector()[:]

		self.form_handler.restrict_to_active_set(self.residual, self.temp1)
		self.form_handler.restrict_to_active_set(self.s, self.temp2)
		sp_val1 = self.form_handler.scalar_product(self.temp1, self.temp2)
		self.form_handler.restrict_to_inactive_set(self.residual, self.temp1)
		self.form_handler.restrict_to_inactive_set(self.s, self.temp2)
		sp_val2 = self.form_handler.scalar_product(self.temp1, self.temp2)

		self.rAr = sp_val1 + sp_val2

		for i in range(self.max_it_inner_newton):

			self.form_handler.restrict_to_active_set(self.q, self.temp1)
			self.form_handler.restrict_to_inactive_set(self.q, self.temp2)
			denom1 = self.form_handler.scalar_product(self.temp1, self.temp1)
			denom2 = self.form_handler.scalar_product(self.temp2, self.temp2)
			denominator = denom1 + denom2

			self.alpha = self.rAr / denominator

			for j in range(self.control_dim):
				self.delta_control[j].vector()[:] += self.alpha * self.p[j].vector()[:]
				self.residual[j].vector()[:] -= self.alpha * self.q[j].vector()[:]

			self.eps = np.sqrt(self.form_handler.scalar_product(self.residual, self.residual))
			debug('Residual of the CR method: ' + format(self.eps / self.eps_0, '.3e') + ' (relative)')
			if self.eps / self.eps_0 < self.inner_newton_tolerance or i == self.max_it_inner_newton - 1:
				break

			self.reduced_hessian_application(self.residual, self.s)

			self.form_handler.restrict_to_active_set(self.residual, self.temp1)
			self.form_handler.restrict_to_active_set(self.s, self.temp2)
			sp_val1 = self.form_handler.scalar_product(self.temp1, self.temp2)
			self.form_handler.restrict_to_inactive_set(self.residual, self.temp1)
			self.form_handler.restrict_to_inactive_set(self.s, self.temp2)
			sp_val2 = self.form_handler.scalar_product(self.temp1, self.temp2)

			self.rAr_new = sp_val1 + sp_val2
			self.beta = self.rAr_new / self.rAr

			for j in range(self.control_dim):
				self.p[j].vector()[:] = self.residual[j].vector()[:] + self.beta * self.p[j].vector()[:]
				self.q[j].vector()[:] = self.s[j].vector()[:] + self.beta * self.q[j].vector()[:]

			self.rAr = self.rAr_new





class UnconstrainedHessianProblem(BaseHessianProblem):
	"""Hessian Problem without control constraints for the inner solver in PDAS.

	"""

	def __init__(self, form_handler, gradient_problem):
		"""Initializes self.

		Parameters
		----------
		form_handler : cashocs._forms.ControlFormHandler
			The FormHandler object for the optimization problem.
		gradient_problem : cashocs._pde_problems.GradientProblem
			The GradientProblem object (this is needed for the computation
			of the Hessian).
		"""

		BaseHessianProblem.__init__(self, form_handler, gradient_problem)

		self.reduced_gradient = [fenics.Function(self.form_handler.control_spaces[j]) for j in range(len(self.gradients))]
		self.temp = [fenics.Function(V) for V in self.form_handler.control_spaces]



	def reduced_hessian_application(self, h, out, idx_active):

		for j in range(self.control_dim):
			self.temp[j].vector()[:] = h[j].vector()[:]
			self.temp[j].vector()[idx_active[j]] = 0.0

		self.hessian_application(self.temp, out)

		for j in range(self.control_dim):
			out[j].vector()[idx_active[j]] = 0.0



	def newton_solve(self, idx_active=None):

		if idx_active is None:
			raise CashocsException('Need to pass idx_active to UnconstrainedHessianProblem.')

		self.gradient_problem.solve()

		for j in range(self.control_dim):
			self.reduced_gradient[j].vector()[:] = self.gradients[j].vector()[:]
			self.reduced_gradient[j].vector()[idx_active[j]] = 0.0

		return BaseHessianProblem.newton_solve(self, idx_active)



	def cg(self, idx_active=None):

		for j in range(self.control_dim):
			self.residual[j].vector()[:] = -self.reduced_gradient[j].vector()[:]
			self.p[j].vector()[:] = self.residual[j].vector()[:]

		self.rsold = self.form_handler.scalar_product(self.residual, self.residual)
		self.eps_0 = np.sqrt(self.rsold)

		for i in range(self.max_it_inner_newton):
			self.reduced_hessian_application(self.p, self.q, idx_active)

			self.alpha = self.rsold / self.form_handler.scalar_product(self.p, self.q)
			for j in range(self.control_dim):
				self.delta_control[j].vector()[:] += self.alpha * self.p[j].vector()[:]
				self.residual[j].vector()[:] -= self.alpha * self.q[j].vector()[:]

			self.rsnew = self.form_handler.scalar_product(self.residual, self.residual)
			self.eps = np.sqrt(self.rsnew)
			debug('Residual of the CG method: ' + format(self.eps / self.eps_0, '.3e') + ' (relative)')
			if self.eps/self.eps_0 < self.inner_newton_tolerance:
				break

			self.beta = self.rsnew / self.rsold

			for j in range(self.control_dim):
				self.p[j].vector()[:] = self.residual[j].vector()[:] + self.beta * self.p[j].vector()[:]

			self.rsold = self.rsnew



	def cr(self, idx_active=None):

		for j in range(self.control_dim):
			self.residual[j].vector()[:] = -self.reduced_gradient[j].vector()[:]
			self.p[j].vector()[:] = self.residual[j].vector()[:]

		self.eps_0 = np.sqrt(self.form_handler.scalar_product(self.residual, self.residual))

		self.reduced_hessian_application(self.residual, self.s, idx_active)

		for j in range(self.control_dim):
			self.q[j].vector()[:] = self.s[j].vector()[:]

		self.rAr = self.form_handler.scalar_product(self.residual, self.s)

		for i in range(self.max_it_inner_newton):
			self.alpha = self.rAr / self.form_handler.scalar_product(self.q, self.q)

			for j in range(self.control_dim):
				self.delta_control[j].vector()[:] += self.alpha * self.p[j].vector()[:]
				self.residual[j].vector()[:] -= self.alpha * self.q[j].vector()[:]

			self.eps = np.sqrt(self.form_handler.scalar_product(self.residual, self.residual))
			debug('Residual of the CR method: ' + format(self.eps / self.eps_0, '.3e') + ' (relative)')
			if self.eps/self.eps_0 < self.inner_newton_tolerance or i==self.max_it_inner_newton - 1:
				break

			self.reduced_hessian_application(self.residual, self.s, idx_active)

			self.rAr_new = self.form_handler.scalar_product(self.residual, self.s)
			self.beta = self.rAr_new / self.rAr

			for j in range(self.control_dim):
				self.p[j].vector()[:] = self.residual[j].vector()[:] + self.beta * self.p[j].vector()[:]
				self.q[j].vector()[:] = self.s[j].vector()[:] + self.beta * self.q[j].vector()[:]

			self.rAr = self.rAr_new
