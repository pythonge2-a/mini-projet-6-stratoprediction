"""
Module 'simulation'
================

Ce module fournit des fonctions pour calculer la trajectoire du ballon stratosphérique,
ainsi que quelques fonctions utilitaires de conversions d'unités.
"""

from .simulation import Balloon
from .utils import get_bounding_square

# Pas utile dans ce cas, mais ça fait pro :)
__all__ = ["Balloon","get_bounding_square"]