# Dakota Marketplace Test Automation

Selenium-based test automation framework for Dakota Marketplace using pytest.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Chrome browser installed

### Setup

1. **Run the setup script** (first time only):
   ```powershell
   .\setup.ps1
   ```

2. **Activate the virtual environment**:
   ```powershell
   .\activate.ps1
   ```

3. **Run tests**:
   ```powershell
   .\run_tests.ps1
   ```

## 📁 Project Structure

```
Dakota_MP/
├── config/
│   ├── config.json          # URLs, credentials, supported portals
│   ├── settings.py        # ENV parsing, resolve_runtime_config
│   └── urls.py            # URL key helpers
├── login_page.py          # Login page object
├── tests/                 # Tab tests (markers for suites + portals)
├── reports/               # Test reports (generated)
├── conftest.py            # Pytest fixtures (driver, base_url, portal, …)
├── requirements.txt
└── pytest.ini
```

## 🛠️ Manual Setup

If you prefer to set up manually:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## 🧪 Running Tests

### Run all tests
```powershell
.\run_tests.ps1
```

### Run with pytest directly
```powershell
.\venv\Scripts\python.exe -m pytest
```

### Run specific test file
```powershell
.\venv\Scripts\python.exe -m pytest tests/test_login.py
```

### Run with specific environment
```powershell
# Run with original UAT
$env:ENV="uat"
.\venv\Scripts\python.exe -m pytest

# Run with UAT FA Data Set portal
$env:ENV="uat_fa_data_set"
.\venv\Scripts\python.exe -m pytest

# Run with PROD Dakota Ria Portal
$env:ENV="prod_dakota_ria_portal"
.\venv\Scripts\python.exe -m pytest
```

## 📊 Test Reports

- **HTML Report**: Generated in `reports/report.html`
- **Allure Report**: Results in `allure-results/` (requires Allure CLI)

## ⚙️ Configuration

`config/config.json` is now normalized for easy maintenance:

- `base_urls`: one URL per base environment (`uat`, `prod`)
- `credentials.base`: All Marketplace Access (base) credentials per environment (`uat` / `prod`)
- `credentials.portals`: portal-specific creds per base environment
- `urls`: single shared URL key map used by all environments

Set runtime environment with `ENV`:

- All Marketplace Access: `uat` / `prod` (uses `credentials.base`)
- Other portals: `uat_fa_data_set`, `prod_dakota_ria_portal`, `uat_dakota_private_markets_access`, etc. (uses `credentials.portals.<portal_key>`)

Filter tests by portal marker, for example:

```powershell
.\venv\Scripts\python.exe -m pytest -m all_marketplace_access
```


## 📦 Dependencies

- selenium==4.30.0
- pytest==8.2.0
- pytest-html==4.1.1
- allure-pytest==2.15.2
- webdriver-manager==4.0.2

## 🔧 VS Code Setup

The project is configured for VS Code with:
- Python interpreter pointing to venv
- Pytest integration
- Type checking enabled

Reload VS Code window after setup to ensure proper Python interpreter detection.

## 📝 Notes

- Virtual environment (`venv/`) is excluded from version control
- Cache files (`__pycache__/`, `.pytest_cache/`) are excluded
- Reports are generated automatically in `reports/` directory

## 🔄 Jenkins Branch Sync

To keep Jenkins jobs stable when one job points to `main` and another points to `master`, sync both branches after Jenkinsfile changes.

```powershell
# Sync main from master and push
.\sync_branches.ps1 -SourceBranch master -TargetBranch main -Push

# Optional: sync master from main and push
.\sync_branches.ps1 -SourceBranch main -TargetBranch master -Push
```

## 🧹 Safe Cleanup

Remove generated artifacts and cache folders:

```powershell
.\cleanup_generated.ps1
```

Optional: include local virtual environment too:

```powershell
.\cleanup_generated.ps1 -IncludeVenv
```

