"""
Module 'display'
================

Ce module permet d'afficher la trajectoire du ballon stratosphérique en 2d et 3d,
ainsi que sur une carte géographique.
"""

from .display import plot_trajectory_2d, plot_trajectory_3d,plot_trajectories_3d, show_on_map

# Pas utile dans ce cas, mais ça fait pro :)
__all__ = ["plot_trajectory_2d", "plot_trajectory_3d", "show_on_map", "plot_trajectories_3d"]