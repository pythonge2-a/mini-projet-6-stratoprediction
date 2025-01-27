"""
Module 'display'
================

Ce module permet d'afficher la trajectoire du ballon stratosphérique en 2d et 3d,
ainsi que sur une carte géographique.
"""

from .display import plot_trajectories_2d, plot_trajectories_3d, show_on_map

# Pas utile dans ce cas, mais ça fait pro :)
__all__ = ["plot_trajectories_2d", "plot_trajectories_3d", "show_on_map"]