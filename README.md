# LAtools GUI

I've set up a framework for an installable Python package with documentation.

## Python Package
All code should go inside the `latools_gui` subdirectory. A python package is any directory that contains an `__init__.py`, which is run when you import the package.

### Installation
Installation is via `setuptools`, and all relevant info/options is in [setup.py](setup.py).

You can make the package accessible to Python using:

```bash
python setup.py develop
```

Using `develop` changes in the code automatically propagate through to the installed version (`install` would create a copy of the current state of the code in your Python site-packages, whereas `develop` just creates a symbolic link to the code location.)

## Documentation

We're using [sphinx](http://www.sphinx-doc.org/en/master/). General structure is:

```bash
docs/source
    |-index.rst  # main page, which sphinx evaluates to build the docs
    |-conf.py  # sphinx configuration
```

You can create subdirectories and new `.rst` files with the within source directory, and populate them with documentation written in [reStructuredText](http://www.sphinx-doc.org/en/master/rest.html) format.

Do build the docs html, run:

```bash
cd docs
make html
```

... or whatever windows equivalent works with the `make.bat` file ...

Whenever you create a new file in the documentation, you have to enter it into the `index.rst` file, or it won't be built. For example:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   my_new_file.rst
   my_new_directory/my_new_file.rst
```

Handily, sphinx warns you if there are `.rst` files in the source directory that *aren't* included in the table of contents.

### Autodoc

One of the best features of sphinx is its ability to autogenerate documentation based on docstrings. This means you **must have good docstring discipline**!

1. Whenever you create a function/class, create a docstring. No excuses.
2. Write them in a consistent format that sphinx can understand, for example the [numpy format](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)):

```python
def f(x, y)::
    """
    Adds x to y.

    Can put a longer description here, if you want.

    Parameters
    ----------
    x : float
        The value of x.
    y : float
        The value of y.

    Returns
    -------
    Sum of x and y : float

    Examples
    --------
    f(3.5, 8)
    > 11.5
    """
    return x + y
```

For autodoc to work, you need to [set it up](http://www.sphinx-doc.org/en/stable/ext/autodoc.html) - probably the best way to do this is create a separate `.rst` file in docs/source that calls autodoc, and then add that to the `index.rst` file.