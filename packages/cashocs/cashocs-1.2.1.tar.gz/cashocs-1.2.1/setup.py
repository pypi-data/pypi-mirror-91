import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cashocs",
    version="1.2.1",
    author="Sebastian Blauth",
    author_email="sebastian.blauth@itwm.fraunhofer.de",
    description="Computational Adjoint-Based Shape Optimization and Optimal Control Software",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/sblauth/cashocs",
    project_urls={'Source' : 'https://github.com/sblauth/cashocs',
                  'Documentation' : 'https://cashocs.readthedocs.io/en/latest/index.html',
                  'Tutorial' : 'https://cashocs.readthedocs.io/en/latest/tutorial_index.html',
                  'Tracker' : 'https://github.com/sblauth/cashocs/issues'
                  },
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords="Computational Adjoint-Based Shape Optimization and Optimal Control Software",
    install_requires=[
		'pytest>=6.0.0',
        'meshio>=4.1.0',
		'deprecated>=1.2.10',
        'matplotlib'
    ],
    entry_points={
        "console_scripts" : [
            "cashocs-convert = cashocs._cli:convert"
        ]
    },
    python_requires='>=3.6',
)
