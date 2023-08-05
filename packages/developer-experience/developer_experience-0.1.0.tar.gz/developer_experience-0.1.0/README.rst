Python Developer Experience (PyDX)
##################################

A knowledge base of things that make the Python developer experience pythonic.


Dependencies
------------
Integrate pyenv_ with pipenv_ to install the Pipfile pinned version of Python
or use  miniconda_ to install the pinned version of Python then activate the
conda environment before running pipenv install so that pipenv finds the correct
version of Python. Alternatively, use Poetry_ for managing both dependencies and
environments.

.. code-block:: bash

    conda create python=3.8 --name pydx
    conda activate pydx
    pip install -r requirements/assumed.txt
    pipenv install --dev -r requirements/development.txt
    pipenv shell


.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _pipenv: https://github.com/pypa/pipenv
.. _poetry: https://python-poetry.org/
.. _pyenv: https://github.com/pyenv/pyenv
