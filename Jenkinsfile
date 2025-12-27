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
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'column_names', 'fields_comparison', 'fields_display', 'lazy_loading', 'list_view_crud', 'pin_unpin'],
            description: 'Select test suite to run (ignored if MARKERS is specified)'
        )
        text(
            name: 'MARKERS',
            defaultValue: '',
            description: 'Optional: Run tests by markers (comma-separated). Examples: "accounts" (runs all 6 tests for accounts tab), "accounts,contact" (runs all tests for accounts and contact tabs), "accounts and column_names" (runs accounts column_names test only). Leave empty to use TEST_SUITE selection.'
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
                    
                    bat """
                        set ENV=${ENV}
                        ${testCommand}
                    """
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
                def testSelection = params.MARKERS && params.MARKERS.trim() ? "Markers: ${params.MARKERS}" : "Suite: ${params.TEST_SUITE}"
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
    def reportOptions = "--html=\"%HTML_REPORT%\" --self-contained-html --alluredir=\"%ALLURE_RESULTS%\" -v --tb=short"
    
    // If markers are specified, use marker selection
    if (markers && markers.trim()) {
        def markersList = markers.split(',').collect { it.trim() }.findAll { it }
        if (markersList.size() > 0) {
            // Build marker expression
            // Support both "marker1,marker2" (OR) and "marker1 and marker2" (AND) syntax
            def markerExpression = markers.trim()
            // Replace comma with "or" for OR logic, or keep "and" for AND logic
            if (!markerExpression.contains(' and ')) {
                markerExpression = markerExpression.replace(',', ' or ')
            }
            echo "Running tests with markers: ${markerExpression}"
            return "${baseCommand} -m \"${markerExpression}\" ${reportOptions}"
        }
    }
    
    // Otherwise use suite selection
    def testPath = getTestPath(testSuite)
    echo "Running test suite: ${testSuite} from path: ${testPath}"
    return "${baseCommand} ${testPath} ${reportOptions}"
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
    
    try {
        def reportPath = "reports/report.html"
        // Use readFile step instead of new File() for Jenkins script security
        // readFile will throw exception if file doesn't exist, which is handled by catch
        def reportContent = readFile(reportPath)
        
        // Try multiple patterns to extract test statistics from HTML report
        // Pattern 1: HTML format like "<span class="passed">5 Passed,</span>" (case-insensitive)
        def passedMatch = reportContent =~ /(?i)<span[^>]*class=["']passed["'][^>]*>(\d+)\s+Passed/
        if (!passedMatch) {
            // Pattern 2: Text format like "5 passed" or "5 Passed"
            passedMatch = reportContent =~ /(\d+)\s+[Pp]assed/
        }
        if (passedMatch) {
            stats.passed = passedMatch[0][1].toInteger()
        }
        
        // Extract failed count
        def failedMatch = reportContent =~ /(?i)<span[^>]*class=["']failed["'][^>]*>(\d+)\s+Failed/
        if (!failedMatch) {
            failedMatch = reportContent =~ /(\d+)\s+[Ff]ailed/
        }
        if (failedMatch) {
            stats.failed = failedMatch[0][1].toInteger()
        }
        
        // Extract skipped count
        def skippedMatch = reportContent =~ /(?i)<span[^>]*class=["']skipped["'][^>]*>(\d+)\s+Skipped/
        if (!skippedMatch) {
            skippedMatch = reportContent =~ /(\d+)\s+[Ss]kipped/
        }
        if (skippedMatch) {
            stats.skipped = skippedMatch[0][1].toInteger()
        }
        
        // Also try to extract from JSON data if available (fallback method)
        // This is more reliable as it counts actual test results
        if (stats.passed == 0 && stats.failed == 0 && stats.skipped == 0) {
            def jsonMatch = reportContent =~ /data-jsonblob="([^"]+)"/
            if (jsonMatch) {
                try {
                    def jsonStr = java.net.URLDecoder.decode(jsonMatch[0][1], "UTF-8")
                    // Count tests by status in JSON - look for result fields
                    def passedCount = (jsonStr =~ /"result"\s*:\s*"passed"/).size()
                    def failedCount = (jsonStr =~ /"result"\s*:\s*"failed"/).size()
                    def skippedCount = (jsonStr =~ /"result"\s*:\s*"skipped"/).size()
                    
                    if (passedCount > 0 || failedCount > 0 || skippedCount > 0) {
                        stats.passed = passedCount
                        stats.failed = failedCount
                        stats.skipped = skippedCount
                        echo "Extracted statistics from JSON data: Passed=${passedCount}, Failed=${failedCount}, Skipped=${skippedCount}"
                    }
                } catch (Exception jsonEx) {
                    echo "Could not parse JSON data: ${jsonEx.getMessage()}"
                }
            }
        }
        
        // Final fallback: Try to parse from console output summary format
        // Format: "5 passed, 0 failed, 0 skipped in 652.69s"
        if (stats.passed == 0 && stats.failed == 0 && stats.skipped == 0) {
            def summaryMatch = reportContent =~ /(?i)(\d+)\s+passed[,\s]+(\d+)\s+failed[,\s]+(\d+)\s+skipped/
            if (summaryMatch) {
                stats.passed = summaryMatch[0][1].toInteger()
                stats.failed = summaryMatch[0][2].toInteger()
                stats.skipped = summaryMatch[0][3].toInteger()
                echo "Extracted statistics from summary format"
            }
        }
        
        // Calculate total
        stats.total = stats.passed + stats.failed + stats.skipped
        
        // Log extracted statistics for debugging
        echo "Extracted test statistics: Total=${stats.total}, Passed=${stats.passed}, Failed=${stats.failed}, Skipped=${stats.skipped}"
        
    } catch (Exception e) {
        // File doesn't exist or couldn't be read - return default stats
        echo "Could not parse test statistics: ${e.getMessage()}"
        echo "Stack trace: ${e.getStackTrace().join('\n')}"
    }
    
    return stats
}

// Email notification function
def sendEmailNotification(buildStatus) {
    def testStats = getTestStatistics()
    def statusColor = buildStatus == 'SUCCESS' ? '#28a745' : buildStatus == 'FAILURE' ? '#dc3545' : '#ffc107'
    def statusIcon = buildStatus == 'SUCCESS' ? '[SUCCESS]' : buildStatus == 'FAILURE' ? '[FAILURE]' : '[UNSTABLE]'
    
    def subject = "${statusIcon} Dakota Marketplace Tests - ${buildStatus} - Build #${env.BUILD_NUMBER}"
    
    // Calculate pass percentage for progress bar
    def passPercentage = testStats.total > 0 ? (testStats.passed * 100 / testStats.total).intValue() : 0
    def failPercentage = testStats.total > 0 ? (testStats.failed * 100 / testStats.total).intValue() : 0
    def skipPercentage = testStats.total > 0 ? (testStats.skipped * 100 / testStats.total).intValue() : 0
    
    def body = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        .email-wrapper {
            max-width: 700px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 3s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        .header-content {
            position: relative;
            z-index: 1;
        }
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }
        .header-subtitle {
            font-size: 14px;
            opacity: 0.9;
            font-weight: 300;
        }
        .status-badge {
            display: inline-block;
            padding: 10px 24px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 13px;
            margin-top: 20px;
            background-color: ${statusColor};
            color: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .content {
            padding: 40px 30px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 35px;
        }
        .info-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .info-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        .info-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
        }
        .info-card h3 {
            font-size: 11px;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        .info-card .value {
            font-size: 24px;
            font-weight: 700;
            color: #2c3e50;
            line-height: 1.2;
        }
        .test-results-section {
            margin: 40px 0;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #e9ecef;
        }
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .section-title::before {
            content: '';
            width: 4px;
            height: 24px;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            text-align: center;
            padding: 25px 15px;
            border-radius: 12px;
            background: white;
            border: 2px solid transparent;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stat-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--stat-color);
        }
        .stat-card.total {
            --stat-color: #007bff;
            border-color: #007bff;
            background: linear-gradient(135deg, #e7f3ff 0%, #ffffff 100%);
        }
        .stat-card.passed {
            --stat-color: #28a745;
            border-color: #28a745;
            background: linear-gradient(135deg, #d4edda 0%, #ffffff 100%);
        }
        .stat-card.failed {
            --stat-color: #dc3545;
            border-color: #dc3545;
            background: linear-gradient(135deg, #f8d7da 0%, #ffffff 100%);
        }
        .stat-card.skipped {
            --stat-color: #ffc107;
            border-color: #ffc107;
            background: linear-gradient(135deg, #fff3cd 0%, #ffffff 100%);
        }
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        .stat-number {
            font-size: 42px;
            font-weight: 800;
            margin: 10px 0;
            color: var(--stat-color);
            line-height: 1;
        }
        .stat-label {
            font-size: 12px;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            margin-top: 8px;
        }
        .progress-bar-container {
            margin-top: 25px;
            background: #e9ecef;
            border-radius: 50px;
            height: 12px;
            overflow: hidden;
            position: relative;
        }
        .progress-bar {
            height: 100%;
            border-radius: 50px;
            display: flex;
            overflow: hidden;
        }
        .progress-segment {
            height: 100%;
            transition: width 0.5s ease;
        }
        .progress-segment.passed {
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        }
        .progress-segment.failed {
            background: linear-gradient(90deg, #dc3545 0%, #e83e8c 100%);
        }
        .progress-segment.skipped {
            background: linear-gradient(90deg, #ffc107 0%, #ff9800 100%);
        }
        .progress-label {
            margin-top: 12px;
            font-size: 12px;
            color: #6c757d;
            display: flex;
            justify-content: space-between;
        }
        .build-details {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 30px 0;
            border: 1px solid #e9ecef;
        }
        .build-details h3 {
            font-size: 16px;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .build-details h3::before {
            content: '';
            width: 4px;
            height: 20px;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }
        .detail-table {
            width: 100%;
            border-collapse: collapse;
        }
        .detail-table tr {
            border-bottom: 1px solid #f1f3f5;
        }
        .detail-table tr:last-child {
            border-bottom: none;
        }
        .detail-table td {
            padding: 14px 0;
            font-size: 14px;
        }
        .detail-table td:first-child {
            font-weight: 600;
            color: #6c757d;
            width: 140px;
        }
        .detail-table td:last-child {
            color: #2c3e50;
            font-weight: 500;
        }
        .action-buttons {
            margin: 35px 0;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        .action-btn {
            display: block;
            padding: 14px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        .action-btn.secondary {
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
            box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
        }
        .action-btn.secondary:hover {
            box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4);
        }
        .footer {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }
        .footer-text {
            font-size: 12px;
            color: #6c757d;
            line-height: 1.8;
        }
        .footer-brand {
            font-weight: 600;
            color: #667eea;
            margin-top: 5px;
        }
        @media only screen and (max-width: 600px) {
            .info-grid, .stats-grid, .action-buttons {
                grid-template-columns: 1fr;
            }
            .content {
                padding: 25px 20px;
            }
            .header {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="header">
            <div class="header-content">
                <h1>Dakota Marketplace</h1>
                <div class="header-subtitle">Test Automation Report</div>
                <div class="status-badge">${buildStatus}</div>
            </div>
        </div>
        
        <div class="content">
            <div class="info-grid">
                <div class="info-card">
                    <h3>Build Number</h3>
                    <div class="value">#${env.BUILD_NUMBER}</div>
                </div>
                <div class="info-card">
                    <h3>Build Status</h3>
                    <div class="value" style="color: ${statusColor};">${buildStatus}</div>
                </div>
                <div class="info-card">
                    <h3>Environment</h3>
                    <div class="value">${ENV.toUpperCase()}</div>
                </div>
                <div class="info-card">
                    <h3>Test Selection</h3>
                    <div class="value" style="font-size: 16px;">${params.MARKERS && params.MARKERS.trim() ? params.MARKERS : params.TEST_SUITE.toUpperCase()}</div>
                </div>
            </div>
            
            <div class="test-results-section">
                <div class="section-title">Test Results Summary</div>
                
                <div class="stats-grid">
                    <div class="stat-card total">
                        <div class="stat-number">${testStats.total}</div>
                        <div class="stat-label">Total Tests</div>
                    </div>
                    <div class="stat-card passed">
                        <div class="stat-number">${testStats.passed}</div>
                        <div class="stat-label">Passed</div>
                    </div>
                    <div class="stat-card failed">
                        <div class="stat-number">${testStats.failed}</div>
                        <div class="stat-label">Failed</div>
                    </div>
                    <div class="stat-card skipped">
                        <div class="stat-number">${testStats.skipped}</div>
                        <div class="stat-label">Skipped</div>
                    </div>
                </div>
                
                ${testStats.total > 0 ? """
                <div class="progress-bar-container">
                    <div class="progress-bar">
                        ${testStats.passed > 0 ? "<div class=\"progress-segment passed\" style=\"width: ${passPercentage}%;\"></div>" : ""}
                        ${testStats.failed > 0 ? "<div class=\"progress-segment failed\" style=\"width: ${failPercentage}%;\"></div>" : ""}
                        ${testStats.skipped > 0 ? "<div class=\"progress-segment skipped\" style=\"width: ${skipPercentage}%;\"></div>" : ""}
                    </div>
                    <div class="progress-label">
                        <span>Pass Rate: ${passPercentage}%</span>
                        <span>${testStats.failed > 0 ? "Fail Rate: ${failPercentage}%" : "All Tests Passed!"}</span>
                    </div>
                </div>
                """ : ""}
            </div>
            
            <div class="build-details">
                <h3>Build Information</h3>
                <table class="detail-table">
                    <tr>
                        <td>Branch</td>
                        <td>${env.BRANCH_NAME ?: 'N/A'}</td>
                    </tr>
                    <tr>
                        <td>Commit</td>
                        <td><code style="background: #f8f9fa; padding: 4px 8px; border-radius: 4px; font-family: 'Courier New', monospace;">${env.GIT_COMMIT.take(7) ?: 'N/A'}</code></td>
                    </tr>
                    <tr>
                        <td>Build Duration</td>
                        <td>${currentBuild.durationString ?: 'N/A'}</td>
                    </tr>
                    <tr>
                        <td>Build Time</td>
                        <td>${new Date().format("yyyy-MM-dd HH:mm:ss")}</td>
                    </tr>
                    <tr>
                        <td>Triggered By</td>
                        <td>${env.BUILD_USER_ID ?: 'System'}</td>
                    </tr>
                </table>
            </div>
            
            <div class="action-buttons">
                <a href="${env.BUILD_URL}" class="action-btn">View Build Details</a>
                <a href="${env.BUILD_URL}HTML_Report/" class="action-btn secondary">HTML Report</a>
                <a href="${env.BUILD_URL}allure/" class="action-btn secondary">Allure Report</a>
                <a href="${env.JOB_URL}" class="action-btn">Job Dashboard</a>
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-text">
                This is an automated email from Jenkins CI/CD Pipeline<br>
                <span class="footer-brand">Dakota Marketplace Test Automation Framework</span>
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

