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

"""A primal dual active set strategy for control constraints.

"""

import fenics
import numpy as np

from .pdas_inner_solvers import InnerCG, InnerGradientDescent, InnerLBFGS, InnerNewton
from ..._exceptions import ConfigError
from ..._optimal_control import OptimizationAlgorithm



class PDAS(OptimizationAlgorithm):
	"""A primal-dual-active-set method.

	"""

	def __init__(self, optimization_problem):
		"""Initialize the primal-dual-active-set method

		Parameters
		----------
		optimization_problem : cashocs.OptimalControlProblem
			the OptimalControlProblem object
		"""

		OptimizationAlgorithm.__init__(self, optimization_problem)

		self.idx_active_upper_prev = [np.array([]) for j in range(self.optimization_problem.control_dim)]
		self.idx_active_lower_prev = [np.array([]) for j in range(self.optimization_problem.control_dim)]
		self.initialized = False
		self.mu = [fenics.Function(self.optimization_problem.control_spaces[j]) for j in range(self.optimization_problem.control_dim)]
		self.shift_mult = self.config.getfloat('AlgoPDAS', 'pdas_regularization_parameter')
		self.verbose = self.config.getboolean('Output', 'verbose', fallback=True)

		self.inner_pdas = self.config.get('AlgoPDAS', 'inner_pdas')
		if self.inner_pdas in ['gradient_descent', 'gd']:
			self.inner_solver = InnerGradientDescent(optimization_problem)
		elif self.inner_pdas in ['cg', 'conjugate_gradient', 'ncg', 'nonlinear_cg']:
			self.inner_solver = InnerCG(optimization_problem)
		elif self.inner_pdas in ['lbfgs', 'bfgs']:
			self.inner_solver = InnerLBFGS(optimization_problem)
		elif self.inner_pdas == 'newton':
			self.inner_solver = InnerNewton(optimization_problem)
		else:
			raise ConfigError('AlgoPDAS', 'inner_pdas', 'Not a valid input. Needs to be one of gradient_descent, lbfgs, cg, or newton.')



	def compute_active_inactive_sets(self):
		"""Computes the active and inactive sets.

		This implementation differs slightly from the one in
		cashocs._forms.ControlFormHandler as it is needed for the PDAS.

		Returns
		-------
		None
		"""

		self.idx_active_lower = [(self.mu[j].vector()[:] + self.shift_mult*(self.optimization_problem.controls[j].vector()[:] - self.optimization_problem.control_constraints[j][0].vector()[:]) < 0).nonzero()[0]
								 for j in range(self.optimization_problem.control_dim)]
		self.idx_active_upper = [(self.mu[j].vector()[:] + self.shift_mult*(self.optimization_problem.controls[j].vector()[:] - self.optimization_problem.control_constraints[j][1].vector()[:]) > 0).nonzero()[0]
								 for j in range(self.optimization_problem.state_dim)]

		self.idx_active = [np.concatenate((self.idx_active_lower[j], self.idx_active_upper[j])) for j in range(self.optimization_problem.control_dim)]
		[self.idx_active[j].sort() for j in range(self.optimization_problem.control_dim)]

		self.idx_inactive = [np.setdiff1d(np.arange(self.optimization_problem.control_spaces[j].dim()), self.idx_active[j]) for j in range(self.optimization_problem.control_dim)]

		if self.initialized:
			if all([np.array_equal(self.idx_active_upper[j], self.idx_active_upper_prev[j]) and np.array_equal(self.idx_active_lower[j], self.idx_active_lower_prev[j]) for j in range(self.optimization_problem.control_dim)]):
				self.converged = True

		self.idx_active_upper_prev = [self.idx_active_upper[j] for j in range(self.optimization_problem.control_dim)]
		self.idx_active_lower_prev = [self.idx_active_lower[j] for j in range(self.optimization_problem.control_dim)]
		self.initialized = True



	def run(self):
		"""Solves the optimization problem with the primal-dual-active-set method.

		Returns
		-------
		None
		"""
		self.iteration = 0

		### TODO: Check for feasible initialization

		self.compute_active_inactive_sets()

		self.state_problem.has_solution = False
		self.adjoint_problem.has_solution = False
		self.gradient_problem.has_solution = False
		self.objective_value = self.optimization_problem.reduced_cost_functional.evaluate()
		self.optimization_problem.state_problem.has_solution = True
		self.optimization_problem.gradient_problem.solve()
		norm_init = np.sqrt(self.optimization_problem._stationary_measure_squared())
		self.optimization_problem.adjoint_problem.has_solution = True

		self.print_results()
		
		while True:

			for j in range(len(self.controls)):
				self.controls[j].vector()[self.idx_active_lower[j]] = self.optimization_problem.control_constraints[j][0].vector()[self.idx_active_lower[j]]
				self.controls[j].vector()[self.idx_active_upper[j]] = self.optimization_problem.control_constraints[j][1].vector()[self.idx_active_upper[j]]


			self.inner_solver.run(self.idx_active)

			for j in range(len(self.controls)):
				self.mu[j].vector()[:] = -self.optimization_problem.gradients[j].vector()[:]
				self.mu[j].vector()[self.idx_inactive[j]] = 0.0

			

			self.objective_value = self.inner_solver.line_search.objective_step
			norm = np.sqrt(self.optimization_problem._stationary_measure_squared())

			self.relative_norm = norm / norm_init

			self.compute_active_inactive_sets()
			
			self.iteration += 1
			
			if self.converged:
				break
			
			if self.iteration >= self.maximum_iterations:
				self.converged_reason = -1
				break
			
			self.print_results()
			
			
