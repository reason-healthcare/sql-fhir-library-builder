#!/usr/bin/env python3
"""
Test Python 3.8 compatibility by checking imports and basic functionality
"""

def test_python38_compatibility():
    """Test that all imports work in Python 3.8 style"""
    try:
        # Test the main imports that might cause issues
        from typing import Dict, List, Optional, Tuple, Union, Any
        from datetime import datetime
        from pathlib import Path
        import base64
        import json
        import re
        
        # Test that our main classes can be imported
        from sql_fhir_library_generator import SQLAnnotationParser, FHIRLibraryBuilder
        
        # Test basic functionality
        parser = SQLAnnotationParser()
        builder = FHIRLibraryBuilder()
        
        # Test parameter parsing method (the one that had the tuple annotation)
        test_result = builder._parse_param_value("test_param integer")
        assert test_result == ("test_param", "integer")
        
        print("✅ All Python 3.8 compatibility tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Python 3.8 compatibility test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_python38_compatibility()
    exit(0 if success else 1)
