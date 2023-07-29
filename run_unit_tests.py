#!/usr/bin/env python
import unittest
import subprocess

def run_unit_tests():
    suite = unittest.TestLoader().discover(start_dir="unit_tests.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    exit_code = 0
    try:
        if not run_unit_tests():
            print("Unit tests failed. Please fix the issues before committing.")
            exit_code = 1
    except Exception as e:
        print("An error occurred while running unit tests:", str(e))
        exit_code = 1
    exit(exit_code)
