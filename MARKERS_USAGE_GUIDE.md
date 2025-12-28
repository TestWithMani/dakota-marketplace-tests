# Pytest Markers Usage Guide

**Status: This file is up to date with current test and CI marker usage.**

This guide explains how to use pytest markers to run specific tests in the Dakota Marketplace test suite.

## Overview

Each test file uses two kinds of markers:
1. **Tab Marker**: Shows which tab a test targets (e.g., `@pytest.mark.accounts`)
2. **Suite Marker**: Shows which kind of suite/test the test is (e.g., `@pytest.mark.column_names`)

## Running Tests with Markers

### Local Execution

**Run all tests for a specific tab:**
```bash
# Accounts tab
pytest -m accounts

# Contact tab
pytest -m contact

# Multiple tabs (OR logic)
pytest -m "accounts or contact"
```

**Run a specific suite for a given tab:**
```bash
# Only column_names tests for Accounts
pytest -m "accounts and column_names"

# Only lazy_loading for Contact tab
pytest -m "contact and lazy_loading"
```

**Run all tests of a specific suite:**
```bash
pytest -m column_names
pytest -m lazy_loading
```

**Use AND/OR logic for multiple tabs/suites:**
```bash
# All tests for Accounts OR Contact
pytest -m "accounts or contact"

# Only column_names tests across Accounts AND Contact
pytest -m "column_names and (accounts or contact)"
```

### Jenkins Execution

1. Go to **Jenkins Job** → **Build with Parameters**

2. **Option 1: Use Markers (recommended for tab selection)**
    - Leave **TEST_SUITE** at default (it’s ignored)
    - In **MARKERS**:
        - Enter a single tab: `accounts`
        - Or multiple tabs (OR logic): `accounts,contact`
        - Tab + suite: `accounts and column_names`
        - Complex: `(accounts or contact) and column_names`

3. **Option 2: Use Test Suite (legacy method)**
    - Leave **MARKERS** empty
    - Select a **TEST_SUITE** from the dropdown

---

## Available Tab Markers

- `accounts`
- `contact`
- `all_documents`
- `filings_13f_investments_search` *(marker names cannot start with digits)*
- `conference_search`
- `consultant_reviews`
- `continuation_vehicle`
- `dakota_city_guides`
- `dakota_searches`
- `dakota_video_search`
- `fee_schedules_dashboard`
- `fund_family_memos`
- `fund_launches`
- `investment_allocator_accounts`
- `investment_allocator_contacts`
- `investment_firm_accounts`
- `investment_firm_contacts`
- `manager_presentation_dashboard`
- `my_accounts`
- `pension_documents`
- `portfolio_companies`
- `portfolio_companies_contacts`
- `private_fund_search`
- `public_company_search`
- `public_investments_search`
- `public_plan_minutes_search`
- `recent_transactions`
- `university_alumni_contacts`

## Available Suite Markers

- `column_names`
- `fields_comparison`
- `fields_display`
- `lazy_loading`
- `list_view_crud`
- `pin_unpin`

---

## Examples

**1. All Accounts tab tests:**
```bash
pytest -m accounts
```
Jenkins: `MARKERS = accounts`

**2. All Accounts OR Contact tab tests:**
```bash
pytest -m "accounts or contact"
```
Jenkins: `MARKERS = accounts,contact`

**3. Only column_names for Accounts:**
```bash
pytest -m "accounts and column_names"
```
Jenkins: `MARKERS = accounts and column_names`

**4. Only lazy_loading for Accounts OR Contact:**
```bash
pytest -m "lazy_loading and (accounts or contact)"`
```
Jenkins: `MARKERS = lazy_loading and (accounts or contact)`

**5. All column_names (using suite):**
```bash
pytest -m column_names
```
Jenkins: `TEST_SUITE = column_names` (leave MARKERS empty)

---

## Notes

- If **MARKERS** is set in Jenkins, **TEST_SUITE** is ignored.
- Comma-separated values in MARKERS = OR logic.
- Use "and"/"or" for advanced logic; parentheses are supported.
- All marker names are **case-sensitive** and must use lowercase/underscores.

*This file is kept current. If you notice inconsistencies, confirm with latest marker usage in Jenkins parameters or test decorators.*

