# tests/conftest.py
import sys
import os
import pytest

# Add the src folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# -------------------------
# Register Custom Markers
# -------------------------
def pytest_configure(config):
    markers = [
        "navigation: Tests Related To Robot Navigation",
        "pick_and_place: Tests for Pick and Place Sequences",
        "safety: Safety-related Tests",
        "action: Real Action Tests",
        "extend: Extended Tests",
        "sensors: Sensor-related Tests",
        "walking: Walking Tests",
    ]
    for mark in markers:
        config.addinivalue_line("markers", mark)

# -------------------------
# Pytest HTML Report Hooks
# -------------------------
def pytest_html_report_title(report):
    report.title = "Robot Simulation TDD Test Reports"

def pytest_html_results_table_header(cells):
    """Add Suite and Author columns to HTML report header."""
    cells.insert(1, "Suite")   # Insert after test name
 #  cells.insert(2, "Author")  # Insert after Suite

def pytest_html_results_table_row(report, cells):
    """Populate Suite and Author columns for each test row."""
    suite_markers = ["navigation", "pick_and_place", "safety", "action", "extend", "walking", "sensors"]
    suite = "General"

    # report.keywords is a dict containing test markers
    for m in suite_markers:
        if m in getattr(report, "keywords", {}):
            suite = m
            break

    cells.insert(1, suite)          # Suite column
  # cells.insert(2, "Bang Thien Nguyen")  # Author column

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.append("Author: Bang Thien Nguyen")

# -------------------------
# Optional metadata
# -------------------------
def pytest_metadata(metadata):
    metadata['Author'] = "Bang Thien Nguyen"
    metadata['Project'] = "Robot Simulation TDD"
