"""
Module 'simulation'
================

Ce module fournit des fonctions pour calculer la trajectoire du ballon stratosphérique,
ainsi que quelques fonctions utilitaires de conversions d'unités.
"""

from .simulation import Balloon
from .utils import prepare_wind_interpolators, prepare_temperature_interpolator, prepare_gp_height_interpolator

# Pas utile dans ce cas, mais ça fait pro :)
__all__ = ["Balloon", "prepare_wind_interpolators", "prepare_temperature_interpolator", "prepare_gp_height_interpolator"]