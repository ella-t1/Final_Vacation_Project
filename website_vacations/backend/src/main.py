"""Main entry point for the Vacations backend project."""

import os

from dotenv import load_dotenv

from src.config import DbConfig
from tests.runner import test_all


def main() -> None:
    """Main function that runs all tests."""
    load_dotenv()
    cfg = DbConfig.from_env()
    print("Vacations backend project")
    print(f"DB host={cfg.host} db={cfg.name} user={cfg.user}")
    print("\nRunning all tests...\n")
    
    # Run all tests as required by project specifications
    exit_code = test_all()
    
    if exit_code == 0:
        print("\n[OK] All tests passed!")
    else:
        print(f"\n[ERROR] Tests failed with exit code {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    exit(main())



