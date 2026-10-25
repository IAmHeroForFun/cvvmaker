#!/usr/bin/env python3
"""
Direct cross-platform entry point for CV Maker.
Run via: python run.py
"""
import os
import sys

# Ensure UTF-8 locale
if not os.environ.get("LC_ALL"):
    os.environ["LC_ALL"] = "en_US.UTF-8"
if not os.environ.get("LANG"):
    os.environ["LANG"] = "en_US.UTF-8"

# Add script directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cvmaker.__main__ import main

if __name__ == "__main__":
    main()
