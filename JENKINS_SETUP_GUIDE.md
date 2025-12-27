# Jenkins CI/CD Setup Guide for Dakota Marketplace Tests

This guide will help you set up Jenkins CI/CD pipeline for your Dakota Marketplace test automation project.

## 📋 Prerequisites

### 1. Jenkins Installation
- Jenkins should be running on `http://localhost:8080/`
- Jenkins credentials: `admin` / `admin123`

### 2. Required Jenkins Plugins

Install the following plugins from **Manage Jenkins → Plugins**:

#### Essential Plugins:
- ✅ **Pipeline** (usually pre-installed)
- ✅ **Git Plugin** (usually pre-installed)
- ✅ **Email Extension Plugin** - For email notifications
- ✅ **HTML Publisher Plugin** - For HTML test reports
- ✅ **Allure Plugin** - For Allure test reports
- ✅ **AnsiColor Plugin** - For colored console output
- ✅ **Timestamper Plugin** - For build timestamps
- ✅ **Build Timeout Plugin** - For build timeout management

#### Installation Steps:
1. Go to **Jenkins Dashboard → Manage Jenkins → Manage Plugins**
2. Click on **Available** tab
3. Search for each plugin name
4. Check the box next to each plugin
5. Click **Install without restart** (or **Download now and install after restart**)
6. Restart Jenkins if required

### 3. System Requirements
- **Python 3.10+** installed and available in PATH
- **Chrome Browser** installed
- **Allure CLI** (optional, for Allure reports)
  - Download from: https://github.com/allure-framework/allure2/releases
  - Add to system PATH

### 4. Email Configuration (SMTP)

Configure SMTP settings for email notifications:

1. Go to **Manage Jenkins → Configure System**
2. Scroll to **Extended E-mail Notification** section
3. Configure SMTP settings:
   - **SMTP server**: Your email server (e.g., `smtp.gmail.com`, `smtp.office365.com`)
   - **SMTP Port**: Usually `587` (TLS) or `465` (SSL)
   - **Use SSL**: Check if using SSL
   - **Use TLS**: Check if using TLS
   - **Username**: Your email address
   - **Password**: Your email password or app password
   - **Default user e-mail suffix**: `@rolustech.com` (optional)

**Note**: For Gmail, you may need to use an App Password instead of your regular password.

## 🚀 Setup Steps

### Step 1: Create Pipeline Job

1. **Open Jenkins Dashboard**
   - Navigate to `http://localhost:8080/`

2. **Create New Item**
   - Click **New Item** on the left sidebar
   - Enter job name: `Dakota-Marketplace-Tests` (or your preferred name)
   - Select **Pipeline** as the job type
   - Click **OK**

### Step 2: Configure Pipeline Job

1. **General Settings**
   - **Description**: "CI/CD Pipeline for Dakota Marketplace Test Automation"
   - Check **GitHub project** (optional)
     - Project url: `https://github.com/TestWithMani/dakota-marketplace-tests`

2. **Build Triggers**
   - Select one or more:
     - ✅ **GitHub hook trigger for GITScm polling** (for webhook-based builds)
     - ✅ **Poll SCM** (schedule: `H/15 * * * *` for every 15 minutes)
     - ✅ **Build periodically** (e.g., `0 2 * * *` for daily at 2 AM)

3. **Pipeline Configuration**
   - **Definition**: Select **Pipeline script from SCM**
   - **SCM**: Select **Git**
   - **Repository URL**: `https://github.com/TestWithMani/dakota-marketplace-tests`
   - **Credentials**: Leave empty (public repo)
   - **Branches to build**: 
     - Branch Specifier: `*/main` or `*/master` (depending on your default branch)
   - **Script Path**: `Jenkinsfile`
   - **Lightweight checkout**: Uncheck this (if available)

4. **Advanced Settings** (optional)
   - **Additional Behaviours**: 
     - Add **Check out to a sub-directory** (optional)
     - Add **Clean before checkout** (recommended)

5. **Click Save**

### Step 3: Configure GitHub Webhook (Optional but Recommended)

For automatic builds on push to GitHub:

1. **Get Jenkins URL**
   - Your Jenkins URL: `http://localhost:8080/`
   - **Note**: For webhooks to work, Jenkins needs to be accessible from GitHub
   - If running locally, you may need:
     - Port forwarding
     - ngrok (for temporary public URL)
     - Or use SCM polling instead

2. **Configure GitHub Webhook**
   - Go to your GitHub repository: `https://github.com/TestWithMani/dakota-marketplace-tests`
   - Click **Settings → Webhooks → Add webhook**
   - **Payload URL**: `http://localhost:8080/github-webhook/` (or your public URL)
   - **Content type**: `application/json`
   - **Which events**: Select **Just the push event**
   - **Active**: Checked
   - Click **Add webhook**

3. **Configure Jenkins for Webhooks**
   - In Jenkins, go to **Manage Jenkins → Configure System**
   - Find **GitHub** section
   - Add GitHub server (if needed)
   - Check **Specify another hook URL** (optional)

### Step 4: Test the Pipeline

1. **Manual Build**
   - Go to your Jenkins job
   - Click **Build with Parameters**
   - Select parameters:
     - **ENVIRONMENT**: `uat` (or `prod`)
     - **TEST_SUITE**: `all` (or specific suite)
     - **SEND_EMAIL**: `true`
   - Click **Build**

2. **Monitor Build**
   - Click on the build number
   - Click **Console Output** to see real-time logs
   - Wait for build to complete

3. **Verify Results**
   - Check **HTML Report** link in build page
   - Check **Allure Report** link (if Allure is installed)
   - Verify email notification received

## 📧 Email Configuration Details

### Gmail SMTP Configuration

If using Gmail for email notifications:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account → Security → App passwords
   - Generate a new app password for "Mail"
   - Use this password in Jenkins SMTP configuration

3. **Jenkins SMTP Settings**:
   ```
   SMTP server: smtp.gmail.com
   SMTP Port: 587
   Use TLS: ✓
   Username: your-email@gmail.com
   Password: [App Password from step 2]
   ```

### Office 365 SMTP Configuration

If using Office 365:

```
SMTP server: smtp.office365.com
SMTP Port: 587
Use TLS: ✓
Username: usman.arshad@rolustech.com
Password: [Your password]
```

## 🎯 Pipeline Parameters

The pipeline supports the following parameters:

| Parameter | Options | Description |
|-----------|---------|-------------|
| **ENVIRONMENT** | `uat`, `prod` | Test environment to run against |
| **TEST_SUITE** | `all`, `column_names`, `fields_comparison`, `fields_display`, `lazy_loading`, `list_view_crud`, `pin_unpin` | Test suite to execute |
| **SEND_EMAIL** | `true`, `false` | Send email notification after build |

## 📊 Reports and Artifacts

The pipeline generates and publishes:

1. **HTML Test Report**
   - Location: `reports/report.html`
   - Accessible via: Build page → HTML Report link

2. **Allure Test Report** (if Allure CLI installed)
   - Location: `allure-report/`
   - Accessible via: Build page → Allure Report link

3. **Test Artifacts**
   - HTML report archived
   - Allure results archived

## 🔧 Troubleshooting

### Issue: Python not found
**Solution**: 
- Ensure Python is installed and in system PATH
- Test by running `python --version` in command prompt
- Add Python to PATH if needed

### Issue: Chrome/ChromeDriver issues
**Solution**:
- Ensure Chrome browser is installed
- The pipeline uses `webdriver-manager` which auto-downloads ChromeDriver
- If issues persist, manually install ChromeDriver and add to PATH

### Issue: Email not sending
**Solution**:
- Verify SMTP settings in Jenkins configuration
- Check Jenkins logs: **Manage Jenkins → System Log**
- Test email configuration: **Manage Jenkins → System Configuration → Test configuration by sending test e-mail**

### Issue: Allure report not generating
**Solution**:
- Install Allure CLI and add to PATH
- Or skip Allure (pipeline will continue without it)
- Reports will still be available as HTML

### Issue: Build fails on checkout
**Solution**:
- Verify GitHub repository URL is correct
- Check internet connectivity
- Verify repository is public (or add credentials if private)

### Issue: Tests fail
**Solution**:
- Check test logs in Console Output
- Verify environment configuration in `config/config.json`
- Ensure test environment is accessible
- Check Chrome browser is installed and working

## 🔄 Running Different Test Suites

You can run specific test suites by selecting them in the build parameters:

- **all**: Runs all tests in `tests/` directory
- **column_names**: Tests in `tests/all_tabs_column_name/`
- **fields_comparison**: Tests in `tests/all_tabs_fields_comparison/`
- **fields_display**: Tests in `tests/all_tabs_fields_display_functionality/`
- **lazy_loading**: Tests in `tests/all_tabs_lazy_loading/`
- **list_view_crud**: Tests in `tests/all_tabs_list_view_crud/`
- **pin_unpin**: Tests in `tests/all_tabs_pin_unpin_functionality/`

## 📝 Best Practices

1. **Regular Builds**: Set up scheduled builds (e.g., nightly)
2. **Branch Strategy**: Consider using multi-branch pipeline for different branches
3. **Build Retention**: Configure build retention policy (already set to 30 builds)
4. **Notifications**: Keep email notifications enabled for important builds
5. **Monitoring**: Regularly check build trends and test results
6. **Environment Management**: Use different environments for different test scenarios

## 🆘 Support

If you encounter any issues:

1. Check Jenkins console output for detailed error messages
2. Review Jenkins system logs
3. Verify all prerequisites are installed
4. Check GitHub repository accessibility
5. Verify email SMTP configuration

## ✅ Verification Checklist

Before considering setup complete, verify:

- [ ] Jenkins is running and accessible
- [ ] All required plugins are installed
- [ ] Python is installed and in PATH
- [ ] Chrome browser is installed
- [ ] GitHub repository is accessible
- [ ] Pipeline job is created and configured
- [ ] Test build runs successfully
- [ ] HTML report is generated and accessible
- [ ] Email notification is received
- [ ] Allure report works (if Allure CLI installed)

---

**Setup Complete!** 🎉

Your Jenkins CI/CD pipeline is now ready to run your Dakota Marketplace tests automatically.

