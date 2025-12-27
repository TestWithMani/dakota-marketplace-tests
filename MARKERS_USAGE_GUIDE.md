# Pytest Markers Usage Guide

This guide explains how to use pytest markers to run specific tests in the Dakota Marketplace test suite.

## Overview

Each test file has been tagged with two types of markers:
1. **Tab Marker**: Identifies which tab the test belongs to (e.g., `@pytest.mark.accounts`)
2. **Suite Marker**: Identifies which test suite it belongs to (e.g., `@pytest.mark.column_names`)

## Running Tests with Markers

### Local Execution

#### Run all tests for a specific tab (all 6 test cases)
```bash
# Run all tests for Accounts tab
pytest -m accounts

# Run all tests for Contact tab
pytest -m contact

# Run all tests for multiple tabs (OR logic)
pytest -m "accounts or contact"
```

#### Run specific suite for a specific tab
```bash
# Run only column_names tests for Accounts tab
pytest -m "accounts and column_names"

# Run only lazy_loading tests for Contact tab
pytest -m "contact and lazy_loading"
```

#### Run all tests in a specific suite
```bash
# Run all column_names tests
pytest -m column_names

# Run all lazy_loading tests
pytest -m lazy_loading
```

#### Run multiple tabs with AND/OR logic
```bash
# Run all tests for Accounts OR Contact tabs
pytest -m "accounts or contact"

# Run column_names tests for Accounts AND Contact tabs
pytest -m "column_names and (accounts or contact)"
```

### Jenkins Execution

1. **Go to Jenkins Job** → **Build with Parameters**

2. **Option 1: Use Markers (Recommended for tab-based selection)**
   - Leave **TEST_SUITE** as default (it will be ignored)
   - In **MARKERS** field, enter:
     - Single tab: `accounts`
     - Multiple tabs: `accounts,contact` (comma-separated, uses OR logic)
     - Tab + Suite: `accounts and column_names`
     - Complex: `(accounts or contact) and column_names`

3. **Option 2: Use Test Suite (Traditional method)**
   - Leave **MARKERS** empty
   - Select **TEST_SUITE** from dropdown

## Available Tab Markers

- `accounts`
- `contact`
- `all_documents`
- `13f_filings_investments_search`
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

## Examples

### Example 1: Run all tests for Accounts tab
```bash
pytest -m accounts
```
**Jenkins**: Set MARKERS = `accounts`

### Example 2: Run all tests for Accounts and Contact tabs
```bash
pytest -m "accounts or contact"
```
**Jenkins**: Set MARKERS = `accounts,contact`

### Example 3: Run only column_names tests for Accounts tab
```bash
pytest -m "accounts and column_names"
```
**Jenkins**: Set MARKERS = `accounts and column_names`

### Example 4: Run lazy_loading tests for Accounts OR Contact tabs
```bash
pytest -m "lazy_loading and (accounts or contact)"
```
**Jenkins**: Set MARKERS = `lazy_loading and (accounts or contact)`

### Example 5: Run all column_names tests (traditional suite method)
```bash
pytest -m column_names
```
**Jenkins**: Set TEST_SUITE = `column_names` (leave MARKERS empty)

## Notes

- When MARKERS is specified in Jenkins, TEST_SUITE selection is ignored
- Comma-separated markers in Jenkins are treated as OR logic
- Use "and" for AND logic, "or" for OR logic
- Parentheses can be used for complex expressions
- All markers are case-sensitive and use lowercase with underscores

