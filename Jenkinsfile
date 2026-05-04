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
            choices: ['uat', 'prod'],
            description: 'Select the test environment to run tests against'
        )
        choice(
            name: 'PORTAL',
            choices: ['Default', 'FA Portal', 'RIA Portal', 'FO Portal', 'Benchmark Portal', 'Recommends Portal', 'FA and RIA Portal'],
            description: 'Select the portal to run tests against. "Default" uses base uat/prod.'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'Column Names Validation', 'Fields Comparison', 'Fields Display Functionality', 'Lazy Loading', 'List View CRUD Operations', 'Pin/Unpin Functionality'],
            description: 'Select one test suite. Use "all" to run all suites.'
        )
        choice(
            name: 'MARKERS',
            choices: ['All Tests', 'Accounts Tab', 'Contact Tab', 'All Documents', '13F Filings & Investments Search', 'Benchmarking Tab', 'Conference Search', 'Consultant Reviews', 'Continuation Vehicle', 'Dakota City Guides', 'Dakota Searches', 'Dakota Video Search', 'Evergreen Fund Performance', 'Fee Schedules Dashboard', 'Forecasted Transactions', 'Fund Family Memos', 'Fund Launches', 'Fundraising News', 'Hedge Fund Performance', 'Investment Allocator - Accounts', 'Investment Allocator - Contacts', 'Investment Firm - Accounts', 'Investment Firm - Contacts', 'Manager Presentation Dashboard', 'My Accounts', 'Pension Documents', 'Portfolio Companies', 'Portfolio Companies - Contacts', 'Private Companies Transactions', 'Private Fund Search', 'Public Company Search', 'Public Investments Search', 'Public Plan Minutes Search', 'Recent Transactions', 'University Alumni - Contacts'],
            description: 'Select one marker. Use "All Tests" for no marker filtering.'
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

        stage('Setup Environment') {
            steps {
                script {
                    def portalMap = [
                        'Default': '',
                        'FA Portal': 'fa_portal',
                        'RIA Portal': 'ria_portal',
                        'FO Portal': 'fo_portal',
                        'Benchmark Portal': 'benchmark_portal',
                        'Recommends Portal': 'recommends_portal',
                        'FA and RIA Portal': 'fa_ria_portal'
                    ]
                    def envName = params.ENVIRONMENT ?: 'uat'
                    def portalName = params.PORTAL ?: 'Default'
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
                            ${env.VENV_DIR}/bin/python -m pip install pytest-html pytest-json-report allure-pytest pytest-xdist
                        """,
                        """
                            py -m venv %VENV_DIR%
                            %VENV_DIR%\\Scripts\\python -m pip install --upgrade pip
                            %VENV_DIR%\\Scripts\\python -m pip install -r requirements.txt
                            %VENV_DIR%\\Scripts\\python -m pip install pytest-html pytest-json-report allure-pytest pytest-xdist
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
                        params.MARKERS as String,
                        params.BROWSER as String,
                        params.PARALLEL_WORKERS as String,
                        params.NON_ASSERTION_RETRY_COUNT as String
                    )
                    def selectedPaths = resolveSelectedTestPaths(params.TEST_SUITE as String)
                    def markerExpr = resolveMarkerExpression(params.MARKERS as String)
                    def collectCmd = buildPytestCommand(
                        selectedPaths,
                        markerExpr,
                        false,
                        true,
                        params.BROWSER as String,
                        params.PARALLEL_WORKERS as String
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
                    def markerExpr = resolveMarkerExpression(params.MARKERS as String)
                    def runCmd = buildPytestCommand(
                        selectedPaths,
                        markerExpr,
                        params.RUN_ALLURE as boolean,
                        false,
                        params.BROWSER as String,
                        params.PARALLEL_WORKERS as String
                    )
                    echo "Pytest command: pytest ${runCmd}"

                    withEnv(["ENV=${env.ENV}", "BROWSER=${(params.BROWSER ?: 'chrome').trim().toLowerCase()}"]) {
                        def retryCount = parseRetryCount(params.NON_ASSERTION_RETRY_COUNT as String)
                        def retrySummary = runPytestWithSelectiveRetries(
                            runCmd,
                            retryCount,
                            params.RUN_ALLURE as boolean,
                            params.BROWSER as String
                        )
                        env.EFFECTIVE_FAILED_COUNT = "${(retrySummary.nonRetryable.size() + retrySummary.unrecoveredRetryable.size())}"
                        env.NON_RETRYABLE_FAILED_COUNT = "${retrySummary.nonRetryable.size()}"
                        env.UNRECOVERED_RETRYABLE_FAILED_COUNT = "${retrySummary.unrecoveredRetryable.size()}"
                        echo "Selective retry summary -> non-retryable(assertion): ${env.NON_RETRYABLE_FAILED_COUNT}, unrecovered retryable: ${env.UNRECOVERED_RETRYABLE_FAILED_COUNT}"
                        if (!retrySummary.success) {
                            error("Pytest failed after selective retries. Non-retryable failures: ${retrySummary.nonRetryable.size()}, unrecovered retryable failures: ${retrySummary.unrecoveredRetryable.size()}")
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
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: env.ALLURE_DIR]],
                            reportName: 'Allure Report'
                        ])
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
                def portalDisplay = params.PORTAL ?: 'Default'
                envDisplay = (portalDisplay == 'Default') ? envDisplay.toUpperCase() : "${envDisplay.toUpperCase()} - ${portalDisplay}"

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

def validateRuntimeParameters(String testSuite, String markers, String browser, String parallelWorkers, String nonAssertionRetryCount) {
    if (testSuite && !testSuite.trim()) {
        error("Invalid TEST_SUITE value.")
    }
    if (markers && !markers.trim()) {
        error("Invalid MARKERS value.")
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

def resolveMarkerExpression(String markers) {
    if (!markers?.trim()) {
        return null
    }
    def markerList = markers
        .split(',')
        .collect { it.trim() }
        .findAll { it && it != 'all' && it != 'All Tests' }
        .collect { mapMarkerDisplayToInternal(it) }
        .unique()
    return markerList.isEmpty() ? null : markerList.join(' or ')
}

def buildPytestCommand(List testPaths, String markerExpression, boolean runAllure, boolean collectOnly, String browser, String parallelWorkers) {
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

def runPytestWithSelectiveRetries(String baseRunCmd, int maxRetries, boolean runAllure, String browser) {
    def nonRetryable = []
    def retryable = []
    def unrecoveredRetryable = []

    try {
        runPytest(baseRunCmd)
        echo "Initial pytest run passed. No retries needed."
        return [success: true, nonRetryable: nonRetryable, unrecoveredRetryable: unrecoveredRetryable]
    } catch (Exception e) {
        echo "Initial pytest run failed: ${e.getMessage()}"
    }

    def initialAnalysis = analyzePytestFailures(env.PYTEST_JSON)
    nonRetryable.addAll(initialAnalysis.nonRetryable as List)
    retryable = (initialAnalysis.retryable as List).unique()

    echo "Failure analysis after initial run -> non-retryable(assertion): ${nonRetryable.size()}, retryable(non-assertion): ${retryable.size()}"
    if (retryable.isEmpty() || maxRetries <= 0) {
        unrecoveredRetryable = retryable
        return [success: (nonRetryable + unrecoveredRetryable).isEmpty(), nonRetryable: nonRetryable.unique(), unrecoveredRetryable: unrecoveredRetryable.unique()]
    }

    for (int attempt = 1; attempt <= maxRetries && !retryable.isEmpty(); attempt++) {
        def retryCmd = buildRetryPytestCommand(retryable, runAllure, browser, attempt)
        echo "Selective retry attempt ${attempt}/${maxRetries} for ${retryable.size()} node(s)."
        try {
            runPytest(retryCmd)
            echo "Selective retry attempt ${attempt} passed for all targeted tests."
            retryable = []
            break
        } catch (Exception retryErr) {
            echo "Selective retry attempt ${attempt} failed: ${retryErr.getMessage()}"
        }

        def retryJson = "reports/report-retry-${attempt}.json"
        def retryAnalysis = analyzePytestFailures(retryJson)
        nonRetryable.addAll(retryAnalysis.nonRetryable as List)
        def stillFailed = ((retryAnalysis.retryable as List) + (retryAnalysis.nonRetryable as List)).unique()
        retryable = retryable.findAll { stillFailed.contains(it) }
        echo "After retry ${attempt} -> still failing retryable tests: ${retryable.size()}"
    }

    unrecoveredRetryable = retryable.unique()
    def finalFailures = (nonRetryable + unrecoveredRetryable).unique()
    return [success: finalFailures.isEmpty(), nonRetryable: nonRetryable.unique(), unrecoveredRetryable: unrecoveredRetryable]
}

def buildRetryPytestCommand(List nodeIds, boolean runAllure, String browser, int attempt) {
    def parts = []
    parts << '-v'
    parts << '--tb=short'
    parts << '--color=no'
    parts << "--junitxml=reports/junit-retry-${attempt}.xml"
    parts << '--json-report'
    parts << "--json-report-file=reports/report-retry-${attempt}.json"
    if (runAllure) {
        parts << "--alluredir=${env.ALLURE_DIR}"
    }
    nodeIds.each { nodeId ->
        parts << "\"${escapeForDoubleQuotes(nodeId as String)}\""
    }
    parts << "--browser=${(browser ?: 'chrome').trim().toLowerCase()}"
    return parts.join(' ')
}

def analyzePytestFailures(String jsonFilePath) {
    def analysis = [retryable: [], nonRetryable: []]
    if (!fileExists(jsonFilePath)) {
        echo "pytest JSON report '${jsonFilePath}' not found; skipping retry analysis."
        return analysis
    }

    try {
        def jsonData = new groovy.json.JsonSlurperClassic().parseText(readFile(jsonFilePath))
        def tests = (jsonData?.tests instanceof List) ? jsonData.tests : []
        tests.each { testItem ->
            def outcome = (testItem?.outcome ?: '').toString().toLowerCase()
            if (outcome in ['failed', 'error']) {
                def nodeId = (testItem?.nodeid ?: '').toString()
                if (nodeId) {
                    def failureText = extractFailureText(testItem)
                    if (isAssertionFailure(failureText)) {
                        analysis.nonRetryable << nodeId
                    } else {
                        analysis.retryable << nodeId
                    }
                }
            }
        }
    } catch (Exception ex) {
        echo "Failed to analyze pytest failures from '${jsonFilePath}': ${ex.getMessage()}"
    }

    analysis.retryable = (analysis.retryable as List).unique()
    analysis.nonRetryable = (analysis.nonRetryable as List).unique()
    return analysis
}

def extractFailureText(def testItem) {
    def candidates = [
        testItem?.call?.longrepr,
        testItem?.setup?.longrepr,
        testItem?.teardown?.longrepr,
        testItem?.longrepr,
        testItem?.keywords?.toString()
    ].findAll { it != null }

    return candidates.collect { candidate ->
        if (candidate instanceof Map || candidate instanceof List) {
            return groovy.json.JsonOutput.toJson(candidate)
        }
        return candidate.toString()
    }.join('\n').toLowerCase()
}

def isAssertionFailure(String failureText) {
    if (!failureText?.trim()) {
        return false
    }
    return failureText.contains('assertionerror') || failureText =~ /\bassert\b/
}

def escapeForDoubleQuotes(String value) {
    return (value ?: '').replace('\\', '\\\\').replace('"', '\\"')
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
    if (params.MARKERS && params.MARKERS.trim()) {
        def markers = params.MARKERS.split(',').collect { it.trim() }.findAll { it && it != 'All Tests' }
        if (markers.size() > 0) {
            testSelectionParts.add("Markers: ${markers.join(', ')}")
        }
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
        'FA Portal': 'fa_portal',
        'RIA Portal': 'ria_portal',
        'FO Portal': 'fo_portal',
        'Benchmark Portal': 'benchmark_portal',
        'Recommends Portal': 'recommends_portal',
        'FA and RIA Portal': 'fa_ria_portal'
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
                  <tr><td style="padding:10px 12px;background:#dbeafe;"><strong>Portal</strong></td><td style="padding:10px 12px;">${params.PORTAL ?: 'Default'}</td></tr>
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

