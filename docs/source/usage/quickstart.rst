**********
Quickstart
**********

Installation
============

PyCardGame can simply be installed using pip. Open your terminal or command prompt and
run the following command:

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ pycardgame

Usage
=====

The PyCardGame package is a highly customizable card game engine. It provides a
framework for creating card games with various rules and mechanics. The package
comes with a set of pre-defined games, but you can also create your own custom
games by extending the base classes provided by the package.

To get started, let's create a simple card game by following these steps:

1. **Import the necessary modules**: Start by importing the required classes and functions from the PyCardGame package.

   .. code-block:: python

      from pycardgame import Game, Player, Card, Deck

2. **Define the game rules**: Create a class that defines the rules of your game. This class should inherit from the `Game` class provided by the package.
