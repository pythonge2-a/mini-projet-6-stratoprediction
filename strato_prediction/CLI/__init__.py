"""
Module 'CLI'
================

Ce module s'occupe de la gestion des argements entrés par la ligne de commande.
"""

from .console import console
from .args import args_retrieval

# Pas utile dans ce cas, mais ça fait pro :)
__all__ = ["console", "args_retrieval"]