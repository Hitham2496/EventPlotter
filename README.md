# EventPlotter
![Tests](https://github.com/Hitham2496/EventPlotter/actions/workflows/tests.yml/badge.svg)

`EventPlotter` - Comprehensive plotting and analysis of events in high energy physics.

## Installation

`EventPlotter` is a python3 package designed for robust and efficient analysis of events
in high energy physics simulations of particle collisions.

This allows for the swift and comprehensive analysis of the **complex data structures**
which are events in HEP, **simplifying the data** and allowing for a wide range of
studies to be performed on simulated events.

The required packages to install `EventPlotter` may be found in `requirements.txt`.

After cloning the repository, there should be a directory named `EventPlotter` present
in your current working directory, navigate to this directory.

The package can then be installed by:
```bash
python3 setup.py install --user 
```
or, as a package to your local environment with `pip`:
```bash
pip install -e . --user
```
Sphinx documentation can be produced with:
```bash
cd docs
make [builder]
```
where [builder] can take any sphinx-compatible documentation builder format (e.g. html,
latex ...).

This will build documentation in `EventPlotter/docs/_build`.

## Usage

The package can be imported into python scripts and notebooks as normal e.g.
```python
#!/usr/bin/env python3
import EventPlotter as ep
```
Consult the API reference in the documentation for detailed listings of the package
functionality available.

Several examples are provided in `EventPlotter/examples` highlighting different methods
for using the package, the companion document for these is the `Usage and Examples`
section of the documentation.

## Testing

Unit tests are provided with the package, and can be executed with
```python
$ python -m pytest
```

## Development Philosophy

The entire commit history and branches created to address issues are both retained for
full transparency and ease of review to e.g. isolate issues that arise.

Issues are logged under the `Issues` tab and addressed with each a dedicated branch
and pull request.

Branches for feature development are denoted with the prefix `dev-` while those addressing
bugs start with the prefix `bug-`

The development is guided by unit-testing at all stages to streamline the production of
high quality code.
