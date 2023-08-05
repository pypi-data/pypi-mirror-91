# VIPCCA
[![Documentation Status](https://readthedocs.org/projects/vipcca/badge/?version=latest)](https://vipcca.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/vipcca?color=blue)

Variational inference of probabilistic canonical correlation analysis

introduction......

............

### Create conda enviroment

```shell

$ conda create -n VIPCCA python=3.6
$ conda activate VIPCCA
```
For more information, see https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html

### Install VIPCCA from pypi

```shell

$ pip install VIPCCA
```

### Install VIPCCA from GitHub source code
```shell

$ git clone https://github.com/jhu99/VIPCCA.git
$ pip install -e ./VIPCCA/
```

**Note**: Please make sure that the `pip` is for python3.6. The current release depends on tensorflow with version 1.13.1. Install tenserfolow-gpu if gpu is avialable on the machine.


### Usage

https://vipcca.readthedocs.io/en/latest/

#### Quick Start

Download example data at http://141.211.10.196/result/test/papers/vipcca/data.tar.gz

```python
import VIPCCA as vp
from VIPCCA import preprocessing as pp
from VIPCCA import plotting as pl

# read single-cell data.
adata_b1 = pp.read_sc_data("./data/mixed_cell_lines/293t.h5ad", batch_name="293t")
adata_b2 = pp.read_sc_data("./data/mixed_cell_lines/jurkat.h5ad", batch_name="jurkat")
adata_b3 = pp.read_sc_data("./data/mixed_cell_lines/mixed.h5ad", batch_name="mixed")

# pp.preprocessing include filteration, log-TPM normalization, selection of highly variable genes.
adata_all= pp.preprocessing([adata_b1, adata_b2, adata_b3])

# VIPCCA will train the neural network on the provided datasets.
handle = vp.VIPCCA(
							adata_all,
							res_path='./results/CVAE_5/',
							split_by="_batch",
							epochs=100,
							lambda_regulizer=5,
							)

# transform user's single-cell data into shared low-dimensional space and recover gene expression.
adata_transform=handle.fit_transform()

# Visualization
pl.run_embedding(adata_transform, path='./results/CVAE_5/',method="umap")
pl.plotEmbedding(adata_transform, path='./results/CVAE_5/', method='umap', group_by="_batch",legend_loc="right margin")
pl.plotEmbedding(adata_transform, path='./results/CVAE_5/', method='umap', group_by="celltype",legend_loc="on data")
```


