"""
SQL FHIR Library Generator

A Python library that extracts @annotations from SQL file comments and creates FHIR Library resources.
"""

from .parser import SQLAnnotationParser
from .fhir_builder import FHIRLibraryBuilder

__version__ = "1.0.0"
__author__ = "SQL FHIR Library Generator Team"

__all__ = [
    "SQLAnnotationParser",
    "FHIRLibraryBuilder",
]
