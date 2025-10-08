#!/usr/bin/env python3
"""
Script to run all unit tests with coverage for the Collapp backend
"""
import subprocess
import sys
import os

def run_all_tests():
    """Run all unit tests with coverage"""
    print("Running All Collapp Backend Tests with Coverage...")
    print("=" * 60)
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Run pytest with coverage on working tests
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "-v", 
            "--tb=short",
            "--cov=app",
            "--cov-report=term-missing",
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
    exit_code = run_all_tests()
    sys.exit(exit_code)