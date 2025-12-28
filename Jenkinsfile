pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '30'))
        timeout(time: 60, unit: 'MINUTES')
        timestamps()
        ansiColor('xterm')
    }
    
    environment {
        // Python virtual environment path
        VENV_PATH = "${WORKSPACE}\\venv"
        PYTHON_EXE = "${VENV_PATH}\\Scripts\\python.exe"
        PIP_EXE = "${VENV_PATH}\\Scripts\\pip.exe"
        
        // Test environment (default: uat)
        ENV = "${params.ENVIRONMENT ?: 'uat'}"
        
        // Report paths
        HTML_REPORT = "${WORKSPACE}\\reports\\report.html"
        ALLURE_RESULTS = "${WORKSPACE}\\allure-results"
        ALLURE_REPORT = "${WORKSPACE}\\allure-report"
        
        // Email configuration
        EMAIL_RECIPIENT = 'usman.arshad@rolustech.com'
    }
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['uat', 'prod'],
            description: 'Select the test environment to run tests against'
        )
        extendedChoice(
            name: 'TEST_SUITE',
            type: 'PT_MULTI_SELECT',
            value: 'all,Column Names Validation,Fields Comparison,Fields Display Functionality,Lazy Loading,List View CRUD Operations,Pin/Unpin Functionality',
            description: 'Select one or more test suites to run:\n\n- Column Names Validation - Validates column names across all tabs\n- Fields Comparison - Compares fields between different views\n- Fields Display Functionality - Tests field display features\n- Lazy Loading - Tests lazy loading functionality\n- List View CRUD Operations - Tests Create, Read, Update, Delete operations\n- Pin/Unpin Functionality - Tests pin and unpin features\n\nNote: Hold Ctrl/Cmd to select multiple suites. If markers are also selected, tests will be filtered by both suite and markers.',
            multiSelectDelimiter: ','
        )
        extendedChoice(
            name: 'MARKERS',
            type: 'PT_MULTI_SELECT',
            value: 'All Tests,Accounts Tab,Contact Tab,All Documents,13F Filings & Investments Search,Accounts (Default),Contact (Default),Investment Allocator - Accounts (Default),Investment Allocator - Contacts (Default),Investment Firm - Contacts (Default),My Accounts (Default),Portfolio Companies - Contacts (Default),University Alumni - Contacts (Default),Conference Search,Consultant Reviews,Continuation Vehicle,Dakota City Guides,Dakota Searches,Dakota Video Search,Fee Schedules Dashboard,Fund Family Memos,Fund Launches,Investment Allocator - Accounts,Investment Allocator - Contacts,Investment Firm - Accounts,Investment Firm - Contacts,Manager Presentation Dashboard,My Accounts,Pension Documents,Portfolio Companies,Portfolio Companies - Contacts,Private Fund Search,Public Company Search,Public Investments Search,Public Plan Minutes Search,Recent Transactions,University Alumni - Contacts',
            description: 'Select one or more test markers (tabs or specific test categories) to run:\n\n- Accounts Tab - Tests for Accounts tab\n- Contact Tab - Tests for Contact tab\n- All Documents - Document-related tests\n- And many more specific test categories...\n\nNote: Hold Ctrl/Cmd to select multiple markers. Selected markers use OR logic. If test suites are also selected, both will be combined.',
            multiSelectDelimiter: ','
        )
        booleanParam(
            name: 'SEND_EMAIL',
            defaultValue: true,
            description: 'Send email notification after build completion'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out code from GitHub..."
                    checkout scm
                    echo "Code checked out successfully"
                    echo "Branch: ${env.BRANCH_NAME}"
                    echo "Commit: ${env.GIT_COMMIT.take(7)}"
                }
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    echo "Setting up Python virtual environment..."
                    
                    // Check if Python is available
                    bat '''
                        python --version
                        if errorlevel 1 (
                            echo Python is not installed or not in PATH
                            exit /b 1
                        )
                    '''
                    
                    // Create virtual environment if it doesn't exist
                    bat '''
                        if not exist "%VENV_PATH%" (
                            echo Creating virtual environment...
                            python -m venv "%VENV_PATH%"
                        ) else (
                            echo Virtual environment already exists
                        )
                    '''
                    
                    // Upgrade pip
                    bat '''
                        echo Upgrading pip...
                        "%PYTHON_EXE%" -m pip install --upgrade pip
                    '''
                    
                    echo "Python environment setup complete"
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing Python dependencies..."
                    bat '''
                        "%PIP_EXE%" install -r requirements.txt
                        if errorlevel 1 (
                            echo Failed to install dependencies
                            exit /b 1
                        )
                    '''
                    echo "Dependencies installed successfully"
                }
            }
        }
        
        stage('Create Directories') {
            steps {
                script {
                    echo "Creating report directories..."
                    bat '''
                        if not exist "%WORKSPACE%\\reports" mkdir "%WORKSPACE%\\reports"
                        if not exist "%WORKSPACE%\\allure-results" mkdir "%WORKSPACE%\\allure-results"
                        if not exist "%WORKSPACE%\\allure-report" mkdir "%WORKSPACE%\\allure-report"
                    '''
                    echo "Directories created"
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    echo "Environment: ${ENV}"
                    
                    def testCommand = buildTestCommand(params.TEST_SUITE, params.MARKERS)
                    echo "Test command: ${testCommand}"
                    
                    // Run tests (output will be visible in console, and we'll parse from HTML report)
                    // Capture exit code but don't fail the stage - we want to generate reports even if tests fail
                    def exitCode = bat(returnStatus: true, script: """
                        set ENV=${ENV}
                        ${testCommand}
                    """)
                    
                    // Store exit code for later use in post actions
                    env.TEST_EXIT_CODE = "${exitCode}"
                    
                    // Try to parse test statistics from HTML report after tests complete
                    // The HTML report is more reliable than console output parsing
                }
            }
            post {
                always {
                    script {
                        // Archive test results
                        archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
                        archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
                    }
                }
            }
        }
        
        stage('Generate Allure Report') {
            when {
                expression { true }
            }
            steps {
                script {
                    echo "Generating Allure report..."
                    try {
                        // Check if Allure is installed
                        bat '''
                            allure --version
                            if errorlevel 1 (
                                echo Allure CLI not found. Skipping Allure report generation.
                                echo Install Allure: https://github.com/allure-framework/allure2/releases
                                exit /b 0
                            )
                        '''
                        
                        // Generate Allure report
                        bat '''
                            allure generate "%ALLURE_RESULTS%" -o "%ALLURE_REPORT%" --clean
                        '''
                        
                        // Publish Allure report
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: 'allure-results']]
                        ])
                        
                        echo "Allure report generated successfully"
                    } catch (Exception e) {
                        echo "WARNING: Allure report generation skipped: ${e.getMessage()}"
                    }
                }
            }
        }
        
        stage('Publish Test Results') {
            when {
                expression { true }
            }
            steps {
                script {
                    echo "Publishing test results..."
                    
                    // Publish JUnit XML for Jenkins trends and history
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                    
                    // Publish HTML report
                    publishHTML([
                        reportName: 'Test Report',
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: true
                    ])
                    
                    echo "Test results published"
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Collect test statistics
                def testStats = getTestStatistics()
                
                // Override build status based on actual test results
                // This ensures builds are marked SUCCESS when all tests pass, even if junit marks them as UNSTABLE
                if (testStats.total > 0) {
                    if (testStats.failed == 0 && testStats.passed > 0) {
                        echo "All tests passed (${testStats.passed}/${testStats.total}). Setting build status to SUCCESS."
                        currentBuild.result = 'SUCCESS'
                    } else if (testStats.failed > 0) {
                        echo "Tests failed (${testStats.failed}/${testStats.total}). Setting build status to FAILURE."
                        currentBuild.result = 'FAILURE'
                    }
                }
                
                // Update build description
                def testSelectionParts = []
                if (params.TEST_SUITE && params.TEST_SUITE.trim() && params.TEST_SUITE != 'all' && params.TEST_SUITE != 'All Tests') {
                    def suites = params.TEST_SUITE.split(',').collect { it.trim() }.findAll { it && it != 'all' && it != 'All Tests' }
                    if (suites.size() > 0) {
                        testSelectionParts.add("Suites: ${suites.join(', ')}")
                    }
                }
                if (params.MARKERS && params.MARKERS.trim()) {
                    def markers = params.MARKERS.split(',').collect { it.trim() }.findAll { it && it != 'All Tests' }
                    if (markers.size() > 0) {
                        testSelectionParts.add("Markers: ${markers.join(', ')}")
                    }
                }
                def testSelection = testSelectionParts.size() > 0 ? testSelectionParts.join(' | ') : "All Tests"
                
                // Format duration - remove "and counting" if present
                def durationDisplay = currentBuild.durationString ?: 'N/A'
                if (durationDisplay.contains('and counting')) {
                    durationDisplay = durationDisplay.replace(' and counting', '')
                }
                
                currentBuild.description = """
                    Environment: ${ENV} | 
                    ${testSelection} | 
                    Tests: ${testStats.total} | 
                    Passed: ${testStats.passed} | 
                    Failed: ${testStats.failed} | 
                    Duration: ${durationDisplay}
                """.stripIndent().trim()
            }
        }
        
        success {
            script {
                echo "Build succeeded!"
                if (params.SEND_EMAIL) {
                    sendEmailNotification('SUCCESS')
                }
            }
        }
        
        failure {
            script {
                echo "Build failed!"
                if (params.SEND_EMAIL) {
                    sendEmailNotification('FAILURE')
                }
            }
        }
        
        unstable {
            script {
                // Check if build was marked unstable but all tests actually passed
                def testStats = getTestStatistics()
                if (testStats.total > 0 && testStats.failed == 0 && testStats.passed > 0) {
                    echo "Build was marked unstable, but all tests passed (${testStats.passed}/${testStats.total}). Setting build status to SUCCESS."
                    currentBuild.result = 'SUCCESS'
                    if (params.SEND_EMAIL) {
                        sendEmailNotification('SUCCESS')
                    }
                } else {
                echo "Build unstable!"
                if (params.SEND_EMAIL) {
                    sendEmailNotification('UNSTABLE')
                }
            }
        }
    }
    }
}

// Helper function to map display names to internal suite names
def mapSuiteDisplayToInternal(displayName) {
    def suiteMapping = [
        'All Tests': 'all',
        'Column Names Validation': 'column_names',
        'Fields Comparison': 'fields_comparison',
        'Fields Display Functionality': 'fields_display',
        'Lazy Loading': 'lazy_loading',
        'List View CRUD Operations': 'list_view_crud',
        'Pin/Unpin Functionality': 'pin_unpin'
    ]
    // Return mapped name or original if not found (for backward compatibility)
    return suiteMapping.get(displayName, displayName)
}

// Helper function to map display names to internal marker names
def mapMarkerDisplayToInternal(displayName) {
    def markerMapping = [
        'All Tests': 'all',
        'Accounts Tab': 'accounts',
        'Contact Tab': 'contact',
        'All Documents': 'all_documents',
        '13F Filings & Investments Search': 'filings_13f_investments_search',
        'Accounts (Default)': 'accounts_default',
        'Contact (Default)': 'contact_default',
        'Investment Allocator - Accounts (Default)': 'investment_allocator_accounts_default',
        'Investment Allocator - Contacts (Default)': 'investment_allocator_contacts_default',
        'Investment Firm - Contacts (Default)': 'investment_firm_contacts_default',
        'My Accounts (Default)': 'my_accounts_default',
        'Portfolio Companies - Contacts (Default)': 'portfolio_companies_contacts_default',
        'University Alumni - Contacts (Default)': 'university_alumni_contacts_default',
        'Conference Search': 'conference_search',
        'Consultant Reviews': 'consultant_reviews',
        'Continuation Vehicle': 'continuation_vehicle',
        'Dakota City Guides': 'dakota_city_guides',
        'Dakota Searches': 'dakota_searches',
        'Dakota Video Search': 'dakota_video_search',
        'Fee Schedules Dashboard': 'fee_schedules_dashboard',
        'Fund Family Memos': 'fund_family_memos',
        'Fund Launches': 'fund_launches',
        'Investment Allocator - Accounts': 'investment_allocator_accounts',
        'Investment Allocator - Contacts': 'investment_allocator_contacts',
        'Investment Firm - Accounts': 'investment_firm_accounts',
        'Investment Firm - Contacts': 'investment_firm_contacts',
        'Manager Presentation Dashboard': 'manager_presentation_dashboard',
        'My Accounts': 'my_accounts',
        'Pension Documents': 'pension_documents',
        'Portfolio Companies': 'portfolio_companies',
        'Portfolio Companies - Contacts': 'portfolio_companies_contacts',
        'Private Fund Search': 'private_fund_search',
        'Public Company Search': 'public_company_search',
        'Public Investments Search': 'public_investments_search',
        'Public Plan Minutes Search': 'public_plan_minutes_search',
        'Recent Transactions': 'recent_transactions',
        'University Alumni - Contacts': 'university_alumni_contacts'
    ]
    // Return mapped name or original if not found (for backward compatibility)
    return markerMapping.get(displayName, displayName)
}

// Helper function to build test command based on suite or markers
def buildTestCommand(testSuite, markers) {
    def baseCommand = "\"%PYTHON_EXE%\" -m pytest"
    def reportOptions = "--html=\"%HTML_REPORT%\" --self-contained-html --alluredir=\"%ALLURE_RESULTS%\" --json-report --json-report-file=\"reports/report.json\" --junitxml=\"reports/junit.xml\" -v --tb=short"
    
    // Parse multiple suites (extendedChoice returns comma-separated string)
    def suitesList = []
    if (testSuite && testSuite.trim()) {
        testSuite.split(',').each { suite ->
            def trimmed = suite.trim()
            if (trimmed && trimmed != 'all' && trimmed != 'All Tests') {
                // Map display name to internal name
                def internalName = mapSuiteDisplayToInternal(trimmed)
                suitesList.add(internalName)
            }
        }
    }
    def hasSuite = suitesList.size() > 0
    
    // Parse multiple markers (extendedChoice returns comma-separated string)
    def markersList = []
    if (markers && markers.trim()) {
        markers.split(',').each { marker ->
            def trimmed = marker.trim()
            if (trimmed && trimmed != 'all' && trimmed != 'All Tests') {
                // Map display name to internal name
                def internalName = mapMarkerDisplayToInternal(trimmed)
                markersList.add(internalName)
            }
        }
    }
    def hasMarkers = markersList.size() > 0
    
    // Build marker expression (multiple markers use OR logic)
    def markerExpression = null
    if (hasMarkers) {
        markerExpression = markersList.join(' or ')
    }
    
    // Case 1: Both suites and markers specified - combine them
    if (hasSuite && hasMarkers) {
        // Build test paths for multiple suites
        def testPaths = []
        suitesList.each { suite ->
            def path = getTestPath(suite)
            if (path && path != 'tests/') {
                testPaths.add(path)
            }
        }
        
        if (testPaths.size() > 0) {
            def pathsStr = testPaths.join(' ')
            echo "Running test suites: ${suitesList.join(', ')} from paths: ${testPaths.join(', ')} with markers: ${markerExpression}"
            return "${baseCommand} ${pathsStr} -m \"${markerExpression}\" ${reportOptions}"
        } else {
            // Fallback: if paths are empty, use marker-only approach
            echo "Running tests with markers: ${markerExpression}"
            return "${baseCommand} -m \"${markerExpression}\" ${reportOptions}"
        }
    }
    
    // Case 2: Only markers specified - run all suites with those markers
    if (hasMarkers) {
        echo "Running tests with markers: ${markerExpression}"
        return "${baseCommand} -m \"${markerExpression}\" ${reportOptions}"
    }
    
    // Case 3: Only suites specified - run all tests in those suites
    if (hasSuite) {
        def testPaths = []
        suitesList.each { suite ->
            def path = getTestPath(suite)
            if (path && path != 'tests/') {
                testPaths.add(path)
            }
        }
        
        if (testPaths.size() > 0) {
            def pathsStr = testPaths.join(' ')
            echo "Running test suites: ${suitesList.join(', ')} from paths: ${testPaths.join(', ')}"
            return "${baseCommand} ${pathsStr} ${reportOptions}"
        }
    }
    
    // Case 4: Neither specified - run all tests
    echo "Running all tests"
    return "${baseCommand} tests/ ${reportOptions}"
}

// Helper function to get test path based on suite selection
def getTestPath(testSuite) {
    def testPaths = [
        'all': 'tests/',
        'column_names': 'tests/all_tabs_column_name/',
        'fields_comparison': 'tests/all_tabs_fields_comparison/',
        'fields_display': 'tests/all_tabs_fields_display_functionality/',
        'lazy_loading': 'tests/all_tabs_lazy_loading/',
        'list_view_crud': 'tests/all_tabs_list_view_crud/',
        'pin_unpin': 'tests/all_tabs_pin_unpin_functionality/'
    ]
    return testPaths.get(testSuite, 'tests/')
}

// Helper function to get test statistics from HTML report
def getTestStatistics() {
    def stats = [
        total: 0,
        passed: 0,
        failed: 0,
        skipped: 0
    ]

    def jsonFile = 'reports/report.json'

    if (!fileExists(jsonFile)) {
        echo "pytest JSON report not found. Returning empty stats."
        return stats
    }

    try {
        // Read JSON file and parse using Groovy's JsonSlurper
        def jsonContent = readFile jsonFile
        def jsonSlurper = new groovy.json.JsonSlurper()
        def report = jsonSlurper.parseText(jsonContent)

        stats.passed  = report.summary?.passed  ?: 0
        stats.failed  = report.summary?.failed  ?: 0
        stats.skipped = report.summary?.skipped ?: 0

        // Deselected tests are NOT counted as executed
        stats.total = stats.passed + stats.failed + stats.skipped

        echo """
        Test Statistics (from JSON):
        Total   : ${stats.total}
        Passed  : ${stats.passed}
        Failed  : ${stats.failed}
        Skipped : ${stats.skipped}
        """.stripIndent()

    } catch (Exception e) {
        echo "Error parsing pytest JSON report: ${e.getMessage()}"
    }

    return stats
}

// Email notification function
def sendEmailNotification(buildStatus) {
    def testStats = getTestStatistics()
    
    // Determine actual status: verify with test statistics to ensure accuracy
    def actualStatus = buildStatus
    
    // Override based on test statistics if they contradict the parameter
    if (testStats.total > 0) {
        if (testStats.failed > 0) {
            // Tests failed - must be FAILURE
            actualStatus = 'FAILURE'
        } else if (testStats.passed > 0 && testStats.failed == 0) {
            // All tests passed - should be SUCCESS
            actualStatus = 'SUCCESS'
        }
    }
    
    echo "Email notification - Parameter: ${buildStatus}, Final status: ${actualStatus}, Tests: ${testStats.passed}/${testStats.total} passed, ${testStats.failed} failed"
    
    // Try to get user who triggered the build (avoiding getRawBuild() for script security)
    def triggeredBy = 'Muhammad Usman Arshad'
    try {
        // Try to get from BUILD_USER_ID environment variable first
        if (env.BUILD_USER_ID && env.BUILD_USER_ID != 'null') {
            triggeredBy = env.BUILD_USER_ID
        }
        // If BUILD_USER_ID is not available, use default
    } catch (Exception e) {
        triggeredBy = 'Muhammad Usman Arshad'
    }
    
    def statusColor = actualStatus == 'SUCCESS' ? '#28a745' : actualStatus == 'FAILURE' ? '#dc3545' : '#ffc107'
    def statusIcon = actualStatus == 'SUCCESS' ? '[PASS]' : actualStatus == 'FAILURE' ? '[FAIL]' : '[WARN]'
    
    // Format current date
    def currentDate = new Date().format("yyyy-MM-dd")
    def subject = "Dakota Automation Report - ${currentDate}"
    
    // Calculate pass percentage for progress bar
    def passPercentage = testStats.total > 0 ? (testStats.passed * 100 / testStats.total).intValue() : 0
    def failPercentage = testStats.total > 0 ? (testStats.failed * 100 / testStats.total).intValue() : 0
    def skipPercentage = testStats.total > 0 ? (testStats.skipped * 100 / testStats.total).intValue() : 0
    
    // Build test selection string for email
    def testSelectionParts = []
    if (params.TEST_SUITE && params.TEST_SUITE.trim() && params.TEST_SUITE != 'all' && params.TEST_SUITE != 'All Tests') {
        def suites = params.TEST_SUITE.split(',').collect { it.trim() }.findAll { it && it != 'all' && it != 'All Tests' }
        if (suites.size() > 0) {
            testSelectionParts.add("Suites: ${suites.join(', ')}")
        }
    }
    if (params.MARKERS && params.MARKERS.trim()) {
        def markers = params.MARKERS.split(',').collect { it.trim() }.findAll { it && it != 'All Tests' }
        if (markers.size() > 0) {
            testSelectionParts.add("Markers: ${markers.join(', ')}")
        }
    }
    def testSelectionDisplay = testSelectionParts.size() > 0 ? testSelectionParts.join('<br>') : 'All Tests'
    
    // Status configuration for template - Professional color scheme
    def statusText = actualStatus == 'SUCCESS' ? 'SUCCESS' : actualStatus == 'FAILURE' ? 'FAILURE' : 'UNSTABLE'
    def statusBarBg = actualStatus == 'SUCCESS' ? '#ecfdf5' : actualStatus == 'FAILURE' ? '#fef2f2' : '#fffbeb'
    def statusBarBorder = actualStatus == 'SUCCESS' ? '#10b981' : actualStatus == 'FAILURE' ? '#ef4444' : '#f59e0b'
    def statusTextColor = actualStatus == 'SUCCESS' ? '#047857' : actualStatus == 'FAILURE' ? '#b91c1c' : '#b45309'
    def statusDarkTextColor = actualStatus == 'SUCCESS' ? '#065f46' : actualStatus == 'FAILURE' ? '#991b1b' : '#92400e'
    
    // Format duration - remove "and counting" if present
    def durationString = currentBuild.durationString ?: 'N/A'
    if (durationString.contains('and counting')) {
        durationString = durationString.replace(' and counting', '')
    }
    
    // Build test selection display
    def testSelectionHtml = ''
    if (testSelectionParts.size() > 0) {
        def suitesHtml = ''
        def markersHtml = ''
        if (params.TEST_SUITE && params.TEST_SUITE.trim() && params.TEST_SUITE != 'all' && params.TEST_SUITE != 'All Tests') {
            def suites = params.TEST_SUITE.split(',').collect { it.trim() }.findAll { it && it != 'all' && it != 'All Tests' }
            if (suites.size() > 0) {
                suitesHtml = "<strong>Suites:</strong> ${suites.join(', ')}"
            }
        }
        if (params.MARKERS && params.MARKERS.trim()) {
            def markers = params.MARKERS.split(',').collect { it.trim() }.findAll { it && it != 'All Tests' }
            if (markers.size() > 0) {
                markersHtml = "<strong>Markers:</strong> ${markers.join(', ')}"
            }
        }
        if (suitesHtml || markersHtml) {
            testSelectionHtml = """
<!-- ================= TEST SELECTION ================= -->
<tr>
<td style="padding:0 32px 28px;background:#ffffff;">
<h3 style="margin:0 0 16px;font-size:20px;color:#1e293b;border-left:5px solid #10b981;padding-left:14px;font-weight:700;">
Test Scope
</h3>

<table width="100%" cellpadding="14" cellspacing="0" style="background:linear-gradient(135deg,#ecfdf5 0%,#d1fae5 100%);border-radius:10px;border:2px solid #10b981;font-size:14px;">
<tr>
<td style="color:#065f46;line-height:1.8;">
${suitesHtml ? suitesHtml + (markersHtml ? '<br>' : '') : ''}${markersHtml ? markersHtml : ''}
</td>
</tr>
</table>
</td>
</tr>
"""
        }
    }
    
    def body = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Dakota Marketplace | Automation Report</title>
</head>

<body style="margin:0;padding:0;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);font-family:Segoe UI, Roboto, Arial, sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td align="center" style="padding:40px 0;">

<!-- ================= MAIN CARD ================= -->
<table width="720" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 25px 50px rgba(0,0,0,0.25);">

<!-- ================= HEADER ================= -->
<tr>
<td style="background:linear-gradient(135deg,#1e40af 0%,#3b82f6 50%,#60a5fa 100%);padding:32px 32px;color:#ffffff;">
    <h1 style="margin:0;font-size:28px;font-weight:700;letter-spacing:0.3px;text-shadow:0 2px 4px rgba(0,0,0,0.2);">
        Dakota Marketplace
    </h1>
    <p style="margin:8px 0 0;font-size:15px;opacity:0.95;font-weight:400;">
        Automated Test Execution Report
    </p>
</td>
</tr>

<!-- ================= STATUS BAR ================= -->
<tr>
<td style="background:${statusBarBg};padding:18px 32px;border-bottom:1px solid ${statusBarBorder};">
    <table width="100%">
        <tr>
            <td>
                <span style="font-size:20px;font-weight:700;color:${statusDarkTextColor};">${statusText}</span>
            </td>
            <td align="right" style="font-size:14px;color:${statusDarkTextColor};">
                Pass Rate: <strong>${passPercentage}%</strong>
            </td>
        </tr>
    </table>
</td>
                    </tr>

<!-- ================= METRICS ================= -->
<tr>
<td style="padding:28px 32px;background:#f8fafc;">
<table width="100%" cellpadding="14" cellspacing="12">
<tr align="center">
<td style="background:linear-gradient(135deg,#3b82f6 0%,#2563eb 100%);color:#ffffff;border-radius:12px;box-shadow:0 4px 12px rgba(59,130,246,0.3);">
    <div style="font-size:12px;opacity:0.9;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;margin-bottom:6px;">TOTAL</div>
    <div style="font-size:32px;font-weight:800;line-height:1;">${testStats.total}</div>
</td>
<td style="background:linear-gradient(135deg,#10b981 0%,#059669 100%);color:#ffffff;border-radius:12px;box-shadow:0 4px 12px rgba(16,185,129,0.3);">
    <div style="font-size:12px;opacity:0.9;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;margin-bottom:6px;">PASSED</div>
    <div style="font-size:32px;font-weight:800;line-height:1;">${testStats.passed}</div>
</td>
<td style="background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%);color:#ffffff;border-radius:12px;box-shadow:0 4px 12px rgba(239,68,68,0.3);">
    <div style="font-size:12px;opacity:0.9;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;margin-bottom:6px;">FAILED</div>
    <div style="font-size:32px;font-weight:800;line-height:1;">${testStats.failed}</div>
</td>
<td style="background:linear-gradient(135deg,#8b5cf6 0%,#7c3aed 100%);color:#ffffff;border-radius:12px;box-shadow:0 4px 12px rgba(139,92,246,0.3);">
    <div style="font-size:12px;opacity:0.9;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;margin-bottom:6px;">SKIPPED</div>
    <div style="font-size:32px;font-weight:800;line-height:1;">${testStats.skipped}</div>
</td>
</tr>
</table>
</td>
                    </tr>

<!-- ================= BUILD DETAILS ================= -->
<tr>
<td style="padding:0 32px 28px;background:#ffffff;">
<h3 style="margin:0 0 16px;font-size:20px;color:#1e293b;border-left:5px solid #3b82f6;padding-left:14px;font-weight:700;">
Build Information
</h3>

<table width="100%" cellpadding="12" cellspacing="0" style="font-size:14px;background:#f8fafc;border-radius:10px;padding:16px;">
<tr style="border-bottom:1px solid #e2e8f0;"><td width="35%" style="color:#64748b;font-weight:600;padding:10px 0;"><strong>Build #</strong></td><td style="color:#1e293b;font-weight:600;padding:10px 0;">${env.BUILD_NUMBER}</td></tr>
<tr style="border-bottom:1px solid #e2e8f0;"><td style="color:#64748b;font-weight:600;padding:10px 0;"><strong>Environment</strong></td><td style="color:#1e293b;font-weight:600;padding:10px 0;">${ENV.toUpperCase()}</td></tr>
<tr style="border-bottom:1px solid #e2e8f0;"><td style="color:#64748b;font-weight:600;padding:10px 0;"><strong>Duration</strong></td><td style="color:#1e293b;font-weight:600;padding:10px 0;">${durationString}</td></tr>
<tr><td style="color:#64748b;font-weight:600;padding:10px 0;"><strong>Triggered By</strong></td><td style="color:#1e293b;font-weight:600;padding:10px 0;">${triggeredBy}</td></tr>
</table>
</td>
                    </tr>

${testSelectionHtml}

<!-- ================= FOOTER ================= -->
<tr>
<td style="background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);color:#cbd5e1;padding:24px 32px;font-size:13px;border-top:1px solid rgba(255,255,255,0.1);">
<p style="margin:0;line-height:1.8;">
Automated by <strong style="color:#ffffff;font-weight:700;">Jenkins CI/CD</strong><br>
<span style="color:#94a3b8;">Dakota Marketplace Test Framework</span>
</p>
</td>
                    </tr>

</table>
<!-- ================= END CARD ================= -->

</td>
                    </tr>
                </table>

</body>
</html>
    """
    
    emailext(
        subject: subject,
        body: body,
        mimeType: 'text/html',
        to: "${EMAIL_RECIPIENT}",
        attachLog: true,
        compressLog: true
    )
}

