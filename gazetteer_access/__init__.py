"""
gazetteer_access.

Simple Python library supporting the access to the who's on first gazetteer data.
"""
from .geocode import geocode_placename
from .reverse_geocode import reverse_geocode_point
from .zonal_statistics import zonal_statistics

__version__ = "0.1.0"
__author__ = 'Bruno Martins'
__credits__ = 'MOOD Project'