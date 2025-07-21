"""
SQL FHIR Library Generator

A Python library that extracts @annotations from SQL file comments and creates FHIR Library resources.
"""

from .fhir_builder import FHIRLibraryBuilder
from .parser import SQLAnnotationParser

__version__ = "1.0.0"
__author__ = "SQL FHIR Library Generator Team"

__all__ = [
    "SQLAnnotationParser",
    "FHIRLibraryBuilder",
]
