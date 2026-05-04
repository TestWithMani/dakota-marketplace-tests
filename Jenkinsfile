pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
        timeout(time: 720, unit: 'MINUTES')
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
            name: 'RESET_BUILD_AND_ALLURE_HISTORY',
            defaultValue: false,
            description: 'If true, deletes previous Jenkins build history and clears any local Allure history before running tests.'
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

        stage('Reset History (Optional)') {
            when {
                expression { return params.RESET_BUILD_AND_ALLURE_HISTORY as boolean }
            }
            steps {
                script {
                    echo "RESET_BUILD_AND_ALLURE_HISTORY=true -> purging historical Jenkins builds and local Allure history."

                    // Clean workspace-level report directories/files so Allure starts from fresh results only.
                    runShell(
                        """
                            rm -rf reports ${env.ALLURE_DIR} allure-report || true
                            mkdir -p reports ${env.ALLURE_DIR}
                        """,
                        """
                            if exist reports rmdir /s /q reports
                            if exist %ALLURE_DIR% rmdir /s /q %ALLURE_DIR%
                            if exist allure-report rmdir /s /q allure-report
                            mkdir reports
                            mkdir %ALLURE_DIR%
                        """
                    )

                    // Remove previous Jenkins builds so UI/build trend/allure trend starts fresh from this build.
                    def job = currentBuild.rawBuild.parent
                    def currentBuildNumber = currentBuild.number as int
                    def deletedCount = 0
                    job.builds.findAll { build -> (build.number as int) < currentBuildNumber }.each { build ->
                        try {
                            build.delete()
                            deletedCount++
                        } catch (Exception ex) {
                            echo "Could not delete build #${build.number}: ${ex.getMessage()}"
                        }
                    }
                    echo "Deleted ${deletedCount} previous build(s)."
                }
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    def portalMap = [
                        'All Marketplace Access': '',
                        'Default': '',
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
                    def envName = params.ENVIRONMENT ?: 'uat'
                    def portalName = params.PORTAL ?: 'All Marketplace Access'
                    def portalKey = portalMap[portalName] ?: ''
                    env.ENV = portalKey ? "${envName}_${portalKey}" : envName
                    echo "Environment configured: ${env.ENV}"
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    runShell(
                        """
                            python3 -m venv ${env.VENV_DIR}
                            ${env.VENV_DIR}/bin/python -m pip install --upgrade pip
                            ${env.VENV_DIR}/bin/python -m pip install -r requirements.txt
                            ${env.VENV_DIR}/bin/python -m pip install pytest-html pytest-json-report allure-pytest pytest-xdist pytest-rerunfailures
                        """,
                        """
                            py -m venv %VENV_DIR%
                            %VENV_DIR%\\Scripts\\python -m pip install --upgrade pip
                            %VENV_DIR%\\Scripts\\python -m pip install -r requirements.txt
                            %VENV_DIR%\\Scripts\\python -m pip install pytest-html pytest-json-report allure-pytest pytest-xdist pytest-rerunfailures
                        """
                    )
                }
            }
        }

        stage('Prepare Report Directories') {
            steps {
                script {
                    runShell(
                        """
                            rm -rf reports ${env.ALLURE_DIR} || true
                            mkdir -p reports ${env.ALLURE_DIR}
                        """,
                        """
                            if exist reports rmdir /s /q reports
                            if exist %ALLURE_DIR% rmdir /s /q %ALLURE_DIR%
                            mkdir reports
                            mkdir %ALLURE_DIR%
                        """
                    )
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
                        params.NON_ASSERTION_RETRY_COUNT as String
                    )
                    def selectedPaths = resolveSelectedTestPaths(params.TEST_SUITE as String)
                    def markerExpr = resolveTabsExpression(params)
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

                    withEnv(["ENV=${env.ENV}", "BROWSER=${(params.BROWSER ?: 'chrome').trim().toLowerCase()}"]) {
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
                def envDisplay = params.ENVIRONMENT ?: 'uat'
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

def validateRuntimeParameters(String testSuite, String browser, String parallelWorkers, String nonAssertionRetryCount) {
    if (testSuite && !testSuite.trim()) {
        error("Invalid TEST_SUITE value.")
    }
    def normalizedBrowser = (browser ?: '').trim().toLowerCase()
    if (!(normalizedBrowser in ['chrome', 'edge', 'firefox'])) {
        error("Invalid BROWSER value '${browser}'. Supported values: chrome, edge, firefox.")
    }

    def workers = (parallelWorkers ?: '1').trim().toLowerCase()
    if (workers == 'auto') {
        return
    }
    if (!(workers ==~ /^\d+$/)) {
        error("Invalid PARALLEL_WORKERS value '${parallelWorkers}'. Use '1', integer >1, or 'auto'.")
    }
    if ((workers as int) < 1) {
        error("PARALLEL_WORKERS must be >= 1, got '${parallelWorkers}'.")
    }

    def retryCount = (nonAssertionRetryCount ?: '1').trim()
    if (!(retryCount ==~ /^\d+$/)) {
        error("Invalid NON_ASSERTION_RETRY_COUNT value '${nonAssertionRetryCount}'. Use integer >= 0.")
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

def buildPytestCommand(List testPaths, String markerExpression, boolean runAllure, boolean collectOnly, String browser, String parallelWorkers, String nonAssertionRetryCount) {
    def parts = []
    parts << '-v'
    parts << '--tb=short'
    parts << '--color=no'
    def selectedBrowser = (browser ?: 'chrome').trim().toLowerCase()
    def workers = (parallelWorkers ?: '1').trim().toLowerCase()

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
            parts << '--only-rerun=disconnected:\\s+not\\s+connected\\s+to\\s+DevTools'
            parts << '--only-rerun=chrome\\s+not\\s+reachable'
            parts << '--only-rerun=ERR_CONNECTION_RESET'
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
    if (markerExpression) {
        parts << '-m'
        parts << "\"${markerExpression}\""
    }
    parts << "--browser=${selectedBrowser}"
    return parts.join(' ')
}

def runPytest(String args) {
    runShell(
        "${env.VENV_DIR}/bin/python -m pytest ${args}",
        "%VENV_DIR%\\Scripts\\python -m pytest ${args}"
    )
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

def mapMarkerDisplayToInternal(displayName) {
    def markerMapping = [
        'All Tests': 'all',
        'Accounts Tab': 'accounts',
        'Contact Tab': 'contact',
        'All Documents': 'all_documents',
        '13F Filings & Investments Search': 'filings_13f_investments_search',
        'Benchmarking Tab': 'benchmarking_tab',
        'Conference Search': 'conference_search',
        'Consultant Reviews': 'consultant_reviews',
        'Continuation Vehicle': 'continuation_vehicle',
        'Dakota City Guides': 'dakota_city_guides',
        'Dakota Searches': 'dakota_searches',
        'Dakota Video Search': 'dakota_video_search',
        'Evergreen Fund Performance': 'evergreen_fund_performance',
        'Fee Schedules Dashboard': 'fee_schedules_dashboard',
        'Forecasted Transactions': 'forecasted_transactions',
        'Fund Family Memos': 'fund_family_memos',
        'Fund Launches': 'fund_launches',
        'Fundraising News': 'fundraising_news',
        'Hedge Fund Performance': 'hedge_fund_performance',
        'Investment Allocator - Accounts': 'investment_allocator_accounts',
        'Investment Allocator - Contacts': 'investment_allocator_contacts',
        'Investment Firm - Accounts': 'investment_firm_accounts',
        'Investment Firm - Contacts': 'investment_firm_contacts',
        'Manager Presentation Dashboard': 'manager_presentation_dashboard',
        'My Accounts': 'my_accounts',
        'Pension Documents': 'pension_documents',
        'Portfolio Companies': 'portfolio_companies',
        'Portfolio Companies - Contacts': 'portfolio_companies_contacts',
        'Private Companies Transactions': 'private_companies_transactions',
        'Private Fund Search': 'private_fund_search',
        'Public Company Search': 'public_company_search',
        'Public Investments Search': 'public_investments_search',
        'Public Plan Minutes Search': 'public_plan_minutes_search',
        'Recent Transactions': 'recent_transactions',
        'University Alumni - Contacts': 'university_alumni_contacts',
        'All Marketplace Access': 'all_marketplace_access',
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
    return markerMapping.get(displayName, displayName)
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
        def jsonText = readFile(jsonFile)
        def passed = extractJsonSummaryInt(jsonText, 'passed')
        def failed = extractJsonSummaryInt(jsonText, 'failed')
        def errored = extractJsonSummaryInt(jsonText, 'error')
        def skipped = extractJsonSummaryInt(jsonText, 'skipped')
        def xfailed = extractJsonSummaryInt(jsonText, 'xfailed')
        def xpassed = extractJsonSummaryInt(jsonText, 'xpassed')

        stats.passed = passed
        stats.failed = failed + errored
        stats.skipped = skipped + xfailed + xpassed
        stats.total = stats.passed + stats.failed + stats.skipped
    } catch (Exception e) {
        echo "Error parsing pytest JSON report: ${e.getMessage()}"
    }
    return stats
}

def extractJsonSummaryInt(String jsonText, String key) {
    if (!jsonText?.trim()) {
        return 0
    }
    def matcher = (jsonText =~ /"summary"\s*:\s*\{(?s).*?"${java.util.regex.Pattern.quote(key)}"\s*:\s*(\d+)/)
    if (matcher.find()) {
        return (matcher.group(1) ?: '0') as int
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
    def actualStatus = buildStatus
    if (testStats.total > 0) {
        actualStatus = testStats.failed > 0 ? 'FAILURE' : 'SUCCESS'
    }
    def recipients = collectRecipientEmails(params.DEFAULT_EMAIL as String, params.ADDITIONAL_EMAILS as String)
    if (recipients.isEmpty() && EMAIL_RECIPIENT?.trim()) {
        recipients = [EMAIL_RECIPIENT]
    }
    if (recipients.isEmpty()) {
        echo "No recipients configured, skipping email."
        return
    }
    def subject = "Dakota Marketplace Smoke Report - ${new Date().format('yyyy-MM-dd')}"
    def statusColor = actualStatus == 'SUCCESS' ? '#16a34a' : (actualStatus == 'FAILURE' ? '#dc2626' : '#f59e0b')
    def durationString = (currentBuild.durationString ?: 'N/A').replace(' and counting', '')
    def passRate = testStats.total > 0 ? ((testStats.passed * 100) / testStats.total) as int : 0
    def jobUrl = env.BUILD_URL ?: ''
    def allureUrl = "${jobUrl}allure"
    def body = """
<html>
  <body style="margin:0;padding:0;background:linear-gradient(140deg,#e0ecff 0%,#efe7ff 45%,#fff6e5 100%);font-family:'Segoe UI',Roboto,Arial,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding:24px;">
          <table width="760" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #dbe3ee;box-shadow:0 14px 32px rgba(30,64,175,0.14);">
            <tr>
              <td style="padding:22px 30px;background:linear-gradient(135deg,#0f172a 0%,#1e40af 52%,#7c3aed 100%);color:#ffffff;">
                <h2 style="margin:0;font-size:30px;letter-spacing:0.2px;">Dakota Marketplace Smoke</h2>
              </td>
            </tr>
            <tr>
              <td style="padding:20px 30px 10px;">
                <table width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;color:#1e293b;border:1px solid #bfdbfe;border-radius:12px;overflow:hidden;background:linear-gradient(180deg,#f8fbff 0%,#ffffff 100%);margin-bottom:12px;">
                  <tr><td width="32%" style="padding:10px 12px;background:#dbeafe;"><strong>Build</strong></td><td style="padding:10px 12px;">#${env.BUILD_NUMBER}</td></tr>
                  <tr><td style="padding:10px 12px;background:#dbeafe;"><strong>Status</strong></td><td style="padding:10px 12px;color:${statusColor};font-weight:700;">${actualStatus}</td></tr>
                  <tr><td style="padding:10px 12px;background:#dbeafe;"><strong>Environment</strong></td><td style="padding:10px 12px;">${(params.ENVIRONMENT ?: 'uat').toUpperCase()}</td></tr>
                  <tr><td style="padding:10px 12px;background:#dbeafe;"><strong>Portal</strong></td><td style="padding:10px 12px;">${params.PORTAL ?: 'All Marketplace Access'}</td></tr>
                  <tr><td style="padding:10px 12px;background:#dbeafe;"><strong>Selection</strong></td><td style="padding:10px 12px;">${parseTestSelection(' | ')}</td></tr>
                  <tr><td style="padding:10px 12px;background:#dbeafe;"><strong>Duration</strong></td><td style="padding:10px 12px;">${durationString}</td></tr>
                  <tr><td style="padding:10px 12px;background:#dbeafe;"><strong>Pass Percentage</strong></td><td style="padding:10px 12px;color:#0f766e;font-weight:700;">${passRate}%</td></tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:0 30px 18px;">
                <table width="100%" cellpadding="8" cellspacing="8" style="font-size:13px;">
                  <tr align="center">
                    <td style="background:linear-gradient(180deg,#ccfbf1 0%,#99f6e4 100%);color:#134e4a;border-radius:12px;"><div style="font-size:11px;">TOTAL</div><div style="font-size:24px;font-weight:800;">${testStats.total}</div></td>
                    <td style="background:linear-gradient(180deg,#dcfce7 0%,#86efac 100%);color:#14532d;border-radius:12px;"><div style="font-size:11px;">PASSED</div><div style="font-size:24px;font-weight:800;">${testStats.passed}</div></td>
                    <td style="background:linear-gradient(180deg,#fee2e2 0%,#fca5a5 100%);color:#7f1d1d;border-radius:12px;"><div style="font-size:11px;">FAILED</div><div style="font-size:24px;font-weight:800;">${testStats.failed}</div></td>
                    <td style="background:linear-gradient(180deg,#ede9fe 0%,#c4b5fd 100%);color:#4c1d95;border-radius:12px;"><div style="font-size:11px;">SKIPPED</div><div style="font-size:24px;font-weight:800;">${testStats.skipped}</div></td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:0 30px 24px;">
                <a href="${jobUrl}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;padding:8px 12px;border-radius:6px;margin-right:8px;">Open Build</a>
                <a href="${allureUrl}" style="display:inline-block;background:#7c3aed;color:#ffffff;text-decoration:none;padding:8px 12px;border-radius:6px;">Open Allure</a>
              </td>
            </tr>
            <tr>
              <td style="padding:13px 30px;background:#0f172a;color:#cbd5e1;font-size:12px;">
                Jenkins CI/CD - Dakota Smoke Automation
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
        to: recipients.join(', '),
        attachLog: true,
        compressLog: true
    )
}

