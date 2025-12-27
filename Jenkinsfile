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
            description: 'Select test suite to run'
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
                    echo "Running test suite: ${params.TEST_SUITE}"
                    echo "Environment: ${ENV}"
                    
                    def testPath = getTestPath(params.TEST_SUITE)
                    def testCommand = "\"%PYTHON_EXE%\" -m pytest ${testPath} --html=\"%HTML_REPORT%\" --self-contained-html --alluredir=\"%ALLURE_RESULTS%\" -v --tb=short"
                    
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
                currentBuild.description = """
                    Environment: ${ENV} | 
                    Suite: ${params.TEST_SUITE} | 
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
        
        // Extract test statistics from HTML report
        def totalMatch = reportContent =~ /(\d+)\s+passed/
        if (totalMatch) {
            stats.passed = totalMatch[0][1].toInteger()
        }
        
        def failedMatch = reportContent =~ /(\d+)\s+failed/
        if (failedMatch) {
            stats.failed = failedMatch[0][1].toInteger()
        }
        
        def skippedMatch = reportContent =~ /(\d+)\s+skipped/
        if (skippedMatch) {
            stats.skipped = skippedMatch[0][1].toInteger()
        }
        
        stats.total = stats.passed + stats.failed + stats.skipped
    } catch (Exception e) {
        // File doesn't exist or couldn't be read - return default stats
        echo "Could not parse test statistics: ${e.getMessage()}"
    }
    
    return stats
}

// Email notification function
def sendEmailNotification(buildStatus) {
    def testStats = getTestStatistics()
    def statusColor = buildStatus == 'SUCCESS' ? '#28a745' : buildStatus == 'FAILURE' ? '#dc3545' : '#ffc107'
    def statusIcon = buildStatus == 'SUCCESS' ? '[SUCCESS]' : buildStatus == 'FAILURE' ? '[FAILURE]' : '[UNSTABLE]'
    
    def subject = "${statusIcon} Dakota Marketplace Tests - ${buildStatus} - Build #${env.BUILD_NUMBER}"
    
    def body = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 30px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            margin: -30px -30px 30px -30px;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            margin-top: 10px;
            background-color: ${statusColor};
            color: white;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        .info-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }
        .info-card h3 {
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .info-card .value {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .test-results {
            margin: 30px 0;
        }
        .test-results h2 {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .stats-container {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .stat-box {
            text-align: center;
            padding: 20px;
            border-radius: 8px;
            min-width: 120px;
            margin: 10px;
        }
        .stat-box.passed {
            background-color: #d4edda;
            border: 2px solid #28a745;
        }
        .stat-box.failed {
            background-color: #f8d7da;
            border: 2px solid #dc3545;
        }
        .stat-box.skipped {
            background-color: #fff3cd;
            border: 2px solid #ffc107;
        }
        .stat-box.total {
            background-color: #e7f3ff;
            border: 2px solid #007bff;
        }
        .stat-number {
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
        }
        .links {
            margin: 30px 0;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 6px;
        }
        .links a {
            display: inline-block;
            margin: 10px 10px 10px 0;
            padding: 12px 24px;
            background-color: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        .links a:hover {
            background-color: #5568d3;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
        .build-info {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
        }
        .build-info table {
            width: 100%;
            border-collapse: collapse;
        }
        .build-info td {
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        .build-info td:first-child {
            font-weight: bold;
            width: 40%;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Dakota Marketplace Test Automation</h1>
            <div class="status-badge">${buildStatus}</div>
        </div>
        
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
                <h3>Test Suite</h3>
                <div class="value">${params.TEST_SUITE.toUpperCase()}</div>
            </div>
        </div>
        
        <div class="test-results">
            <h2>Test Results Summary</h2>
            <div class="stats-container">
                <div class="stat-box total">
                    <div class="stat-number" style="color: #007bff;">${testStats.total}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat-box passed">
                    <div class="stat-number" style="color: #28a745;">${testStats.passed}</div>
                    <div class="stat-label">Passed</div>
                </div>
                <div class="stat-box failed">
                    <div class="stat-number" style="color: #dc3545;">${testStats.failed}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-box skipped">
                    <div class="stat-number" style="color: #ffc107;">${testStats.skipped}</div>
                    <div class="stat-label">Skipped</div>
                </div>
            </div>
        </div>
        
        <div class="build-info">
            <h3 style="margin-top: 0;">Build Information</h3>
            <table>
                <tr>
                    <td>Branch:</td>
                    <td>${env.BRANCH_NAME ?: 'N/A'}</td>
                </tr>
                <tr>
                    <td>Commit:</td>
                    <td>${env.GIT_COMMIT.take(7) ?: 'N/A'}</td>
                </tr>
                <tr>
                    <td>Build Duration:</td>
                    <td>${currentBuild.durationString ?: 'N/A'}</td>
                </tr>
                <tr>
                    <td>Build Time:</td>
                    <td>${new Date().format("yyyy-MM-dd HH:mm:ss")}</td>
                </tr>
                <tr>
                    <td>Triggered By:</td>
                    <td>${env.BUILD_USER_ID ?: 'System'}</td>
                </tr>
            </table>
        </div>
        
        <div class="links">
            <h3 style="margin-top: 0;">Quick Links</h3>
            <a href="${env.BUILD_URL}">View Build Details</a>
            <a href="${env.BUILD_URL}HTML_Report/">View HTML Report</a>
            <a href="${env.BUILD_URL}allure/">View Allure Report</a>
            <a href="${env.JOB_URL}">View Job Dashboard</a>
        </div>
        
        <div class="footer">
            <p>This is an automated email from Jenkins CI/CD Pipeline</p>
            <p>Dakota Marketplace Test Automation Framework</p>
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

