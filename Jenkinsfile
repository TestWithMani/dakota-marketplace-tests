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
    def statusIcon = buildStatus == 'SUCCESS' ? '[SUCCESS]' : buildStatus == 'FAILURE' ? '[FAILURE]' : '[UNSTABLE]'
    
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
    
    def body = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            padding: 20px 10px;
            line-height: 1.6;
            color: #1a1a1a;
            -webkit-font-smoothing: antialiased;
        }
        .container {
            max-width: 580px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .header {
            background: ${statusColor};
            color: #fff;
            padding: 24px 20px;
            text-align: center;
        }
        .header-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 4px;
            letter-spacing: -0.3px;
        }
        .header-subtitle {
            font-size: 12px;
            opacity: 0.95;
            font-weight: 400;
        }
        .status-indicator {
            display: inline-block;
            margin-top: 12px;
            padding: 4px 12px;
            background: rgba(255,255,255,0.2);
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .content {
            padding: 20px;
        }
        .stats-row {
            display: table;
            width: 100%;
            table-layout: fixed;
            margin-bottom: 20px;
            border-collapse: separate;
            border-spacing: 8px;
        }
        .stat-box {
            display: table-cell;
            text-align: center;
            padding: 16px 8px;
            background: #f8f9fa;
            border-radius: 6px;
            vertical-align: top;
        }
        .stat-number {
            font-size: 28px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 6px;
        }
        .stat-label {
            font-size: 11px;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .stat-box.total .stat-number { color: #2563eb; }
        .stat-box.passed .stat-number { color: #16a34a; }
        .stat-box.failed .stat-number { color: #dc2626; }
        .stat-box.skipped .stat-number { color: #ca8a04; }
        .progress-wrapper {
            margin: 20px 0;
            padding: 16px;
            background: #f8f9fa;
            border-radius: 6px;
        }
        .progress-title {
            font-size: 12px;
            font-weight: 600;
            color: #4b5563;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .progress-bar {
            height: 6px;
            background: #e5e7eb;
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 8px;
        }
        .progress-fill {
            height: 100%;
            border-radius: 3px;
            display: inline-block;
        }
        .progress-fill.passed { background: #16a34a; }
        .progress-fill.failed { background: #dc2626; }
        .progress-fill.skipped { background: #ca8a04; }
        .progress-text {
            font-size: 11px;
            color: #6b7280;
            display: flex;
            justify-content: space-between;
        }
        .info-section {
            margin: 20px 0;
            padding: 16px;
            background: #f8f9fa;
            border-radius: 6px;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e5e7eb;
            font-size: 13px;
        }
        .info-row:last-child { border-bottom: none; }
        .info-label {
            color: #6b7280;
            font-weight: 500;
        }
        .info-value {
            color: #1a1a1a;
            font-weight: 600;
            text-align: right;
        }
        .code {
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        .actions {
            margin: 20px 0;
            display: table;
            width: 100%;
            table-layout: fixed;
            border-collapse: separate;
            border-spacing: 8px;
        }
        .btn {
            display: table-cell;
            padding: 10px 12px;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            font-size: 12px;
            font-weight: 600;
            color: #fff;
        }
        .btn-primary {
            background: #2563eb;
        }
        .btn-secondary {
            background: #6b7280;
        }
        .footer {
            padding: 16px 20px;
            background: #f8f9fa;
            text-align: center;
            border-top: 1px solid #e5e7eb;
        }
        .footer-text {
            font-size: 11px;
            color: #6b7280;
            line-height: 1.5;
        }
        .footer-brand {
            font-weight: 600;
            color: #4b5563;
            margin-top: 4px;
        }
        @media only screen and (max-width: 600px) {
            .stats-row, .actions { display: block; }
            .stat-box, .btn {
                display: block;
                width: 100%;
                margin-bottom: 8px;
            }
            .content { padding: 16px; }
            .header { padding: 20px 16px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-title">Dakota Marketplace</div>
            <div class="header-subtitle">Test Automation Report</div>
            <div class="status-indicator">${buildStatus}</div>
        </div>
        
        <div class="content">
            <div class="stats-row">
                <div class="stat-box total">
                    <div class="stat-number">${testStats.total}</div>
                    <div class="stat-label">Total</div>
                </div>
                <div class="stat-box passed">
                    <div class="stat-number">${testStats.passed}</div>
                    <div class="stat-label">Passed</div>
                </div>
                <div class="stat-box failed">
                    <div class="stat-number">${testStats.failed}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-box skipped">
                    <div class="stat-number">${testStats.skipped}</div>
                    <div class="stat-label">Skipped</div>
                </div>
            </div>
            
            ${testStats.total > 0 ? """
            <div class="progress-wrapper">
                <div class="progress-title">Test Results</div>
                <div class="progress-bar">
                    ${testStats.passed > 0 ? "<span class=\"progress-fill passed\" style=\"width: ${passPercentage}%;\"></span>" : ""}
                    ${testStats.failed > 0 ? "<span class=\"progress-fill failed\" style=\"width: ${failPercentage}%;\"></span>" : ""}
                    ${testStats.skipped > 0 ? "<span class=\"progress-fill skipped\" style=\"width: ${skipPercentage}%;\"></span>" : ""}
                </div>
                <div class="progress-text">
                    <span>Pass Rate: ${passPercentage}%</span>
                    <span>${testStats.failed > 0 ? "Fail: ${failPercentage}%" : "All Passed ✓"}</span>
                </div>
            </div>
            """ : ""}
            
            <div class="info-section">
                <div class="info-row">
                    <span class="info-label">Build #</span>
                    <span class="info-value">${env.BUILD_NUMBER}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Environment</span>
                    <span class="info-value">${ENV.toUpperCase()}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Branch</span>
                    <span class="info-value">${env.BRANCH_NAME ?: 'N/A'}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Commit</span>
                    <span class="info-value"><span class="code">${env.GIT_COMMIT.take(7) ?: 'N/A'}</span></span>
                </div>
                <div class="info-row">
                    <span class="info-label">Duration</span>
                    <span class="info-value">${currentBuild.durationString ?: 'N/A'}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Triggered By</span>
                    <span class="info-value">${triggeredBy}</span>
                </div>
                ${testSelectionParts.size() > 0 ? """
                <div class="info-row">
                    <span class="info-label">Test Selection</span>
                    <span class="info-value" style="font-size: 11px;">${testSelectionDisplay}</span>
                </div>
                """ : ""}
            </div>
            
            <div class="actions">
                <a href="${env.BUILD_URL}" class="btn btn-primary">Build Details</a>
                <a href="${env.BUILD_URL}HTML_Report/" class="btn btn-secondary">HTML Report</a>
                <a href="${env.BUILD_URL}allure/" class="btn btn-secondary">Allure Report</a>
                <a href="${env.JOB_URL}" class="btn btn-primary">Dashboard</a>
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-text">
                Automated by Jenkins CI/CD<br>
                <span class="footer-brand">Dakota Marketplace Test Framework</span>
            </div>
        </div>
    </div>
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

