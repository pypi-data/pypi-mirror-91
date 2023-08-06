# ![QuCumber](https://raw.githubusercontent.com/PIQuIL/QuCumber/master/docs/_static/img/QuCumber_full.png)
[![PyPI Version](https://img.shields.io/pypi/v/qucumber)](https://pypi.org/project/qucumber)
[![Python Versions](https://img.shields.io/pypi/pyversions/qucumber)](https://pypi.org/project/qucumber)
[![Documentation Status](https://readthedocs.org/projects/qucumber/badge/?version=stable)](https://qucumber.readthedocs.io/en/stable/?badge=stable)
[![Build Status (Travis)](https://travis-ci.com/PIQuIL/QuCumber.svg?branch=master)](https://travis-ci.com/PIQuIL/QuCumber)
[![Build Status (AppVeyor)](https://ci.appveyor.com/api/projects/status/lqdrc8qp94w4b9kf/branch/master?svg=true)](https://ci.appveyor.com/project/emerali/qucumber/branch/master)
[![codecov](https://codecov.io/gh/PIQuIL/QuCumber/branch/master/graph/badge.svg)](https://codecov.io/gh/PIQuIL/QuCumber)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![arXiv](https://img.shields.io/badge/arXiv-1812.09329-B31B1B.svg)](https://arxiv.org/abs/1812.09329)
[![scipost](https://img.shields.io/badge/SciPost-7.1.009-blue.svg)](https://scipost.org/SciPostPhys.7.1.009)

## A Quantum Calculator Used for Many-body Eigenstate Reconstruction

QuCumber is a program that reconstructs an unknown quantum wavefunction
from a set of measurements. The measurements should consist of binary counts;
for example, the occupation of an atomic orbital, or angular momentum eigenvalue of
a qubit. These measurements form a training set, which is used to train a
stochastic neural network called a Restricted Boltzmann Machine. Once trained, the
neural network is a reconstructed representation of the unknown wavefunction
underlying the measurement data. It can be used for generative modelling, i.e.
producing new instances of measurements, and to calculate estimators not
contained in the original data set.

QuCumber is developed by the Perimeter Institute Quantum Intelligence Lab (PIQuIL).

## Features

QuCumber implements unsupervised generative modelling with a two-layer RBM.
Each layer is a number of binary stochastic variables (with values 0 or 1). The
size of the visible layer corresponds to the input data, i.e. the number of
qubits. The size of the hidden layer is a hyperparameter, varied to systematically control
representation error.

Currently, quantum state reconstruction/tomography can be performed on both pure and mixed states.
Pure state reconstruction can be further broken down into positive or complex wavefunction reconstruction.
In the case of a positive wavefunction, data is only required in one basis. For complex wavefunctions as
well as mixed states, measurement data in additional bases will be required to train the state.

## Documentation

Documentation can be found [here](https://qucumber.readthedocs.io/en/stable/).

See "QuCumber: wavefunction reconstruction with neural networks" https://scipost.org/SciPostPhys.7.1.009

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes.

### Installing

If you're on Windows, you will have to install PyTorch manually; instructions
can be found on their website: [pytorch.org](https://pytorch.org).

You can install the latest stable version of QuCumber, along with its dependencies,
using [`pip`](https://pip.pypa.io/en/stable/quickstart/):

```bash
pip install qucumber
```

If, for some reason, `pip` fails to install PyTorch, you can find installation
instructions on their website. Once that's done you should be able to install
QuCumber through `pip` as above.

QuCumber supports Python 3.6 and newer stable versions.

### Installing the bleeding-edge version

If you'd like to install the most upto date, but potentially unstable version,
you can clone the repository's master branch and then build from source like so:

```bash
git clone git@github.com:PIQuIL/QuCumber.git
cd ./QuCumber
python setup.py install
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute
to the project, and the process for submitting pull requests to us.

## License

QuCumber is licensed under the Apache License Version 2.0, this includes almost
all files in this repo. However, some miscellaneous files may be licensed
differently. See [LICENSE](LICENSE) for more details.

## Citation

```latex
@Article{10.21468/SciPostPhys.7.1.009,
    title={{QuCumber: wavefunction reconstruction with neural networks}},
    author={Matthew J. S. Beach and Isaac De Vlugt and Anna Golubeva and Patrick Huembeli and Bohdan Kulchytskyy and Xiuzhe Luo and Roger G. Melko and Ejaaz Merali and Giacomo Torlai},
    journal={SciPost Phys.},
    volume={7},
    issue={1},
    pages={9},
    year={2019},
    publisher={SciPost},
    doi={10.21468/SciPostPhys.7.1.009},
    url={https://scipost.org/10.21468/SciPostPhys.7.1.009},
}
```

## Acknowledgments

- We thank M. Albergo, G. Carleo, J. Carrasquilla, D. Sehayek, and
  L. Hayward Sierens for many helpful discussions.

- We thank the [Perimeter Institute](https://www.perimeterinstitute.ca) for the
  continuing support of PIQuIL.

- Thanks to Nick Mercer for creating our awesome logo. You can check out more of
  Nick's work by visiting [his portfolio](https://www.behance.net/nickdmercec607)
  on Behance!
