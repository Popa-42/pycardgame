************
Installation
************

You can install PyCardGame using pip. Open your terminal or command prompt and
run the following command:

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ pycardgame

This command will install the latest version of PyCardGame from the Test PyPI
repository. If you want to install a specific version, you can specify it like
this:

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ pycardgame==0.1.8

If you want to include the package in a ``requirements.txt`` file, you can do so
by adding the following lines:

.. code-block:: text

   -i https://test.pypi.org/simple/
   pycardgame~=0.1.8

Installing from Source
======================

If you prefer to install PyCardGame from source, you can clone the repository
and install it using pip:

.. code-block:: bash

   git clone https://github.com/Popa-42/pycardgame.git
   cd pycardgame
   python -m pip install -e .

Troubleshooting
===============

Common issues
-------------

#. **ImportError: No module named 'pycardgame'**

   - Make sure you've activated your virtual environment (if using one)
   - Try reinstalling the package
   - Check if the installation was successful by running ``pip list``

#. **Version compatibility**

   - Ensure you're using Python 3.8 or higher
   - Check the package version with ``pip show pycardgame``

#. **Permission Issues**

   - On Unix-like systems, you might need to use ``sudo`` for system-wide installation
   - Consider using a virtual environment to avoid permission issues

#. **Network Issues**

   - Ensure you have a stable internet connection
   - Check if the Test PyPI repository is accessible

Getting Help
------------

If you encounter any issues during installation:

#. Check the `GitHub Issues <https://github.com/Popa-42/pycardgame/issues/>`_ page

#. Create a new issue with:

   - Your Python version (``python --version``)
   - Your operating system
   - The exact error message
   - Steps to reproduce the issue
