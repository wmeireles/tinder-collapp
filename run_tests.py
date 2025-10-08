#!/usr/bin/env python3
"""
Script to run all unit tests for the Collapp backend
"""
import subprocess
import sys
import os

def run_tests():
    """Run all unit tests"""
    print("Running Collapp Backend Unit Tests...")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Run pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "-v", 
            "--tb=short",
            "tests/test_simple_endpoints.py",
            "tests/test_security.py", 
            "tests/test_utils.py"
        ], capture_output=False)
        
        if result.returncode == 0:
            print("\nAll tests passed!")
        else:
            print("\nSome tests failed!")
            
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)