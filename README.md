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
│   └── config.json          # Environment configurations
├── pages/
│   └── login_page.py        # Page Object Model classes
├── tests/
│   └── test_login.py        # Test cases
├── reports/                 # Test reports (generated)
├── conftest.py             # Pytest fixtures and configuration
├── requirements.txt        # Python dependencies
└── pytest.ini             # Pytest configuration
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
$env:ENV="uat"
.\venv\Scripts\python.exe -m pytest
```

## 📊 Test Reports

- **HTML Report**: Generated in `reports/report.html`
- **Allure Report**: Results in `allure-results/` (requires Allure CLI)

## ⚙️ Configuration

Edit `config/config.json` to configure different environments (UAT, PROD, etc.).

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

