# Jenkins Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Required Jenkins Plugins

Go to **Manage Jenkins → Plugins → Available** and install:
- Email Extension Plugin
- HTML Publisher Plugin
- Allure Plugin
- AnsiColor Plugin
- Timestamper Plugin

### Step 2: Configure Email (SMTP)

**Manage Jenkins → Configure System → Extended E-mail Notification**

Example for Gmail:
```
SMTP server: smtp.gmail.com
Port: 587
Use TLS: ✓
Username: your-email@gmail.com
Password: [App Password]
```

### Step 3: Create Pipeline Job

1. **New Item** → Name: `Dakota-Marketplace-Tests`
2. Select **Pipeline**
3. **Pipeline** section:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/TestWithMani/dakota-marketplace-tests`
   - Branch: `*/main` (or `*/master`)
   - Script Path: `Jenkinsfile`
4. **Save**

### Step 4: Run First Build

1. Click **Build with Parameters**
2. Select:
   - ENVIRONMENT: `uat`
   - PORTAL: `Default` (or select a specific portal)
   - TEST_SUITE: Check `all` or select specific suites
   - MARKERS: (optional) Select specific tab or portal markers
   - SEND_EMAIL: `true`
   - ADDITIONAL_EMAILS: (optional) Add comma-separated email addresses
3. Click **Build**

### Step 5: Verify

- ✅ Check build console output
- ✅ View HTML report
- ✅ Check email notification

## 📧 Email Template Features

The email notification includes:
- ✅ Beautiful HTML template with gradient header
- ✅ Build status badge (Success/Failure/Unstable)
- ✅ Test statistics (Total, Passed, Failed, Skipped)
- ✅ Build information (Branch, Commit, Duration)
- ✅ Quick links to reports and build details
- ✅ Color-coded status indicators

## 🎯 Common Commands

### Run All Tests
```
Build with Parameters → TEST_SUITE: all
```

### Run Specific Suite
```
Build with Parameters → TEST_SUITE: column_names
```

### Run on Production
```
Build with Parameters → ENVIRONMENT: prod → PORTAL: Default
```

### Run on Specific Portal
```
Build with Parameters → ENVIRONMENT: uat → PORTAL: FA Portal
```

## 🔗 Important Links

- **Jenkins URL**: http://localhost:8080/
- **GitHub Repo**: https://github.com/TestWithMani/dakota-marketplace-tests
- **Email Recipient**: usman.arshad@rolustech.com

## ⚙️ Pipeline Features

- ✅ Automatic virtual environment setup
- ✅ Dependency installation
- ✅ Parallel test execution support
- ✅ HTML and Allure reports
- ✅ Email notifications with beautiful template
- ✅ Build history retention (30 builds)
- ✅ Test result archiving
- ✅ Multiple test suite support
- ✅ Environment selection (UAT/PROD)
- ✅ Portal selection (Default, FA Portal, RIA Portal, FO Portal, Benchmark Portal, Recommends Portal, FA and RIA Portal)
- ✅ Portal-specific test markers

---

**Need help?** See `JENKINS_SETUP_GUIDE.md` for detailed instructions.

