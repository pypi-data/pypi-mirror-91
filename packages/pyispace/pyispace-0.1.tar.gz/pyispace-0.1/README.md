# PyISpace

_Python Instance Space Analysis Toolkit_

<!--![picture](docs/img/circle-fs.png)-->

## Getting Started

This is the Python version of the [Instance Space Analysis](https://github.com/andremun/InstanceSpace) (ISA) toolkit, originally written in Matlab code. The ISA toolkit was developed as part of the project [Matilda](https://matilda.unimelb.edu.au/matilda/), in the university of Melbourne.

PyISpace is a Python package that contains a subset of the tools present in the original Matlab code repository. It is not our intention to add new features to the toolkit. For a complete experience of all tools, we recommend the original code, or the [web version](https://matilda.unimelb.edu.au/matilda/).

### Requirements
Python 3.7 or newer.

### Installation

```
git clone https://gitlab.com/ita-ml/pyispace.git
cd pyispace/
pip install -e .
```


### Usage

1. Command Line Interface

Inside the folder containing the required files ``options.json`` and ``metadata.csv``, run  
```
python -m pyispace
```
For more information about these files, please refer to the original repository instructions.

2. Python package

```
from pyispace import train_is
model = train_is(metadata, opts)
```
