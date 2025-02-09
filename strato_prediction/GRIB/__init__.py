"""
Module 'data_retrieval'
================

Ce module fournit des fonctions pour télécharger et récupérer les données d'un fichier GRIB.
"""

from .data_retrieval import download_grib_file, load_grib_data,download_next_grib_file, interpolate_data

# Pas utile dans ce cas, mais ça fait pro :)
__all__ = ["download_grib_file", "load_grib_data","download_next_grib_file", "interpolate_data"]