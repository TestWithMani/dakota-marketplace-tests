# Utility Scripts

This directory contains utility scripts used for test automation setup and maintenance.

## Scripts

### `add_markers.py`
Script to add pytest markers to test files. This script:
- Adds tab markers (e.g., `@pytest.mark.accounts`) to identify which tab a test belongs to
- Adds suite markers (e.g., `@pytest.mark.column_names`) to identify which test suite it belongs to
- Automatically imports pytest if not already imported
- Skips files that already have markers

**Usage:**
```bash
python scripts/add_markers.py
```

**When to use:**
- When adding new test files that need markers
- If markers need to be re-added to test files
- To ensure all test files have proper markers

### `extract_tabs.py`
Helper script to extract tab names from test file names. Used internally by `add_markers.py`.

**Note:** These scripts have already been run on all existing test files. They are kept here for future use when new test files are added.

