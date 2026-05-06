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
    def subject = "Dakota Marketplace Smoke Report - ${new Date().format('yyyy-MM-dd')}"
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
<html>
  <body style="margin:0;padding:0;background:#eef2ff;font-family:'Segoe UI',Arial,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:radial-gradient(circle at top left,#dbeafe 0%,#eef2ff 45%,#f8fafc 100%);">
      <tr>
        <td align="center" style="padding:24px 16px;">
          <table width="780" cellpadding="0" cellspacing="0" style="background:#ffffff;border:1px solid #dbe3ee;border-radius:14px;overflow:hidden;box-shadow:0 14px 35px rgba(15,23,42,0.12);">
            <tr>
              <td style="padding:22px 26px;background:linear-gradient(135deg,#0f172a 0%,#1e293b 40%,#2563eb 100%);color:#ffffff;">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <td>
                      <h2 style="margin:0;font-size:27px;line-height:1.2;">Dakota Marketplace Smoke</h2>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:18px 22px 8px;">
                <table width="100%" cellpadding="6" cellspacing="6" style="font-size:13px;">
                  <tr align="center">
                    <td style="background:#eff6ff;color:#0f172a;border:1px solid #bfdbfe;border-radius:10px;"><div style="font-size:11px;letter-spacing:0.4px;">TOTAL</div><div style="font-size:26px;font-weight:800;line-height:1.2;">${testStats.total}</div></td>
                    <td style="background:#ecfdf3;color:#14532d;border:1px solid #86efac;border-radius:10px;"><div style="font-size:11px;letter-spacing:0.4px;">PASSED</div><div style="font-size:26px;font-weight:800;line-height:1.2;">${testStats.passed}</div></td>
                    <td style="background:#fef2f2;color:#7f1d1d;border:1px solid #fca5a5;border-radius:10px;"><div style="font-size:11px;letter-spacing:0.4px;">FAILED</div><div style="font-size:26px;font-weight:800;line-height:1.2;">${testStats.failed}</div></td>
                    <td style="background:#f5f3ff;color:#4c1d95;border:1px solid #c4b5fd;border-radius:10px;"><div style="font-size:11px;letter-spacing:0.4px;">SKIPPED</div><div style="font-size:26px;font-weight:800;line-height:1.2;">${testStats.skipped}</div></td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:4px 22px 14px;">
                <table width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;color:#0f172a;border:1px solid #dbe3ee;border-radius:10px;overflow:hidden;background:linear-gradient(135deg,#f0f9ff 0%,#eef2ff 45%,#f5f3ff 100%);">
                  <tr><td width="38%" style="padding:11px 12px;background:#e0f2fe;color:#0c4a6e;"><strong>Environment</strong></td><td style="padding:11px 12px;font-weight:600;background:#f8fbff;">${environmentLabel}</td></tr>
                  <tr><td style="padding:11px 12px;background:#ede9fe;color:#4c1d95;"><strong>Portal</strong></td><td style="padding:11px 12px;font-weight:600;background:#fcfaff;">${params.PORTAL ?: 'All Marketplace Access'}</td></tr>
                  <tr><td style="padding:11px 12px;background:#dcfce7;color:#14532d;"><strong>Duration</strong></td><td style="padding:11px 12px;font-weight:600;background:#f7fff9;">${durationString}</td></tr>
                  <tr><td style="padding:11px 12px;background:#fef3c7;color:#92400e;"><strong>Pass Percentage</strong></td><td style="padding:11px 12px;color:${passRateColor};font-weight:800;background:#fffdf5;">${passRate}%</td></tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:0 22px 18px;">
                <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;border:1px solid #dbe3ee;border-radius:10px;">
                  <tr>
                    <td style="padding:0 14px 14px;">
                      ${allureAvailable ? "<a href=\"${allureUrl}\" style=\"display:inline-block;background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#ffffff;text-decoration:none;padding:10px 14px;font-size:13px;font-weight:700;border-radius:8px;margin-top:2px;\">Open Allure Report</a>" : "<span style=\"display:inline-block;background:#e2e8f0;color:#475569;padding:10px 14px;font-size:13px;font-weight:700;border-radius:8px;margin-top:2px;\">Allure Report Not Available</span>"}
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:12px 22px;background:#0f172a;color:#cbd5e1;font-size:12px;">
                Jenkins CI/CD - Dakota Smoke Automation | Generated at ${new Date().format('yyyy-MM-dd HH:mm:ss')}
              </td>
            </tr>
          </table>
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
        to: recipients.join(', ')
    )
}

