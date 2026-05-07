pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
        timeout(time: 1080, unit: 'MINUTES')
    }

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['PROD', 'UAT'],
            description: 'Select the test environment to run tests against'
        )
        choice(
            name: 'PORTAL',
            choices: [
                'All Marketplace Access',
                'Dakota Ria Portal',
                'Dakota Transactions & CEOs Access',
                'FA Data Set',
                'Is Deal Team?',
                'Dakota Private Markets Access',
                'Dakota Recommends Portal Access',
                'Dakota Family Office Portal',
                'Dakota private wealth portal',
                'Dakota International portal'
            ],
            description: 'All Marketplace Access uses base uat/prod credentials (no portal suffix on ENV). Other choices set ENV to uat_<portal> / prod_<portal>.'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'Column Names Validation', 'Fields Comparison', 'Fields Display Functionality', 'Lazy Loading', 'List View CRUD Operations', 'Pin/Unpin Functionality'],
            description: 'Select one test suite. Use "all" to run all suites.'
        )
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'edge', 'firefox'],
            description: 'Browser used for Selenium execution.'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run browser in headless mode.'
        )
        string(
            name: 'BROWSER_WIDTH',
            defaultValue: '1920',
            description: 'Browser viewport width in pixels.'
        )
        string(
            name: 'BROWSER_HEIGHT',
            defaultValue: '1080',
            description: 'Browser viewport height in pixels.'
        )
        string(
            name: 'PARALLEL_WORKERS',
            defaultValue: '1',
            description: "Pytest xdist workers. Use '1' to disable parallel mode, integer >1, or 'auto'."
        )
        string(
            name: 'NON_ASSERTION_RETRY_COUNT',
            defaultValue: '1',
            description: "Retry attempts for non-assertion pytest failures (0 disables selective retry)."
        )
        booleanParam(
            name: 'RUN_ALLURE',
            defaultValue: true,
            description: 'Generate and publish Allure report in Jenkins.'
        )
        booleanParam(
            name: 'RESET_WORKSPACE_AND_ALLURE_HISTORY',
            defaultValue: false,
            description: 'If true, clears workspace report folders and local Allure results before running tests.'
        )
        booleanParam(
            name: 'SEND_EMAIL',
            defaultValue: true,
            description: 'Send email notification after build completion'
        )
        text(
            name: 'ADDITIONAL_EMAILS',
            defaultValue: '',
            description: 'Additional recipients (comma-separated).'
        )
        string(
            name: 'DEFAULT_EMAIL',
            defaultValue: 'usman.arshad@rolustech.com',
            description: 'Primary recipient.'
        )
        text(
            name: 'TAB_SELECTION_HELP',
            defaultValue: 'Select one or more TAB_* checkboxes below to filter tests by tabs.\nIf none are selected, no tab marker filter is applied.',
            description: 'Read-only help text for tab selection.'
        )
        booleanParam(name: 'TAB_ALL_MARKETPLACE_ACCESS', defaultValue: false, description: 'All Marketplace Access')
        booleanParam(name: 'TAB_ACCOUNTS', defaultValue: false, description: 'Accounts Tab')
        booleanParam(name: 'TAB_CONTACT', defaultValue: false, description: 'Contact Tab')
        booleanParam(name: 'TAB_ALL_DOCUMENTS', defaultValue: false, description: 'All Documents')
        booleanParam(name: 'TAB_13F_FILINGS_INVESTMENTS_SEARCH', defaultValue: false, description: '13F Filings & Investments Search')
        booleanParam(name: 'TAB_BENCHMARKING', defaultValue: false, description: 'Benchmarking Tab')
        booleanParam(name: 'TAB_CONFERENCE_SEARCH', defaultValue: false, description: 'Conference Search')
        booleanParam(name: 'TAB_CONSULTANT_REVIEWS', defaultValue: false, description: 'Consultant Reviews')
        booleanParam(name: 'TAB_CONTINUATION_VEHICLE', defaultValue: false, description: 'Continuation Vehicle')
        booleanParam(name: 'TAB_DAKOTA_CITY_GUIDES', defaultValue: false, description: 'Dakota City Guides')
        booleanParam(name: 'TAB_DAKOTA_SEARCHES', defaultValue: false, description: 'Dakota Searches')
        booleanParam(name: 'TAB_DAKOTA_VIDEO_SEARCH', defaultValue: false, description: 'Dakota Video Search')
        booleanParam(name: 'TAB_EVERGREEN_FUND_PERFORMANCE', defaultValue: false, description: 'Evergreen Fund Performance')
        booleanParam(name: 'TAB_FEE_SCHEDULES_DASHBOARD', defaultValue: false, description: 'Fee Schedules Dashboard')
        booleanParam(name: 'TAB_FORECASTED_TRANSACTIONS', defaultValue: false, description: 'Forecasted Transactions')
        booleanParam(name: 'TAB_FUND_FAMILY_MEMOS', defaultValue: false, description: 'Fund Family Memos')
        booleanParam(name: 'TAB_FUND_LAUNCHES', defaultValue: false, description: 'Fund Launches')
        booleanParam(name: 'TAB_FUNDRAISING_NEWS', defaultValue: false, description: 'Fundraising News')
        booleanParam(name: 'TAB_HEDGE_FUND_PERFORMANCE', defaultValue: false, description: 'Hedge Fund Performance')
        booleanParam(name: 'TAB_INVESTMENT_ALLOCATOR_ACCOUNTS', defaultValue: false, description: 'Investment Allocator - Accounts')
        booleanParam(name: 'TAB_INVESTMENT_ALLOCATOR_CONTACTS', defaultValue: false, description: 'Investment Allocator - Contacts')
        booleanParam(name: 'TAB_INVESTMENT_FIRM_ACCOUNTS', defaultValue: false, description: 'Investment Firm - Accounts')
        booleanParam(name: 'TAB_INVESTMENT_FIRM_CONTACTS', defaultValue: false, description: 'Investment Firm - Contacts')
        booleanParam(name: 'TAB_MANAGER_PRESENTATION_DASHBOARD', defaultValue: false, description: 'Manager Presentation Dashboard')
        booleanParam(name: 'TAB_MY_ACCOUNTS', defaultValue: false, description: 'My Accounts')
        booleanParam(name: 'TAB_PENSION_DOCUMENTS', defaultValue: false, description: 'Pension Documents')
        booleanParam(name: 'TAB_PORTFOLIO_COMPANIES', defaultValue: false, description: 'Portfolio Companies')
        booleanParam(name: 'TAB_PORTFOLIO_COMPANIES_CONTACTS', defaultValue: false, description: 'Portfolio Companies - Contacts')
        booleanParam(name: 'TAB_PRIVATE_COMPANIES_TRANSACTIONS', defaultValue: false, description: 'Private Companies Transactions')
        booleanParam(name: 'TAB_PRIVATE_FUND_SEARCH', defaultValue: false, description: 'Private Fund Search')
        booleanParam(name: 'TAB_PUBLIC_COMPANY_SEARCH', defaultValue: false, description: 'Public Company Search')
        booleanParam(name: 'TAB_PUBLIC_INVESTMENTS_SEARCH', defaultValue: false, description: 'Public Investments Search')
        booleanParam(name: 'TAB_PUBLIC_PLAN_MINUTES_SEARCH', defaultValue: false, description: 'Public Plan Minutes Search')
        booleanParam(name: 'TAB_RECENT_TRANSACTIONS', defaultValue: false, description: 'Recent Transactions')
        booleanParam(name: 'TAB_UNIVERSITY_ALUMNI_CONTACTS', defaultValue: false, description: 'University Alumni - Contacts')
    }

    environment {
        VENV_DIR = '.venv-jenkins'
        PYTEST_JUNIT = 'reports/junit.xml'
        PYTEST_HTML = 'reports/report.html'
        PYTEST_JSON = 'reports/report.json'
        ALLURE_DIR = 'allure-results'
        EMAIL_RECIPIENT = 'usman.arshad@rolustech.com'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                    def shortCommit = env.GIT_COMMIT ? env.GIT_COMMIT.take(7) : 'N/A'
                    echo "Branch: ${env.BRANCH_NAME ?: 'N/A'} | Commit: ${shortCommit}"
                }
            }
        }

        stage('Reset Workspace Reports (Optional)') {
            when {
                expression { return params.RESET_WORKSPACE_AND_ALLURE_HISTORY as boolean }
            }
            steps {
                script {
                    echo "RESET_WORKSPACE_AND_ALLURE_HISTORY=true -> clearing workspace reports and local Allure results."

                    // Clean workspace-level report directories/files so Allure starts from fresh results only.
                    clearReportDirectories()

                    // Build history deletion is intentionally skipped to avoid Jenkins Script Security failures.
                    echo "Skipping Jenkins build history deletion in pipeline script. Use a trusted admin-maintained cleanup job if needed."
                }
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    def envName = (params.ENVIRONMENT ?: 'UAT').toLowerCase()
                    def portalName = params.PORTAL ?: 'All Marketplace Access'
                    def portalKey = getPortalMap()[portalName] ?: ''
                    env.TEST_ENV = portalKey ? "${envName}_${portalKey}" : envName
                    echo "Environment configured: ${env.TEST_ENV}"
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    setupPythonEnvironment()
                }
            }
        }

        stage('Prepare Report Directories') {
            steps {
                script {
                    clearReportDirectories()
                }
            }
        }

        stage('Static Validation') {
            steps {
                script {
                    validateRuntimeParameters(
                        params.TEST_SUITE as String,
                        params.BROWSER as String,
                        params.PARALLEL_WORKERS as String,
                        params.NON_ASSERTION_RETRY_COUNT as String,
                        params.BROWSER_WIDTH as String,
                        params.BROWSER_HEIGHT as String
                    )
                    def selectedPaths = resolveSelectedTestPaths(params.TEST_SUITE as String)
                    def markerExpr = resolveTabsExpression(params)
                    echo "Selected marker expression: ${markerExpr ?: 'none'}"
                    def collectCmd = buildPytestCommand(
                        selectedPaths,
                        markerExpr,
                        false,
                        true,
                        params.BROWSER as String,
                        params.PARALLEL_WORKERS as String,
                        params.NON_ASSERTION_RETRY_COUNT as String
                    )
                    runPytest('--version')
                    runPytest(collectCmd)
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def selectedPaths = resolveSelectedTestPaths(params.TEST_SUITE as String)
                    def markerExpr = resolveTabsExpression(params)
                    echo "Selected marker expression: ${markerExpr ?: 'none'}"
                    def runCmd = buildPytestCommand(
                        selectedPaths,
                        markerExpr,
                        params.RUN_ALLURE as boolean,
                        false,
                        params.BROWSER as String,
                        params.PARALLEL_WORKERS as String,
                        params.NON_ASSERTION_RETRY_COUNT as String
                    )
                    echo "Pytest command: pytest ${runCmd}"

                    withEnv([
                        "TEST_ENV=${env.TEST_ENV}",
                        "BROWSER=${(params.BROWSER ?: 'chrome').trim().toLowerCase()}",
                        "HEADLESS=${params.HEADLESS as boolean}",
                        "BROWSER_WIDTH=${(params.BROWSER_WIDTH ?: '1920').trim()}",
                        "BROWSER_HEIGHT=${(params.BROWSER_HEIGHT ?: '1080').trim()}"
                    ]) {
                        catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                            runPytest(runCmd)
                        }
                    }
                }
            }
        }

        stage('Publish Reports') {
            steps {
                script {
                    if (fileExists(env.PYTEST_JUNIT)) {
                        junit allowEmptyResults: true, testResults: env.PYTEST_JUNIT
                    }

                    try {
                        publishHTML(target: [
                            reportName: 'Pytest HTML Report',
                            reportDir: 'reports',
                            reportFiles: 'report.html',
                            keepAll: true,
                            alwaysLinkToLastBuild: true,
                            allowMissing: true
                        ])
                    } catch (Exception ex) {
                        echo "HTML Publisher not available or failed: ${ex.getMessage()}"
                    }

                    if (params.RUN_ALLURE && fileExists(env.ALLURE_DIR)) {
                        try {
                            allure([
                                includeProperties: false,
                                jdk: '',
                                properties: [],
                                reportBuildPolicy: 'ALWAYS',
                                results: [[path: env.ALLURE_DIR]],
                                reportName: 'Allure Report'
                            ])
                        } catch (MissingMethodException ex) {
                            echo "Allure plugin not installed; skipping allure publish step."
                        } catch (Exception ex) {
                            echo "Allure publish failed: ${ex.getMessage()}"
                        }
                    } else if (params.RUN_ALLURE) {
                        echo "Skipping Allure publish: ${env.ALLURE_DIR} not found."
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                def testStats = getTestStatistics()
                if ((env.EFFECTIVE_FAILED_COUNT ?: '').isInteger()) {
                    testStats.failed = env.EFFECTIVE_FAILED_COUNT as int
                    if (testStats.total > 0) {
                        testStats.passed = Math.max(testStats.total - testStats.failed - testStats.skipped, 0)
                    }
                }
                if (testStats.total > 0) {
                    currentBuild.result = testStats.failed > 0 ? 'FAILURE' : 'SUCCESS'
                }

                def durationDisplay = (currentBuild.durationString ?: 'N/A').replace(' and counting', '')
                def envDisplay = params.ENVIRONMENT ?: 'UAT'
                def portalDisplay = params.PORTAL ?: 'All Marketplace Access'
                envDisplay = (portalDisplay == 'All Marketplace Access' || portalDisplay == 'Default') ? envDisplay.toUpperCase() : "${envDisplay.toUpperCase()} - ${portalDisplay}"

                currentBuild.description = """
                    Environment: ${envDisplay} |
                    ${parseTestSelection(' | ')} |
                    Tests: ${testStats.total} |
                    Passed: ${testStats.passed} |
                    Failed: ${testStats.failed} |
                    Duration: ${durationDisplay}
                """.stripIndent().trim()

                if (fileExists('reports')) {
                    archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
                }
                if (fileExists(env.ALLURE_DIR)) {
                    archiveArtifacts artifacts: "${env.ALLURE_DIR}/**", allowEmptyArchive: true
                }

                if (params.SEND_EMAIL) {
                    sendEmailNotification(currentBuild.currentResult ?: 'UNKNOWN')
                }
            }
        }
    }
}

def getPortalMap() {
    return [
        'All Marketplace Access': '',
        'Dakota Ria Portal': 'dakota_ria_portal',
        'Dakota Transactions & CEOs Access': 'dakota_transactions_ceos_access',
        'FA Data Set': 'fa_data_set',
        'Is Deal Team?': 'is_deal_team',
        'Dakota Private Markets Access': 'dakota_private_markets_access',
        'Dakota Recommends Portal Access': 'dakota_recommends_portal_access',
        'Dakota Family Office Portal': 'dakota_family_office_portal',
        'Dakota private wealth portal': 'dakota_private_wealth_portal',
        'Dakota International portal': 'dakota_international_portal'
    ]
}

def setupPythonEnvironment() {
    if (isUnix()) {
        sh """
            if [ ! -x "${env.VENV_DIR}/bin/python" ]; then
                python3 -m venv ${env.VENV_DIR}
            fi
            ${env.VENV_DIR}/bin/python -m pip install --upgrade pip
            ${env.VENV_DIR}/bin/python -m pip install -r requirements.txt
            ${env.VENV_DIR}/bin/python -m pip install pytest-html pytest-json-report allure-pytest pytest-xdist pytest-rerunfailures
        """
    } else {
        bat 'if not exist "%VENV_DIR%\\Scripts\\python" py -m venv %VENV_DIR%'
        bat '%VENV_DIR%\\Scripts\\python -m pip install --upgrade pip'
        bat '%VENV_DIR%\\Scripts\\python -m pip install -r requirements.txt'
        bat '%VENV_DIR%\\Scripts\\python -m pip install pytest-html pytest-json-report allure-pytest pytest-xdist pytest-rerunfailures'
    }
}

def validateRuntimeParameters(String testSuite, String browser, String parallelWorkers, String nonAssertionRetryCount, String browserWidth, String browserHeight) {
    if (testSuite != null && !testSuite.trim()) {
        error("Invalid TEST_SUITE value.")
    }

    def normalizedBrowser = (browser ?: '').trim().toLowerCase()
    if (!(normalizedBrowser in ['chrome', 'edge', 'firefox'])) {
        error("Invalid BROWSER value '${browser}'. Supported values: chrome, edge, firefox.")
    }

    def workers = (parallelWorkers ?: '1').trim().toLowerCase()
    if (workers != 'auto') {
        if (!(workers ==~ /^\d+$/)) {
            error("Invalid PARALLEL_WORKERS value '${parallelWorkers}'. Use '1', integer >1, or 'auto'.")
        }
        if ((workers as int) < 1) {
            error("PARALLEL_WORKERS must be >= 1, got '${parallelWorkers}'.")
        }
    }

    def retryCount = (nonAssertionRetryCount ?: '1').trim()
    if (!(retryCount ==~ /^\d+$/)) {
        error("Invalid NON_ASSERTION_RETRY_COUNT value '${nonAssertionRetryCount}'. Use integer >= 0.")
    }

    validateViewportDimension('BROWSER_WIDTH', browserWidth)
    validateViewportDimension('BROWSER_HEIGHT', browserHeight)
}

def validateViewportDimension(String name, String value) {
    def normalized = (value ?: '').trim()
    if (!(normalized ==~ /^\d+$/)) {
        error("Invalid ${name} value '${value}'. Use integer > 0.")
    }
    if ((normalized as int) <= 0) {
        error("${name} must be > 0, got '${value}'.")
    }
}

def resolveSelectedTestPaths(String testSuite) {
    def suites = parseSuites(testSuite)
    if (suites.isEmpty()) {
        return ['tests/']
    }
    def paths = suites.collect { getTestPath(it) }.findAll { it && it != 'tests/' }.unique()
    return paths.isEmpty() ? ['tests/'] : paths
}

def resolveTabsExpression(def paramsObj) {
    def markerFromCheckboxes = getTabCheckboxMap()
        .findAll { row -> (paramsObj?."${row.param}" as boolean) }
        .collect { row -> row.marker }
        .unique()
    if (markerFromCheckboxes.isEmpty()) {
        return null
    }
    echo "Tab marker expression (OR logic): ${markerFromCheckboxes.join(' or ')}"
    return markerFromCheckboxes.join(' or ')
}

def getTabCheckboxMap() {
    return [
        [param: 'TAB_ALL_MARKETPLACE_ACCESS', marker: 'all_marketplace_access'],
        [param: 'TAB_ACCOUNTS', marker: 'accounts'],
        [param: 'TAB_CONTACT', marker: 'contact'],
        [param: 'TAB_ALL_DOCUMENTS', marker: 'all_documents'],
        [param: 'TAB_13F_FILINGS_INVESTMENTS_SEARCH', marker: 'filings_13f_investments_search'],
        [param: 'TAB_BENCHMARKING', marker: 'benchmarking_tab'],
        [param: 'TAB_CONFERENCE_SEARCH', marker: 'conference_search'],
        [param: 'TAB_CONSULTANT_REVIEWS', marker: 'consultant_reviews'],
        [param: 'TAB_CONTINUATION_VEHICLE', marker: 'continuation_vehicle'],
        [param: 'TAB_DAKOTA_CITY_GUIDES', marker: 'dakota_city_guides'],
        [param: 'TAB_DAKOTA_SEARCHES', marker: 'dakota_searches'],
        [param: 'TAB_DAKOTA_VIDEO_SEARCH', marker: 'dakota_video_search'],
        [param: 'TAB_EVERGREEN_FUND_PERFORMANCE', marker: 'evergreen_fund_performance'],
        [param: 'TAB_FEE_SCHEDULES_DASHBOARD', marker: 'fee_schedules_dashboard'],
        [param: 'TAB_FORECASTED_TRANSACTIONS', marker: 'forecasted_transactions'],
        [param: 'TAB_FUND_FAMILY_MEMOS', marker: 'fund_family_memos'],
        [param: 'TAB_FUND_LAUNCHES', marker: 'fund_launches'],
        [param: 'TAB_FUNDRAISING_NEWS', marker: 'fundraising_news'],
        [param: 'TAB_HEDGE_FUND_PERFORMANCE', marker: 'hedge_fund_performance'],
        [param: 'TAB_INVESTMENT_ALLOCATOR_ACCOUNTS', marker: 'investment_allocator_accounts'],
        [param: 'TAB_INVESTMENT_ALLOCATOR_CONTACTS', marker: 'investment_allocator_contacts'],
        [param: 'TAB_INVESTMENT_FIRM_ACCOUNTS', marker: 'investment_firm_accounts'],
        [param: 'TAB_INVESTMENT_FIRM_CONTACTS', marker: 'investment_firm_contacts'],
        [param: 'TAB_MANAGER_PRESENTATION_DASHBOARD', marker: 'manager_presentation_dashboard'],
        [param: 'TAB_MY_ACCOUNTS', marker: 'my_accounts'],
        [param: 'TAB_PENSION_DOCUMENTS', marker: 'pension_documents'],
        [param: 'TAB_PORTFOLIO_COMPANIES', marker: 'portfolio_companies'],
        [param: 'TAB_PORTFOLIO_COMPANIES_CONTACTS', marker: 'portfolio_companies_contacts'],
        [param: 'TAB_PRIVATE_COMPANIES_TRANSACTIONS', marker: 'private_companies_transactions'],
        [param: 'TAB_PRIVATE_FUND_SEARCH', marker: 'private_fund_search'],
        [param: 'TAB_PUBLIC_COMPANY_SEARCH', marker: 'public_company_search'],
        [param: 'TAB_PUBLIC_INVESTMENTS_SEARCH', marker: 'public_investments_search'],
        [param: 'TAB_PUBLIC_PLAN_MINUTES_SEARCH', marker: 'public_plan_minutes_search'],
        [param: 'TAB_RECENT_TRANSACTIONS', marker: 'recent_transactions'],
        [param: 'TAB_UNIVERSITY_ALUMNI_CONTACTS', marker: 'university_alumni_contacts']
    ]
}


def resolveEffectiveParallelWorkers(String parallelWorkers) {
    def requestedWorkers = (parallelWorkers ?: '1').trim().toLowerCase()
    if (requestedWorkers != 'auto') {
        return requestedWorkers
    }

    def detectedWorkers = isUnix()
        ? sh(script: 'getconf _NPROCESSORS_ONLN 2>/dev/null || nproc 2>/dev/null || echo 2', returnStdout: true).trim()
        : bat(script: '@echo off\r\necho %NUMBER_OF_PROCESSORS%', returnStdout: true).trim()

    if (!(detectedWorkers ==~ /^\d+$/) || (detectedWorkers as int) < 1) {
        echo "Unable to detect worker count for PARALLEL_WORKERS=auto. Falling back to 2."
        return '2'
    }
    return detectedWorkers
}

def buildPytestCommand(List testPaths, String markerExpression, boolean runAllure, boolean collectOnly, String browser, String parallelWorkers, String nonAssertionRetryCount) {
    def parts = []
    parts << '-v'
    parts << '--tb=short'
    parts << '--color=no'
    def selectedBrowser = (browser ?: 'chrome').trim().toLowerCase()
    def workers = resolveEffectiveParallelWorkers(parallelWorkers)

    if (workers != '1') {
        parts << '-n'
        parts << workers
    }

    if (collectOnly) {
        parts << '--collect-only'
        parts << '-q'
    } else {
        def retries = parseRetryCount(nonAssertionRetryCount)
        if (retries > 0) {
            parts << "--reruns=${retries}"
            parts << '--reruns-delay=2'
            parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?TimeoutException'
            parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?NoSuchElementException'
            parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?StaleElementReferenceException'
            parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?ElementClickInterceptedException'
            parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?WebDriverException'
        }
        parts << "--junitxml=${env.PYTEST_JUNIT}"
        parts << "--html=${env.PYTEST_HTML}"
        parts << '--self-contained-html'
        parts << '--json-report'
        parts << "--json-report-file=${env.PYTEST_JSON}"
        if (runAllure) {
            parts << "--alluredir=${env.ALLURE_DIR}"
        }
    }
    parts.addAll(testPaths)
    if (markerExpression?.trim()) {
        parts << '-m'
        parts << formatMarkerExpression(markerExpression)
    }
    if (!collectOnly) {
        parts << "--browser=${selectedBrowser}"
    }
    return parts.join(' ')
}

def runPytest(String args) {
    runShell(
        "${resolveVenvPythonCommand(true)} -m pytest ${args}",
        "${resolveVenvPythonCommand(false)} -m pytest ${args}"
    )
}

def resolveVenvPythonCommand(boolean unixStyle) {
    return unixStyle ? "${env.VENV_DIR}/bin/python" : "%VENV_DIR%\\Scripts\\python"
}

def parseRetryCount(String retryCount) {
    def normalized = (retryCount ?: '1').trim()
    if (!(normalized ==~ /^\d+$/)) {
        return 1
    }
    return normalized as int
}

def runShell(String unixCommand, String windowsCommand) {
    if (isUnix()) {
        sh(unixCommand)
    } else {
        bat(windowsCommand)
    }
}

def formatMarkerExpression(String markerExpression) {
    return (markerExpression ?: '').trim()
}

def clearReportDirectories() {
    cleanDirs(['reports', env.ALLURE_DIR])
    setupReports()
}

def cleanDirs(List dirs) {
    def normalizedDirs = dirs.findAll { it?.trim() }
    if (normalizedDirs.isEmpty()) {
        return
    }

    if (isUnix()) {
        sh """
            for path in ${normalizedDirs.collect { "'${it}'" }.join(' ')}; do
                if [ -e "\$path" ]; then
                    rm -rf "\$path"
                fi
            done
        """
    } else {
        normalizedDirs.each { d ->
            bat """
                if exist "${d}" (
                    rmdir /s /q "${d}" || (ping -n 3 127.0.0.1 > nul && rmdir /s /q "${d}")
                )
            """
        }
    }
}

def setupReports() {
    runShell(
        """
            mkdir -p reports ${env.ALLURE_DIR}
        """,
        """
            if not exist "reports" mkdir "reports"
            if not exist "${env.ALLURE_DIR}" mkdir "${env.ALLURE_DIR}"
        """
    )
}

def parseTestSelection(separator = ' | ') {
    def testSelectionParts = []
    if (params.TEST_SUITE && params.TEST_SUITE.trim() && params.TEST_SUITE != 'all' && params.TEST_SUITE != 'All Tests') {
        def suites = params.TEST_SUITE.split(',').collect { it.trim() }.findAll { it && it != 'all' && it != 'All Tests' }
        if (suites.size() > 0) {
            testSelectionParts.add("Suites: ${suites.join(', ')}")
        }
    }
    def selectedCheckboxMarkers = getTabCheckboxMap()
        .findAll { row -> (params."${row.param}" as boolean) }
        .collect { row -> row.marker }
        .unique()
    if (selectedCheckboxMarkers.size() > 0) {
        testSelectionParts.add("Tabs: ${selectedCheckboxMarkers.join(', ')}")
    }
    testSelectionParts.add("Browser: ${(params.BROWSER ?: 'chrome').trim().toLowerCase()}")
    testSelectionParts.add("Workers: ${(params.PARALLEL_WORKERS ?: '1').trim()}")
    return testSelectionParts.size() > 0 ? testSelectionParts.join(separator) : "All Tests"
}

def parseSuites(String testSuite) {
    if (!testSuite?.trim()) return []
    return testSuite
        .split(',')
        .collect { it.trim() }
        .findAll { it && it != 'all' && it != 'All Tests' }
        .collect { mapSuiteDisplayToInternal(it) }
        .unique()
}

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
    return suiteMapping.get(displayName, displayName)
}

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

def getTestStatistics() {
    def stats = [total: 0, passed: 0, failed: 0, skipped: 0]
    def jsonFile = env.PYTEST_JSON ?: 'reports/report.json'
    if (!fileExists(jsonFile)) {
        echo "pytest JSON report not found. Returning empty stats."
        return stats
    }
    try {
        def report = readJSON file: jsonFile
        def summary = (report?.summary instanceof Map) ? report.summary : [:]
        def passed = parseSummaryValue(summary, 'passed')
        def failed = parseSummaryValue(summary, 'failed')
        def errored = parseSummaryValue(summary, 'error')
        def skipped = parseSummaryValue(summary, 'skipped')
        def xfailed = parseSummaryValue(summary, 'xfailed')
        def xpassed = parseSummaryValue(summary, 'xpassed')

        stats.passed = passed
        stats.failed = failed + errored
        stats.skipped = skipped + xfailed + xpassed
        stats.total = stats.passed + stats.failed + stats.skipped
        echo "pytest stats parsed: ${stats}"
    } catch (MissingMethodException e) {
        echo "Pipeline Utility Steps readJSON is not available: ${e.getMessage()}"
        echo "Install/enable Pipeline Utility Steps plugin to improve report parsing reliability."
    } catch (Exception e) {
        echo "Error parsing pytest JSON report: ${e.getMessage()}"
    }
    return stats
}

def parseSummaryValue(Map summary, String key) {
    def raw = summary?."${key}"
    if (raw == null) {
        return 0
    }
    if (raw instanceof Number) {
        return (raw as Number).intValue()
    }
    def normalized = raw.toString().trim()
    if (normalized ==~ /^\d+$/) {
        return normalized as int
    }
    return 0
}

def collectRecipientEmails(String defaultEmail, String additionalEmails) {
    def recipients = []
    def seen = [] as Set
    [defaultEmail, additionalEmails].findAll { it?.trim() }.each { source ->
        source
            .split(/[,\s;]+/)
            .collect { it.trim() }
            .findAll { it }
            .each { mail ->
                def key = mail.toLowerCase()
                if (!seen.contains(key)) {
                    seen.add(key)
                    recipients.add(mail)
                }
            }
    }
    return recipients
}

def sendEmailNotification(String buildStatus) {
    def testStats = getTestStatistics()
    def recipients = collectRecipientEmails(params.DEFAULT_EMAIL as String, params.ADDITIONAL_EMAILS as String)
    if (recipients.isEmpty() && env.EMAIL_RECIPIENT?.trim()) {
        recipients = [env.EMAIL_RECIPIENT]
    }
    if (recipients.isEmpty()) {
        echo "No recipients configured, skipping email."
        return
    }
    def subject = "Dakota Marketplace Smoke Report || ${new Date().format('yyyy-MM-dd')}"
    def durationString = (currentBuild.durationString ?: 'N/A').replace(' and counting', '')
    // Force double math for Jenkins sandbox compatibility, then round to 1 decimal.
    def passRate = 0.0
    if (testStats.total > 0) {
        double passRateRaw = ((testStats.passed as double) * 1000.0d) / (testStats.total as double)
        passRate = (Math.round(passRateRaw) as long) / 10.0d
    }
    def passRateColor = passRate >= 90 ? '#16a34a' : (passRate >= 70 ? '#f59e0b' : '#dc2626')
    def environmentLabel = ((params.ENVIRONMENT ?: 'UAT').toUpperCase() == 'PROD') ? 'Production' : 'UAT'
    def jobUrl = env.BUILD_URL ?: ''
    def allureUrl = "${jobUrl}allure"
    def allureAvailable = params.RUN_ALLURE && fileExists(env.ALLURE_DIR)
    def body = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dakota Marketplace Smoke — Test Report</title>
<style>
  /* Email-safe typography (many clients block external font imports). */
  body { margin: 0; padding: 0; background: #eef2ff; font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }
  * { box-sizing: border-box; }
  .wrapper { background: linear-gradient(135deg,#eef2ff 0%,#f8fafc 55%,#eef2ff 100%); padding: 32px 16px; }
  .card { max-width: 680px; margin: 0 auto; background: #ffffff; border: 1px solid #dbe3ee; border-radius: 18px; overflow: hidden; box-shadow: 0 16px 55px rgba(6,13,31,0.16); }

  /* HEADER */
  .hd { background: #060d1f; padding: 0; }
  .hd-stripe { height: 4px; background: linear-gradient(90deg,#60a5fa,#1d4ed8,#7c3aed); width: 100%; }
  .hd-inner { padding: 26px 30px 22px; }
  .hd-eyebrow { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
  .hd-badge { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #bfdbfe; background: rgba(29,78,216,0.18); border: 1px solid rgba(96,165,250,0.65); padding: 4px 10px; border-radius: 999px; }
  .hd-dot { width: 6px; height: 6px; border-radius: 50%; background: #22c55e; display: inline-block; }
  .hd-live { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 9px; color: #86efac; letter-spacing: 1px; }
  .hd-title { font-size: 24px; font-weight: 800; color: #f8fafc; letter-spacing: -0.6px; line-height: 1.15; margin: 0; }

  /* STATS */
  .stats { display: table; width: 100%; border-collapse: collapse; border-top: 1px solid #0f1e3d; border-bottom: 1px solid #e2e8f0; }
  .sc { display: table-cell; width: 25%; padding: 18px 8px 16px; text-align: center; border-right: 1px solid #e2e8f0; background: #ffffff; vertical-align: top; }
  .sc:last-child { border-right: none; }
  .sc-icon { font-size: 18px; display: block; margin-bottom: 6px; }
  .sc-lbl { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 9px; letter-spacing: 1.8px; text-transform: uppercase; color: #64748b; margin-bottom: 5px; display: block; }
  .sc-num { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 30px; font-weight: 800; line-height: 1; display: block; }
  .sc-num.total  { color: #0f172a; }
  .sc-num.passed { color: #16a34a; }
  .sc-num.failed { color: #dc2626; }
  .sc-num.skipped{ color: #7c3aed; }
  .sc-sub { font-size: 10px; color: #94a3b8; margin-top: 4px; display: block; }

  /* BODY */
  .body { padding: 24px 28px; background: #ffffff; }
  .section-row { margin-bottom: 14px; }
  .section-label { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #94a3b8; }
  .section-divider { border: none; border-top: 1px solid #e2e8f0; margin: 0; flex: 1; }

  /* INFO GRID */
  .info-table { width: 100%; border-collapse: separate; border-spacing: 10px; margin: 0 -10px 10px; }
  .ic { background: linear-gradient(135deg,#f8fafc 0%,#ffffff 100%); border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 14px; vertical-align: top; width: 50%; }
  .ic-lbl { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 9px; letter-spacing: 1.2px; text-transform: uppercase; color: #94a3b8; display: block; margin-bottom: 4px; }
  .ic-val { font-size: 13px; font-weight: 600; color: #0f172a; display: block; }

  /* ALLURE */
  .allure { background: linear-gradient(135deg,#f8fafc 0%,#eef2ff 100%); border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 18px; }
  .allure-inner { display: table; width: 100%; }
  .allure-left  { display: table-cell; vertical-align: middle; }
  .allure-right { display: table-cell; vertical-align: middle; text-align: right; }
  .allure-icon  { display: inline-block; width: 42px; height: 42px; border-radius: 10px; background: #ffffff; border: 1px solid #e2e8f0; text-align: center; line-height: 42px; font-size: 20px; vertical-align: middle; margin-right: 12px; }
  .allure-text  { display: inline-block; vertical-align: middle; }
  .allure-name  { font-size: 13px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 2px; }
  .allure-url   { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 10px; color: #94a3b8; display: block; word-break: break-all; }
  .allure-btn   { display: inline-block; padding: 10px 18px; background: #000000; color: #ffffff; font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 12px; font-weight: 800; border-radius: 999px; text-decoration: none; letter-spacing: 0.6px; border: 1px solid #000000; white-space: nowrap; }
  .allure-btn-unavail { display: inline-block; padding: 10px 18px; background: #f1f5f9; color: #94a3b8; font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 12px; font-weight: 800; border-radius: 999px; text-decoration: none; letter-spacing: 0.6px; border: 1px solid #e2e8f0; white-space: nowrap; }

  /* FOOTER */
  .footer { background: #060d1f; padding: 14px 28px; border-top: 1px solid #0f1e3d; }
  .footer-inner { display: table; width: 100%; }
  .footer-left  { display: table-cell; vertical-align: middle; }
  .footer-right { display: table-cell; vertical-align: middle; text-align: right; }
  .footer-logo  { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 10px; font-weight: 800; color: #60a5fa; letter-spacing: 1px; }
  .footer-pipe  { color: #1d3a6e; font-size: 12px; margin: 0 6px; }
  .footer-text  { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 10px; color: #1d4069; }
  .footer-ts    { font-family: "Consolas","SFMono-Regular","Menlo","Monaco","Courier New",monospace; font-size: 10px; color: #1d4069; }
</style>
</head>
<body>
<div class="wrapper">
<div class="card">

  <!-- HEADER -->
  <div class="hd">
    <div class="hd-stripe"></div>
    <div class="hd-inner">
      <div class="hd-eyebrow">
        <span class="hd-badge">Smoke &middot; Automated</span>
        <span class="hd-dot"></span>
        <span class="hd-live">Build complete</span>
      </div>
      <h1 class="hd-title">Dakota Marketplace Smoke</h1>
    </div>
  </div>

  <!-- STATS ROW -->
  <div class="stats">
    <div class="sc">
      <span class="sc-icon" style="color:#64748b;">&#9776;</span>
      <span class="sc-lbl">Total</span>
      <span class="sc-num total">${testStats.total}</span>
      <span class="sc-sub">test cases</span>
    </div>
    <div class="sc">
      <span class="sc-icon" style="color:#16a34a;">&#10003;</span>
      <span class="sc-lbl">Passed</span>
      <span class="sc-num passed">${testStats.passed}</span>
      <span class="sc-sub">passed checks</span>
    </div>
    <div class="sc">
      <span class="sc-icon" style="color:#dc2626;">&#10005;</span>
      <span class="sc-lbl">Failed</span>
      <span class="sc-num failed">${testStats.failed}</span>
      <span class="sc-sub">action required</span>
    </div>
    <div class="sc">
      <span class="sc-icon" style="color:#7c3aed;">&#9193;</span>
      <span class="sc-lbl">Skipped</span>
      <span class="sc-num skipped">${testStats.skipped}</span>
      <span class="sc-sub">not executed</span>
    </div>
  </div>

  <!-- BODY -->
  <div class="body">

    <!-- Run Details -->
    <div class="section-row">
      <span class="section-label">Run details</span>
      <hr class="section-divider" style="display:inline-block;width:80%;margin-left:10px;vertical-align:middle;">
    </div>

    <table class="info-table">
      <tr>
        <td class="ic">
          <span class="ic-lbl">Environment</span>
          <span class="ic-val">${environmentLabel}</span>
        </td>
        <td class="ic">
          <span class="ic-lbl">Portal</span>
          <span class="ic-val">${params.PORTAL ?: 'All Marketplace Access'}</span>
        </td>
      </tr>
      <tr>
        <td class="ic">
          <span class="ic-lbl">Duration</span>
          <span class="ic-val">${durationString}</span>
        </td>
        <td class="ic">
          <span class="ic-lbl">Pass Percentage</span>
          <span class="ic-val" style="color:${passRateColor};font-weight:700;">${passRate}%</span>
        </td>
      </tr>
    </table>

    <!-- Allure Report -->
    <div class="section-row" style="margin-top:20px;">
      <span class="section-label">Allure report</span>
      <hr class="section-divider" style="display:inline-block;width:73%;margin-left:10px;vertical-align:middle;">
    </div>

    <div class="allure">
      <div class="allure-inner">
        <div class="allure-left">
          <span class="allure-icon">&#128202;</span>
          <span class="allure-text">
            <span class="allure-name">Allure Test Report</span>
            <span class="allure-url">${allureAvailable ? allureUrl : 'Report not available for this build'}</span>
          </span>
        </div>
        <div class="allure-right">
          ${allureAvailable ? "<a href=\"${allureUrl}\" class=\"allure-btn\">Open report &rarr;</a>" : "<span class=\"allure-btn-unavail\">Not available</span>"}
        </div>
      </div>
    </div>

  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div class="footer-inner">
      <div class="footer-left">
        <span class="footer-logo">JENKINS</span>
        <span class="footer-pipe">|</span>
        <span class="footer-text">Dakota Smoke Automation</span>
      </div>
      <div class="footer-right">
        <span class="footer-ts">Generated ${new Date().format('yyyy-MM-dd HH:mm:ss')} UTC</span>
      </div>
    </div>
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
        to: recipients.join(', ')
    )
}

