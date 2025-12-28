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
            description: 'Select test environment'
        )
        extendedChoice(
            name: 'TEST_SUITE',
            type: 'PT_MULTI_SELECT',
            value: 'all,column_names,fields_comparison,fields_display,lazy_loading,list_view_crud,pin_unpin',
            description: 'Select one or more test suites to run. Hold Ctrl/Cmd to select multiple. If MARKERS are also selected, tests will be filtered by both suite and markers.',
            multiSelectDelimiter: ','
        )
        extendedChoice(
            name: 'MARKERS',
            type: 'PT_MULTI_SELECT',
            value: 'accounts,contact,all_documents,filings_13f_investments_search,accounts_default,contact_default,investment_allocator_accounts_default,investment_allocator_contacts_default,investment_firm_contacts_default,my_accounts_default,portfolio_companies_contacts_default,university_alumni_contacts_default,conference_search,consultant_reviews,continuation_vehicle,dakota_city_guides,dakota_searches,dakota_video_search,fee_schedules_dashboard,fund_family_memos,fund_launches,investment_allocator_accounts,investment_allocator_contacts,investment_firm_accounts,investment_firm_contacts,manager_presentation_dashboard,my_accounts,pension_documents,portfolio_companies,portfolio_companies_contacts,private_fund_search,public_company_search,public_investments_search,public_plan_minutes_search,recent_transactions,university_alumni_contacts,column_names,fields_comparison,fields_display,lazy_loading,list_view_crud,pin_unpin',
            description: 'Select one or more markers (tabs or suites) to run. Hold Ctrl/Cmd to select multiple. Selected markers use OR logic. If TEST_SUITE is also selected, both will be combined.',
            multiSelectDelimiter: ','
        )
        booleanParam(
            name: 'SEND_EMAIL',
            defaultValue: true,
            description: 'Send email notification after build'
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
                    bat """
                        set ENV=${ENV}
                        ${testCommand}
                    """
                    
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
                    
                    // Check test results and set build status accordingly
                    def testStats = getTestStatistics()
                    if (testStats.total > 0 && testStats.failed == 0 && testStats.passed > 0) {
                        echo "All tests passed! Setting build status to SUCCESS."
                        currentBuild.result = 'SUCCESS'
                    } else if (testStats.failed > 0) {
                        echo "Some tests failed. Build status will be FAILURE."
                        currentBuild.result = 'FAILURE'
                    }
                    
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
                
                // Update build description
                def testSelectionParts = []
                if (params.TEST_SUITE && params.TEST_SUITE.trim() && params.TEST_SUITE != 'all') {
                    def suites = params.TEST_SUITE.split(',').collect { it.trim() }.findAll { it && it != 'all' }
                    if (suites.size() > 0) {
                        testSelectionParts.add("Suites: ${suites.join(', ')}")
                    }
                }
                if (params.MARKERS && params.MARKERS.trim()) {
                    def markers = params.MARKERS.split(',').collect { it.trim() }.findAll { it }
                    if (markers.size() > 0) {
                        testSelectionParts.add("Markers: ${markers.join(', ')}")
                    }
                }
                def testSelection = testSelectionParts.size() > 0 ? testSelectionParts.join(' | ') : "All Tests"
                
                currentBuild.description = """
                    Environment: ${ENV} | 
                    ${testSelection} | 
                    Tests: ${testStats.total} | 
                    Passed: ${testStats.passed} | 
                    Failed: ${testStats.failed} | 
                    Duration: ${currentBuild.durationString}
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
                echo "Build unstable!"
                if (params.SEND_EMAIL) {
                    sendEmailNotification('UNSTABLE')
                }
            }
        }
    }
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
            if (trimmed && trimmed != 'all') {
                suitesList.add(trimmed)
            }
        }
    }
    def hasSuite = suitesList.size() > 0
    
    // Parse multiple markers (extendedChoice returns comma-separated string)
    def markersList = []
    if (markers && markers.trim()) {
        markers.split(',').each { marker ->
            def trimmed = marker.trim()
            if (trimmed) {
                markersList.add(trimmed)
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
    
    def statusColor = buildStatus == 'SUCCESS' ? '#28a745' : buildStatus == 'FAILURE' ? '#dc3545' : '#ffc107'
    def statusIcon = buildStatus == 'SUCCESS' ? '[PASS]' : buildStatus == 'FAILURE' ? '[FAIL]' : '[WARN]'
    
    def subject = "${statusIcon} Dakota Marketplace Tests - ${buildStatus} - Build #${env.BUILD_NUMBER}"
    
    // Calculate pass percentage for progress bar
    def passPercentage = testStats.total > 0 ? (testStats.passed * 100 / testStats.total).intValue() : 0
    def failPercentage = testStats.total > 0 ? (testStats.failed * 100 / testStats.total).intValue() : 0
    def skipPercentage = testStats.total > 0 ? (testStats.skipped * 100 / testStats.total).intValue() : 0
    
    // Build test selection string for email
    def testSelectionParts = []
    if (params.TEST_SUITE && params.TEST_SUITE.trim() && params.TEST_SUITE != 'all') {
        def suites = params.TEST_SUITE.split(',').collect { it.trim() }.findAll { it && it != 'all' }
        if (suites.size() > 0) {
            testSelectionParts.add("Suites: ${suites.join(', ')}")
        }
    }
    if (params.MARKERS && params.MARKERS.trim()) {
        def markers = params.MARKERS.split(',').collect { it.trim() }.findAll { it }
        if (markers.size() > 0) {
            testSelectionParts.add("Markers: ${markers.join(', ')}")
        }
    }
    def testSelectionDisplay = testSelectionParts.size() > 0 ? testSelectionParts.join('<br>') : 'All Tests'
    
    // Status configuration for template
    def statusText = buildStatus == 'SUCCESS' ? 'SUCCESS' : buildStatus == 'FAILURE' ? 'FAILURE' : 'UNSTABLE'
    def statusBarBg = buildStatus == 'SUCCESS' ? '#d1fae5' : buildStatus == 'FAILURE' ? '#fee2e2' : '#fef3c7'
    def statusBarBorder = buildStatus == 'SUCCESS' ? '#86efac' : buildStatus == 'FAILURE' ? '#fca5a5' : '#fde68a'
    def statusTextColor = buildStatus == 'SUCCESS' ? '#14532d' : buildStatus == 'FAILURE' ? '#991b1b' : '#92400e'
    def statusDarkTextColor = buildStatus == 'SUCCESS' ? '#065f46' : buildStatus == 'FAILURE' ? '#7f1d1d' : '#78350f'
    
    // Build test selection display
    def testSelectionHtml = ''
    if (testSelectionParts.size() > 0) {
        def suitesHtml = ''
        def markersHtml = ''
        if (params.TEST_SUITE && params.TEST_SUITE.trim() && params.TEST_SUITE != 'all') {
            def suites = params.TEST_SUITE.split(',').collect { it.trim() }.findAll { it && it != 'all' }
            if (suites.size() > 0) {
                suitesHtml = "<strong>Suites:</strong> ${suites.join(', ')}"
            }
        }
        if (params.MARKERS && params.MARKERS.trim()) {
            def markers = params.MARKERS.split(',').collect { it.trim() }.findAll { it }
            if (markers.size() > 0) {
                markersHtml = "<strong>Markers:</strong> ${markers.join(', ')}"
            }
        }
        if (suitesHtml || markersHtml) {
            testSelectionHtml = """
<!-- ================= TEST SELECTION ================= -->
<tr>
<td style="padding:0 32px 28px;">
<h3 style="margin:0 0 12px;font-size:18px;color:#0f172a;border-left:4px solid #16a34a;padding-left:10px;">
Test Scope
</h3>

<table width="100%" cellpadding="10" cellspacing="0" style="background:#f8fafc;border-radius:8px;font-size:14px;">
<tr>
<td>
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

<body style="margin:0;padding:0;background:#0f172a;font-family:Segoe UI, Roboto, Arial, sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td align="center" style="padding:40px 0;">

<!-- ================= MAIN CARD ================= -->
<table width="720" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 20px 45px rgba(0,0,0,0.35);">

<!-- ================= HEADER ================= -->
<tr>
<td style="background:linear-gradient(135deg,#0f172a,#1e293b);padding:28px 32px;color:#ffffff;">
    <h1 style="margin:0;font-size:26px;font-weight:600;letter-spacing:0.3px;">
        Dakota Marketplace
    </h1>
    <p style="margin:6px 0 0;font-size:14px;opacity:0.85;">
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
                <span style="font-size:20px;font-weight:700;color:${statusDarkTextColor};">${statusIcon} ${statusText}</span>
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
<td style="padding:28px 32px;">
<table width="100%" cellpadding="12" cellspacing="0">
<tr align="center">
<td style="background:#0f172a;color:#ffffff;border-radius:10px;">
    <div style="font-size:13px;opacity:0.8;">TOTAL</div>
    <div style="font-size:26px;font-weight:700;">${testStats.total}</div>
</td>
<td style="background:#dcfce7;color:#14532d;border-radius:10px;">
    <div style="font-size:13px;">PASSED</div>
    <div style="font-size:26px;font-weight:700;">${testStats.passed}</div>
</td>
<td style="background:#fee2e2;color:#7f1d1d;border-radius:10px;">
    <div style="font-size:13px;">FAILED</div>
    <div style="font-size:26px;font-weight:700;">${testStats.failed}</div>
</td>
<td style="background:#f1f5f9;color:#334155;border-radius:10px;">
    <div style="font-size:13px;">SKIPPED</div>
    <div style="font-size:26px;font-weight:700;">${testStats.skipped}</div>
</td>
</tr>
</table>
</td>
</tr>

<!-- ================= BUILD DETAILS ================= -->
<tr>
<td style="padding:0 32px 28px;">
<h3 style="margin:0 0 12px;font-size:18px;color:#0f172a;border-left:4px solid #2563eb;padding-left:10px;">
Build Information
</h3>

<table width="100%" cellpadding="8" cellspacing="0" style="font-size:14px;color:#334155;">
<tr><td width="35%"><strong>Build #</strong></td><td>${env.BUILD_NUMBER}</td></tr>
<tr><td><strong>Environment</strong></td><td>${ENV.toUpperCase()}</td></tr>
<tr><td><strong>Branch</strong></td><td>${env.BRANCH_NAME ?: 'N/A'}</td></tr>
<tr><td><strong>Commit</strong></td><td>${env.GIT_COMMIT.take(7) ?: 'N/A'}</td></tr>
<tr><td><strong>Duration</strong></td><td>${currentBuild.durationString ?: 'N/A'}</td></tr>
<tr><td><strong>Triggered By</strong></td><td>${triggeredBy}</td></tr>
</table>
</td>
</tr>

${testSelectionHtml}

<!-- ================= ACTION BUTTONS ================= -->
<tr>
<td style="padding:0 32px 32px;">
<table width="100%" cellpadding="12" cellspacing="0">
<tr>
<td align="center" style="background:#2563eb;border-radius:8px;">
<a href="${env.BUILD_URL}" style="color:#ffffff;text-decoration:none;font-weight:600;">
View Jenkins Build
</a>
</td>
<td align="center" style="background:#0f172a;border-radius:8px;">
<a href="${env.BUILD_URL}HTML_Report/" style="color:#ffffff;text-decoration:none;font-weight:600;">
HTML Report
</a>
</td>
<td align="center" style="background:#16a34a;border-radius:8px;">
<a href="${env.BUILD_URL}allure/" style="color:#ffffff;text-decoration:none;font-weight:600;">
Allure Report
</a>
</td>
</tr>
</table>
</td>
</tr>

<!-- ================= FOOTER ================= -->
<tr>
<td style="background:#020617;color:#94a3b8;padding:18px 32px;font-size:12px;">
<p style="margin:0;">
Automated by <strong>Jenkins CI/CD</strong><br>
Dakota Marketplace Test Framework
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

