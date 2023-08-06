# paropy

Python package to process data from PARODY-JA4.3 dynamo simulations.

## Getting Started

### Prerequisites
- [Python](https://www.python.org/)

### Installing
Conda:
```
conda install -c jnywong paropy
```

Pip:
```
pip install paropy
```

Git:

Find the Git repo [here](https://github.com/jnywong/nondim-slurry).

### Example script: diagnostics

Sample scripts can be found within the module package `paropy/scripts`.

1. Open `paropy/scripts/diagnostics.py`

2. Set path to simulation data by setting

```
run_ID = <run_ID> # PARODY simulation tag
directory = <path_to_data>
```

3. Run `paropy/scripts/diagnostics.py`

4. Admire the output:

![](https://raw.githubusercontent.com/jnywong/paropy/master/docs/diag1_test.png)

![](https://raw.githubusercontent.com/jnywong/paropy/master/docs/diag2_test.png)

### Example script: meridional snapshots

1. Open `paropy/scripts/meridional_snapshot.py`

2. Set path to simulation data by setting

```
run_ID = <run_ID> # PARODY simulation tag
directory = <path_to_data>
```

3. Specify timestamp of snapshot by setting `timestamp`

4. Run `paropy/scripts/meridional_snapshot.py`

5. Admire the output:

![](https://raw.githubusercontent.com/jnywong/paropy/master/docs/merid_test.png)

### Example script: surface snapshots

1. Open `paropy/scripts/surface_snapshot.py`

2. Set path to simulation data by setting

```
run_ID = <run_ID> # PARODY simulation tag
directory = <path_to_data>
```

3. Specify timestamp of snapshot by setting `timestamp`

4. Run `paropy/scripts/surface_snapshot.py`

5. Admire the output:

![](https://raw.githubusercontent.com/jnywong/paropy/master/docs/surface_test.png)

## Links

* [PyPI](https://pypi.org/project/paropy/)
* [Anaconda Cloud](https://anaconda.org/jnywong/paropy)

## Authors

* [**Jenny Wong**](https://jnywong.github.io/) - *Institut de Physique du Globe de Paris - Institut des Sciences de la Terre*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Del Duca Foundation
* ERC SEIC

:tada:
