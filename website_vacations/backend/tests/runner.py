"""Test runner that executes all tests."""

import sys
import pytest


def test_all() -> int:
    """
    Execute all tests in the test suite.
    This function runs all test classes and functions.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Run pytest with verbose output
    return pytest.main(["-v", "tests/"])


def main() -> int:
    """Main entry point for test runner."""
    return test_all()


if __name__ == "__main__":
    sys.exit(main())



