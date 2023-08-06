# pyhard

__Instance Hardness Python package__.

## Getting Started

Python 3.7 is required. Matlab is also required in order to run [matilda](https://matilda.unimelb.edu.au/matilda/). As far as we know, only recent versions of Matlab offer an engine for Python 3. Namely, we have tested only version R2020a.

### Installation
1. __Clone repository__
```
git clone https://gitlab.com/ita-ml/instance-hardness.git
```

2. __Install package via pip__
```
cd instance-hardness/
pip install -e .
```

3. __Install Matlab engine for Python__  
Refer to this [link](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html), which contains detailed instructions.

### Usage

In the command line (terminal):

```
cd your/path/instance-hardness
python pyhard
```

It should generate the `metadata.csv` file and run the matilda software.

### Configuration

See the file `config.yaml` in `/instance-hardness/conf/`. It contains options for file paths, measures to be calculated, which classifiers to use and their parametrization.
