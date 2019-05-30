# -*- coding: utf-8 -*-

"""
    oddcrawler
"""

__version__ = "0.1.0"

from .monumental import MonumentalExtractor
from .cr_hoy import CRHoyExtractor
from .la_prensa_libre import LaPrensaLibreExtractor
from .la_republica import LaRepublicaExtractor
from .webpage_extractors import WebpageExtractor
from .job_metadata import ExtractorJob
from .job_metadata import NewsFilter
from .database_manager import Database
