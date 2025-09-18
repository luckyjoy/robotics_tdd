# run_all_tests.py
import pytest
import sys

def main():
    # Default: run all simulation tests
    sys.exit(pytest.main(["-v", "-m", "sim", "tests/"]))

if __name__ == "__main__":
    main()
