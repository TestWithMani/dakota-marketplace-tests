// ============================================================
//  Dakota Marketplace — Regression Pipeline
//  Fixes applied:
//   1.  Single clearReportDirectories() call (removed duplicate from Reset stage)
//   2.  resolveSelectedTestPaths / resolveTabsExpression computed once, stored in env
//   3.  getTestStatistics() called once; result passed into sendEmailNotification()
//   4.  EFFECTIVE_FAILED_COUNT wired up: parsed from JSON after catchError
//   5.  Static Validation wrapped in same withEnv block as Run Tests
//   6.  Marker expression shell-quoted to survive word-splitting
//   7.  Unknown TEST_SUITE values caught early in validateRuntimeParameters()
//   8.  TAB_SELECTION_HELP replaced with a descriptive separator comment param
//   9.  Pass-rate calculation centralised inside getTestStatistics() return map
//  10.  Viewport dims forwarded into Static Validation collect stage
//  11.  Empty RESOLVED_TEST_PATHS guarded with safe fallback ('tests/')
//  12.  Windows cmd quoting: -m uses double-quotes on Windows, single on Unix
//  13.  venv lives in JENKINS_HOME, not the workspace — installed once server-wide
//  14.  --only-rerun flags collapsed into one combined regex (last flag wins bug)
//  15.  Shared venv writes serialised via flock (Unix) / FileShare.None (Windows)
// ============================================================

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
            description: 'Select the test environment to run tests against.'
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
            description: 'All Marketplace Access uses base uat/prod credentials. Other choices append a portal suffix to the ENV.'
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
            description: "Pytest xdist workers. Use '1' to disable parallel mode, an integer > 1, or 'auto'."
        )
        string(
            name: 'NON_ASSERTION_RETRY_COUNT',
            defaultValue: '1',
            description: "Retry attempts for non-assertion pytest failures. 0 disables selective retry."
        )
        booleanParam(
            name: 'RUN_ALLURE',
            defaultValue: true,
            description: 'Generate and publish Allure report in Jenkins.'
        )
        booleanParam(
            name: 'RESET_WORKSPACE_AND_ALLURE_HISTORY',
            defaultValue: false,
            description: 'If true, clears workspace report folders and local Allure results before the Prepare Report Directories stage runs its own clean. No duplicate clean occurs.'
        )
        booleanParam(
            name: 'SEND_EMAIL',
            defaultValue: true,
            description: 'Send email notification after build completion.'
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
        // ── Tab filter checkboxes ─────────────────────────────────────────────
        // Select one or more TAB_* checkboxes to filter tests by tab marker.
        // If none are selected, no tab marker filter is applied and all tabs run.
        // ─────────────────────────────────────────────────────────────────────
        booleanParam(name: 'TAB_ALL_MARKETPLACE_ACCESS',        defaultValue: false, description: 'Tab: All Marketplace Access')
        booleanParam(name: 'TAB_ACCOUNTS',                      defaultValue: false, description: 'Tab: Accounts')
        booleanParam(name: 'TAB_CONTACT',                       defaultValue: false, description: 'Tab: Contact')
        booleanParam(name: 'TAB_ALL_DOCUMENTS',                 defaultValue: false, description: 'Tab: All Documents')
        booleanParam(name: 'TAB_13F_FILINGS_INVESTMENTS_SEARCH',defaultValue: false, description: 'Tab: 13F Filings & Investments Search')
        booleanParam(name: 'TAB_BENCHMARKING',                  defaultValue: false, description: 'Tab: Benchmarking')
        booleanParam(name: 'TAB_CONFERENCE_SEARCH',             defaultValue: false, description: 'Tab: Conference Search')
        booleanParam(name: 'TAB_CONSULTANT_REVIEWS',            defaultValue: false, description: 'Tab: Consultant Reviews')
        booleanParam(name: 'TAB_CONTINUATION_VEHICLE',          defaultValue: false, description: 'Tab: Continuation Vehicle')
        booleanParam(name: 'TAB_DAKOTA_CITY_GUIDES',            defaultValue: false, description: 'Tab: Dakota City Guides')
        booleanParam(name: 'TAB_DAKOTA_SEARCHES',               defaultValue: false, description: 'Tab: Dakota Searches')
        booleanParam(name: 'TAB_DAKOTA_VIDEO_SEARCH',           defaultValue: false, description: 'Tab: Dakota Video Search')
        booleanParam(name: 'TAB_EVERGREEN_FUND_PERFORMANCE',    defaultValue: false, description: 'Tab: Evergreen Fund Performance')
        booleanParam(name: 'TAB_FEE_SCHEDULES_DASHBOARD',       defaultValue: false, description: 'Tab: Fee Schedules Dashboard')
        booleanParam(name: 'TAB_FORECASTED_TRANSACTIONS',       defaultValue: false, description: 'Tab: Forecasted Transactions')
        booleanParam(name: 'TAB_FUND_FAMILY_MEMOS',             defaultValue: false, description: 'Tab: Fund Family Memos')
        booleanParam(name: 'TAB_FUND_LAUNCHES',                 defaultValue: false, description: 'Tab: Fund Launches')
        booleanParam(name: 'TAB_FUNDRAISING_NEWS',              defaultValue: false, description: 'Tab: Fundraising News')
        booleanParam(name: 'TAB_HEDGE_FUND_PERFORMANCE',        defaultValue: false, description: 'Tab: Hedge Fund Performance')
        booleanParam(name: 'TAB_INVESTMENT_ALLOCATOR_ACCOUNTS', defaultValue: false, description: 'Tab: Investment Allocator – Accounts')
        booleanParam(name: 'TAB_INVESTMENT_ALLOCATOR_CONTACTS', defaultValue: false, description: 'Tab: Investment Allocator – Contacts')
        booleanParam(name: 'TAB_INVESTMENT_FIRM_ACCOUNTS',      defaultValue: false, description: 'Tab: Investment Firm – Accounts')
        booleanParam(name: 'TAB_INVESTMENT_FIRM_CONTACTS',      defaultValue: false, description: 'Tab: Investment Firm – Contacts')
        booleanParam(name: 'TAB_MANAGER_PRESENTATION_DASHBOARD',defaultValue: false, description: 'Tab: Manager Presentation Dashboard')
        booleanParam(name: 'TAB_MY_ACCOUNTS',                   defaultValue: false, description: 'Tab: My Accounts')
        booleanParam(name: 'TAB_PENSION_DOCUMENTS',             defaultValue: false, description: 'Tab: Pension Documents')
        booleanParam(name: 'TAB_PORTFOLIO_COMPANIES',           defaultValue: false, description: 'Tab: Portfolio Companies')
        booleanParam(name: 'TAB_PORTFOLIO_COMPANIES_CONTACTS',  defaultValue: false, description: 'Tab: Portfolio Companies – Contacts')
        booleanParam(name: 'TAB_PRIVATE_COMPANIES_TRANSACTIONS',defaultValue: false, description: 'Tab: Private Companies Transactions')
        booleanParam(name: 'TAB_PRIVATE_FUND_SEARCH',           defaultValue: false, description: 'Tab: Private Fund Search')
        booleanParam(name: 'TAB_PUBLIC_COMPANY_SEARCH',         defaultValue: false, description: 'Tab: Public Company Search')
        booleanParam(name: 'TAB_PUBLIC_INVESTMENTS_SEARCH',     defaultValue: false, description: 'Tab: Public Investments Search')
        booleanParam(name: 'TAB_PUBLIC_PLAN_MINUTES_SEARCH',    defaultValue: false, description: 'Tab: Public Plan Minutes Search')
        booleanParam(name: 'TAB_RECENT_TRANSACTIONS',           defaultValue: false, description: 'Tab: Recent Transactions')
        booleanParam(name: 'TAB_UNIVERSITY_ALUMNI_CONTACTS',    defaultValue: false, description: 'Tab: University Alumni – Contacts')
    }

    environment {
        // FIX 13: venv lives in JENKINS_HOME, completely outside the workspace.
        //         Survives workspace wipes, clean checkouts, and build-discarder
        //         pruning. Python + all pytest plugins are installed exactly once
        //         per Jenkins server rather than on every build.
        VENV_DIR        = "${env.JENKINS_HOME}/.dakota-venv"
        PYTEST_JUNIT    = 'reports/junit.xml'
        PYTEST_HTML     = 'reports/report.html'
        PYTEST_JSON     = 'reports/report.json'
        ALLURE_DIR      = 'allure-results'
        EMAIL_RECIPIENT = 'usman.arshad@rolustech.com'
    }

    stages {

        // ── 1. Checkout ──────────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                    def shortCommit = env.GIT_COMMIT ? env.GIT_COMMIT.take(7) : 'N/A'
                    echo "Branch: ${env.BRANCH_NAME ?: 'N/A'} | Commit: ${shortCommit}"
                }
            }
        }

        // ── 2. Reset workspace (optional) ─────────────────────────────────────
        // FIX 1: Does NOT call clearReportDirectories() anymore.
        //         The mandatory "Prepare Report Directories" stage below always
        //         does the clean, so doing it here too was a duplicate wipe.
        //         This stage now only logs intent; the actual clean happens once.
        stage('Reset Workspace Reports (Optional)') {
            when {
                expression { return params.RESET_WORKSPACE_AND_ALLURE_HISTORY as boolean }
            }
            steps {
                script {
                    echo "RESET_WORKSPACE_AND_ALLURE_HISTORY=true: the upcoming 'Prepare Report Directories' stage will perform a full clean of all report folders and Allure results."
                    echo "Skipping Jenkins build history deletion in pipeline script. Use a trusted admin-maintained cleanup job if needed."
                }
            }
        }

        // ── 3. Setup environment ──────────────────────────────────────────────
        stage('Setup Environment') {
            steps {
                script {
                    def envName    = (params.ENVIRONMENT ?: 'UAT').toLowerCase()
                    def portalName = params.PORTAL ?: 'All Marketplace Access'
                    def portalKey  = getPortalMap()[portalName] ?: ''
                    env.TEST_ENV   = portalKey ? "${envName}_${portalKey}" : envName
                    echo "Environment configured: ${env.TEST_ENV}"
                }
            }
        }

        // ── 4. Setup Python environment ───────────────────────────────────────
        stage('Setup Python Environment') {
            steps {
                script {
                    setupPythonEnvironment()
                }
            }
        }

        // ── 5. Prepare report directories ─────────────────────────────────────
        // FIX 1 (cont.): Single authoritative clean + mkdir. Runs every build.
        stage('Prepare Report Directories') {
            steps {
                script {
                    clearReportDirectories()
                }
            }
        }

        // ── 6. Resolve test selection (once) ──────────────────────────────────
        // FIX 2: Compute paths and marker expression a single time, persist to
        //         env vars so Static Validation and Run Tests share the values
        //         without re-computing (and without double echo in the logs).
        stage('Resolve Test Selection') {
            steps {
                script {
                    // FIX 7: validateRuntimeParameters now also validates TEST_SUITE
                    //         against the known list and errors early on a bad value.
                    validateRuntimeParameters(
                        params.TEST_SUITE as String,
                        params.BROWSER as String,
                        params.PARALLEL_WORKERS as String,
                        params.NON_ASSERTION_RETRY_COUNT as String,
                        params.BROWSER_WIDTH as String,
                        params.BROWSER_HEIGHT as String
                    )

                    def selectedPaths = resolveSelectedTestPaths(params.TEST_SUITE as String)
                    def markerExpr    = resolveTabsExpression(params)

                    // Persist for downstream stages
                    env.RESOLVED_TEST_PATHS  = selectedPaths.join('|')
                    env.RESOLVED_MARKER_EXPR = markerExpr ?: ''

                    echo "Test paths   : ${env.RESOLVED_TEST_PATHS}"
                    echo "Marker expr  : ${env.RESOLVED_MARKER_EXPR ?: '(none)'}"
                }
            }
        }

        // ── 7. Static validation ──────────────────────────────────────────────
        // FIX 5:  Wrapped in the same withEnv block used by Run Tests so that
        //         conftest fixtures relying on TEST_ENV / BROWSER / HEADLESS /
        //         viewport vars behave identically at collection time.
        // FIX 10: BROWSER_WIDTH and BROWSER_HEIGHT now forwarded here too.
        // FIX 11: Safe fallback on RESOLVED_TEST_PATHS in case env is ever empty.
        stage('Static Validation') {
            steps {
                script {
                    def selectedPaths = (env.RESOLVED_TEST_PATHS ?: 'tests/').split('\\|').toList()
                    def markerExpr    = env.RESOLVED_MARKER_EXPR ?: null

                    def collectCmd = buildPytestCommand(
                        selectedPaths,
                        markerExpr,
                        false,
                        true,   // collect-only
                        params.BROWSER as String,
                        params.PARALLEL_WORKERS as String,
                        params.NON_ASSERTION_RETRY_COUNT as String
                    )

                    withEnv([
                        "TEST_ENV=${env.TEST_ENV}",
                        "BROWSER=${(params.BROWSER ?: 'chrome').trim().toLowerCase()}",
                        "HEADLESS=${params.HEADLESS as boolean}",
                        "BROWSER_WIDTH=${(params.BROWSER_WIDTH ?: '1920').trim()}",
                        "BROWSER_HEIGHT=${(params.BROWSER_HEIGHT ?: '1080').trim()}"
                    ]) {
                        runPytest('--version')
                        runPytest(collectCmd)
                    }
                }
            }
        }

        // ── 8. Run tests ──────────────────────────────────────────────────────
        // FIX 4:  After catchError, parse the JSON report and write
        //         EFFECTIVE_FAILED_COUNT so post{} can use the real count.
        // FIX 11: Safe fallback on RESOLVED_TEST_PATHS in case env is ever empty.
        stage('Run Tests') {
            steps {
                script {
                    def selectedPaths = (env.RESOLVED_TEST_PATHS ?: 'tests/').split('\\|').toList()
                    def markerExpr    = env.RESOLVED_MARKER_EXPR ?: null

                    def runCmd = buildPytestCommand(
                        selectedPaths,
                        markerExpr,
                        params.RUN_ALLURE as boolean,
                        false,  // not collect-only
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

                    // FIX 4: Wire up EFFECTIVE_FAILED_COUNT from the JSON report
                    //         produced in this stage so post{} gets the real value.
                    def stats = getTestStatistics()
                    env.EFFECTIVE_FAILED_COUNT = stats.failed as String
                    echo "Effective failed count set to: ${env.EFFECTIVE_FAILED_COUNT}"
                }
            }
        }

        // ── 9. Publish reports ────────────────────────────────────────────────
        stage('Publish Reports') {
            steps {
                script {
                    if (fileExists(env.PYTEST_JUNIT)) {
                        junit allowEmptyResults: true, testResults: env.PYTEST_JUNIT
                    }

                    try {
                        publishHTML(target: [
                            reportName           : 'Pytest HTML Report',
                            reportDir            : 'reports',
                            reportFiles          : 'report.html',
                            keepAll              : true,
                            alwaysLinkToLastBuild: true,
                            allowMissing         : true
                        ])
                    } catch (Exception ex) {
                        echo "HTML Publisher not available or failed: ${ex.getMessage()}"
                    }

                    if (params.RUN_ALLURE && fileExists(env.ALLURE_DIR)) {
                        try {
                            allure([
                                includeProperties: false,
                                jdk              : '',
                                properties       : [],
                                reportBuildPolicy: 'ALWAYS',
                                results          : [[path: env.ALLURE_DIR]],
                                reportName       : 'Allure Report'
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

    // ── post: always ─────────────────────────────────────────────────────────
    // FIX 3: getTestStatistics() called exactly once; result passed into
    //         sendEmailNotification() instead of being re-parsed there.
    post {
        always {
            script {
                def testStats = getTestStatistics()

                // FIX 4 (cont.): Apply EFFECTIVE_FAILED_COUNT override when set
                if ((env.EFFECTIVE_FAILED_COUNT ?: '').isInteger()) {
                    int effectiveFailed = env.EFFECTIVE_FAILED_COUNT as int
                    if (effectiveFailed != testStats.failed) {
                        echo "Overriding parsed failed count (${testStats.failed}) with EFFECTIVE_FAILED_COUNT (${effectiveFailed})."
                        testStats.failed = effectiveFailed
                        if (testStats.total > 0) {
                            testStats.passed = Math.max(testStats.total - testStats.failed - testStats.skipped, 0)
                        }
                    }
                }

                if (testStats.total > 0) {
                    currentBuild.result = testStats.failed > 0 ? 'FAILURE' : 'SUCCESS'
                }

                def durationDisplay = (currentBuild.durationString ?: 'N/A').replace(' and counting', '')
                def envDisplay      = params.ENVIRONMENT ?: 'UAT'
                def portalDisplay   = params.PORTAL ?: 'All Marketplace Access'
                envDisplay = (portalDisplay == 'All Marketplace Access' || portalDisplay == 'Default')
                    ? envDisplay.toUpperCase()
                    : "${envDisplay.toUpperCase()} - ${portalDisplay}"

                currentBuild.description = """
                    Environment: ${envDisplay} |
                    ${parseTestSelection(' | ')} |
                    Tests: ${testStats.total} |
                    Passed: ${testStats.passed} |
                    Failed: ${testStats.failed} |
                    Pass rate: ${testStats.passRate}% |
                    Duration: ${durationDisplay}
                """.stripIndent().trim()

                if (fileExists('reports')) {
                    archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
                }
                if (fileExists(env.ALLURE_DIR)) {
                    archiveArtifacts artifacts: "${env.ALLURE_DIR}/**", allowEmptyArchive: true
                }

                // FIX 3: Pass the already-computed testStats into the email function
                if (params.SEND_EMAIL) {
                    sendEmailNotification(currentBuild.currentResult ?: 'UNKNOWN', testStats)
                }
            }
        }
    }
}

// ══════════════════════════════════════════════════════════════════════════════
//  Helper functions
// ══════════════════════════════════════════════════════════════════════════════

def getPortalMap() {
    return [
        'All Marketplace Access'           : '',
        'Dakota Ria Portal'                : 'dakota_ria_portal',
        'Dakota Transactions & CEOs Access': 'dakota_transactions_ceos_access',
        'FA Data Set'                      : 'fa_data_set',
        'Is Deal Team?'                    : 'is_deal_team',
        'Dakota Private Markets Access'    : 'dakota_private_markets_access',
        'Dakota Recommends Portal Access'  : 'dakota_recommends_portal_access',
        'Dakota Family Office Portal'      : 'dakota_family_office_portal',
        'Dakota private wealth portal'     : 'dakota_private_wealth_portal',
        'Dakota International portal'      : 'dakota_international_portal'
    ]
}

def setupPythonEnvironment() {
    // FIX 13: VENV_DIR points to JENKINS_HOME/.dakota-venv — shared across all
    //         builds on this agent, created once, reused forever.
    //
    // FIX 15: The shared venv is protected by an exclusive file lock so that two
    //         jobs running concurrently on the same agent cannot both execute pip
    //         at the same time and corrupt site-packages.
    //
    //         Unix:    flock(1) with a 300-second timeout on a dedicated lock file.
    //                  The venv creation itself is also locked — a second build
    //                  arriving before the first finishes python3 -m venv will wait
    //                  rather than racing on an incomplete venv.
    //
    //         Windows: PowerShell opens the lock file with FileShare.None, which
    //                  causes any competing process that tries to open the same file
    //                  to block (IOException) until the first process closes it.
    //                  A 300-second polling retry loop provides the same timeout
    //                  behaviour as flock -w on Unix.
    if (isUnix()) {
        sh """
            # Acquire an exclusive lock on .pip.lock for the duration of venv
            # creation AND all pip installs.  flock -w 300 waits up to 5 minutes
            # before giving up with a non-zero exit code (which sh -e propagates).
            (
                flock -w 300 9 || { echo "Timed out waiting for venv lock after 300s"; exit 1; }

                if [ ! -x "${env.VENV_DIR}/bin/python" ]; then
                    echo "Creating shared venv at ${env.VENV_DIR} (first-time setup)..."
                    python3 -m venv ${env.VENV_DIR}
                else
                    echo "Reusing existing shared venv at ${env.VENV_DIR}."
                fi

                ${env.VENV_DIR}/bin/python -m pip install --upgrade pip --quiet
                ${env.VENV_DIR}/bin/python -m pip install -r requirements.txt --quiet
                ${env.VENV_DIR}/bin/python -m pip install \
                    pytest-html pytest-json-report allure-pytest \
                    pytest-xdist pytest-rerunfailures --quiet

            ) 9>"${env.VENV_DIR}/.pip.lock"
        """
    } else {
        // On Windows we use PowerShell to hold an exclusive file handle for the
        // entire duration of venv creation + pip installs.  FileShare.None means
        // no other process can open the lock file while we hold it — they will
        // receive an IOException and retry every 5 seconds up to 300 seconds.
        powershell """
            \$lockPath  = '${env.VENV_DIR}/.pip.lock'
            \$venvPy    = '${env.VENV_DIR}/Scripts/python.exe'
            \$pip       = '${env.VENV_DIR}/Scripts/python'
            \$timeout   = 300
            \$waited    = 0
            \$lockStream = \$null

            while (\$true) {
                try {
                    \$lockStream = [System.IO.File]::Open(
                        \$lockPath,
                        [System.IO.FileMode]::OpenOrCreate,
                        [System.IO.FileAccess]::ReadWrite,
                        [System.IO.FileShare]::None
                    )
                    break
                } catch [System.IO.IOException] {
                    if (\$waited -ge \$timeout) {
                        Write-Error "Timed out waiting for venv lock after \${timeout}s"
                        exit 1
                    }
                    Write-Host "Waiting for venv lock... (\${waited}s elapsed)"
                    Start-Sleep -Seconds 5
                    \$waited += 5
                }
            }

            try {
                if (-Not (Test-Path \$venvPy)) {
                    Write-Host "Creating shared venv at ${env.VENV_DIR} (first-time setup)..."
                    py -m venv '${env.VENV_DIR}'
                } else {
                    Write-Host "Reusing existing shared venv at ${env.VENV_DIR}."
                }

                & \$pip -m pip install --upgrade pip --quiet
                & \$pip -m pip install -r requirements.txt --quiet
                & \$pip -m pip install pytest-html pytest-json-report allure-pytest pytest-xdist pytest-rerunfailures --quiet

                if (\$LASTEXITCODE -ne 0) { exit \$LASTEXITCODE }
            } finally {
                if (\$lockStream) { \$lockStream.Close() }
            }
        """
    }
}

// FIX 7: KNOWN_SUITES used both for the dropdown (in pipeline params) and for
//         early validation here, so an unrecognised value errors immediately
//         rather than silently running the entire test suite.
@groovy.transform.Field
static final List KNOWN_SUITE_DISPLAY_NAMES = [
    'all',
    'Column Names Validation',
    'Fields Comparison',
    'Fields Display Functionality',
    'Lazy Loading',
    'List View CRUD Operations',
    'Pin/Unpin Functionality'
]

def validateRuntimeParameters(String testSuite, String browser, String parallelWorkers, String nonAssertionRetryCount, String browserWidth, String browserHeight) {
    // FIX 7: Validate TEST_SUITE against the known list
    if (testSuite?.trim() && !KNOWN_SUITE_DISPLAY_NAMES.contains(testSuite.trim())) {
        error("Invalid TEST_SUITE value '${testSuite}'. Must be one of: ${KNOWN_SUITE_DISPLAY_NAMES.join(', ')}.")
    }

    def normalizedBrowser = (browser ?: '').trim().toLowerCase()
    if (!(normalizedBrowser in ['chrome', 'edge', 'firefox'])) {
        error("Invalid BROWSER value '${browser}'. Supported values: chrome, edge, firefox.")
    }

    def workers = (parallelWorkers ?: '1').trim().toLowerCase()
    if (workers != 'auto') {
        if (!(workers ==~ /^\d+$/)) {
            error("Invalid PARALLEL_WORKERS value '${parallelWorkers}'. Use '1', an integer > 1, or 'auto'.")
        }
        if ((workers as int) < 1) {
            error("PARALLEL_WORKERS must be >= 1, got '${parallelWorkers}'.")
        }
    }

    def retryCount = (nonAssertionRetryCount ?: '1').trim()
    if (!(retryCount ==~ /^\d+$/)) {
        error("Invalid NON_ASSERTION_RETRY_COUNT value '${nonAssertionRetryCount}'. Use an integer >= 0.")
    }

    validateViewportDimension('BROWSER_WIDTH', browserWidth)
    validateViewportDimension('BROWSER_HEIGHT', browserHeight)
}

def validateViewportDimension(String name, String value) {
    def normalized = (value ?: '').trim()
    if (!(normalized ==~ /^\d+$/)) {
        error("Invalid ${name} value '${value}'. Use an integer > 0.")
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
    def markers = getTabCheckboxMap()
        .findAll { row -> (paramsObj?."${row.param}" as boolean) }
        .collect { row -> row.marker }
        .unique()
    if (markers.isEmpty()) {
        return null
    }
    def expression = markers.join(' or ')
    echo "Tab marker expression (OR logic): ${expression}"
    return expression
}

def getTabCheckboxMap() {
    return [
        [param: 'TAB_ALL_MARKETPLACE_ACCESS',         marker: 'all_marketplace_access'],
        [param: 'TAB_ACCOUNTS',                        marker: 'accounts'],
        [param: 'TAB_CONTACT',                         marker: 'contact'],
        [param: 'TAB_ALL_DOCUMENTS',                   marker: 'all_documents'],
        [param: 'TAB_13F_FILINGS_INVESTMENTS_SEARCH',  marker: 'filings_13f_investments_search'],
        [param: 'TAB_BENCHMARKING',                    marker: 'benchmarking_tab'],
        [param: 'TAB_CONFERENCE_SEARCH',               marker: 'conference_search'],
        [param: 'TAB_CONSULTANT_REVIEWS',              marker: 'consultant_reviews'],
        [param: 'TAB_CONTINUATION_VEHICLE',            marker: 'continuation_vehicle'],
        [param: 'TAB_DAKOTA_CITY_GUIDES',              marker: 'dakota_city_guides'],
        [param: 'TAB_DAKOTA_SEARCHES',                 marker: 'dakota_searches'],
        [param: 'TAB_DAKOTA_VIDEO_SEARCH',             marker: 'dakota_video_search'],
        [param: 'TAB_EVERGREEN_FUND_PERFORMANCE',      marker: 'evergreen_fund_performance'],
        [param: 'TAB_FEE_SCHEDULES_DASHBOARD',         marker: 'fee_schedules_dashboard'],
        [param: 'TAB_FORECASTED_TRANSACTIONS',         marker: 'forecasted_transactions'],
        [param: 'TAB_FUND_FAMILY_MEMOS',               marker: 'fund_family_memos'],
        [param: 'TAB_FUND_LAUNCHES',                   marker: 'fund_launches'],
        [param: 'TAB_FUNDRAISING_NEWS',                marker: 'fundraising_news'],
        [param: 'TAB_HEDGE_FUND_PERFORMANCE',          marker: 'hedge_fund_performance'],
        [param: 'TAB_INVESTMENT_ALLOCATOR_ACCOUNTS',   marker: 'investment_allocator_accounts'],
        [param: 'TAB_INVESTMENT_ALLOCATOR_CONTACTS',   marker: 'investment_allocator_contacts'],
        [param: 'TAB_INVESTMENT_FIRM_ACCOUNTS',        marker: 'investment_firm_accounts'],
        [param: 'TAB_INVESTMENT_FIRM_CONTACTS',        marker: 'investment_firm_contacts'],
        [param: 'TAB_MANAGER_PRESENTATION_DASHBOARD',  marker: 'manager_presentation_dashboard'],
        [param: 'TAB_MY_ACCOUNTS',                     marker: 'my_accounts'],
        [param: 'TAB_PENSION_DOCUMENTS',               marker: 'pension_documents'],
        [param: 'TAB_PORTFOLIO_COMPANIES',             marker: 'portfolio_companies'],
        [param: 'TAB_PORTFOLIO_COMPANIES_CONTACTS',    marker: 'portfolio_companies_contacts'],
        [param: 'TAB_PRIVATE_COMPANIES_TRANSACTIONS',  marker: 'private_companies_transactions'],
        [param: 'TAB_PRIVATE_FUND_SEARCH',             marker: 'private_fund_search'],
        [param: 'TAB_PUBLIC_COMPANY_SEARCH',           marker: 'public_company_search'],
        [param: 'TAB_PUBLIC_INVESTMENTS_SEARCH',       marker: 'public_investments_search'],
        [param: 'TAB_PUBLIC_PLAN_MINUTES_SEARCH',      marker: 'public_plan_minutes_search'],
        [param: 'TAB_RECENT_TRANSACTIONS',             marker: 'recent_transactions'],
        [param: 'TAB_UNIVERSITY_ALUMNI_CONTACTS',      marker: 'university_alumni_contacts']
    ]
}

def resolveEffectiveParallelWorkers(String parallelWorkers) {
    def requested = (parallelWorkers ?: '1').trim().toLowerCase()
    if (requested != 'auto') {
        return requested
    }
    def detected = isUnix()
        ? sh(script: 'getconf _NPROCESSORS_ONLN 2>/dev/null || nproc 2>/dev/null || echo 2', returnStdout: true).trim()
        : bat(script: '@echo off\r\necho %NUMBER_OF_PROCESSORS%', returnStdout: true).trim()

    if (!(detected ==~ /^\d+$/) || (detected as int) < 1) {
        echo "Unable to detect worker count for PARALLEL_WORKERS=auto. Falling back to 2."
        return '2'
    }
    return detected
}

// FIX 6: Marker expression is now single-quoted in the generated command string
//         so the shell does not word-split on the spaces surrounding 'or'.
def buildPytestCommand(List testPaths, String markerExpression, boolean runAllure, boolean collectOnly, String browser, String parallelWorkers, String nonAssertionRetryCount) {
    def parts   = []
    def workers = resolveEffectiveParallelWorkers(parallelWorkers)

    parts << '-v'
    parts << '--tb=short'
    parts << '--color=no'

    if (workers != '1') {
        parts << "-n ${workers}"
    }

    if (collectOnly) {
        parts << '--collect-only'
        parts << '-q'
    } else {
        def retries = parseRetryCount(nonAssertionRetryCount)
        if (retries > 0) {
            parts << "--reruns=${retries}"
            parts << '--reruns-delay=2'
            // FIX 14: pytest-rerunfailures only honours the LAST --only-rerun when
            //         multiple are supplied — each one silently overwrites the previous.
            //         A single alternation regex is the correct and documented pattern:
            //         all five exception types are matched by one compiled expression,
            //         and pytest-rerunfailures receives exactly one --only-rerun flag.
            parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?(TimeoutException|NoSuchElementException|StaleElementReferenceException|ElementClickInterceptedException|WebDriverException)'
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

    // FIX 6 + FIX 12: Marker expression quoting is now platform-aware.
    //   Unix  (bash/sh): wrap in single quotes → -m 'accounts or contact'
    //     Single quotes prevent ALL shell interpretation; the safest choice on Unix.
    //   Windows (cmd):   wrap in double quotes → -m "accounts or contact"
    //     cmd.exe does not treat single quotes as string delimiters at all — it
    //     passes them literally to the process, so pytest receives 'accounts' with
    //     the quote characters embedded and the marker match fails silently.
    //     Double quotes are the correct Windows delimiter for multi-word arguments.
    if (markerExpression?.trim()) {
        def safeExpr = markerExpression.trim()
        if (isUnix()) {
            // Escape any embedded single quotes for bash safety
            parts << "-m '${safeExpr.replace("'", "'\\''")}'"
        } else {
            // Escape any embedded double quotes for cmd safety
            parts << "-m \"${safeExpr.replace('"', '\\"')}\""
        }
    }

    if (!collectOnly) {
        parts << "--browser=${(browser ?: 'chrome').trim().toLowerCase()}"
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
    // FIX 13 (cont.): Interpolate env.VENV_DIR directly on both platforms.
    // The old %VENV_DIR% bat syntax only works for plain strings; now that
    // VENV_DIR is a Groovy-expanded absolute path we must use env.VENV_DIR.
    return unixStyle
        ? "${env.VENV_DIR}/bin/python"
        : "${env.VENV_DIR}\\Scripts\\python"
}

def parseRetryCount(String retryCount) {
    def normalized = (retryCount ?: '1').trim()
    return (normalized ==~ /^\d+$/) ? (normalized as int) : 1
}

def runShell(String unixCommand, String windowsCommand) {
    if (isUnix()) {
        sh(unixCommand)
    } else {
        bat(windowsCommand)
    }
}

def clearReportDirectories() {
    cleanDirs(['reports', env.ALLURE_DIR])
    setupReports()
}

def cleanDirs(List dirs) {
    def normalized = dirs.findAll { it?.trim() }
    if (normalized.isEmpty()) return

    if (isUnix()) {
        sh """
            for path in ${normalized.collect { "'${it}'" }.join(' ')}; do
                if [ -e "\$path" ]; then
                    rm -rf "\$path"
                fi
            done
        """
    } else {
        normalized.each { d ->
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
        "mkdir -p reports ${env.ALLURE_DIR}",
        """
            if not exist "reports" mkdir "reports"
            if not exist "${env.ALLURE_DIR}" mkdir "${env.ALLURE_DIR}"
        """
    )
}

def parseTestSelection(String separator = ' | ') {
    def parts = []
    if (params.TEST_SUITE?.trim() && params.TEST_SUITE != 'all') {
        def suites = params.TEST_SUITE.split(',').collect { it.trim() }.findAll { it && it != 'all' }
        if (suites) {
            parts << "Suites: ${suites.join(', ')}"
        }
    }
    def selectedMarkers = getTabCheckboxMap()
        .findAll { row -> (params."${row.param}" as boolean) }
        .collect { row -> row.marker }
        .unique()
    if (selectedMarkers) {
        parts << "Tabs: ${selectedMarkers.join(', ')}"
    }
    parts << "Browser: ${(params.BROWSER ?: 'chrome').trim().toLowerCase()}"
    parts << "Workers: ${(params.PARALLEL_WORKERS ?: '1').trim()}"
    return parts ? parts.join(separator) : 'All Tests'
}

def parseSuites(String testSuite) {
    if (!testSuite?.trim()) return []
    return testSuite
        .split(',')
        .collect { it.trim() }
        .findAll { it && it != 'all' }
        .collect { mapSuiteDisplayToInternal(it) }
        .unique()
}

def mapSuiteDisplayToInternal(String displayName) {
    def mapping = [
        'all'                            : 'all',
        'Column Names Validation'        : 'column_names',
        'Fields Comparison'              : 'fields_comparison',
        'Fields Display Functionality'   : 'fields_display',
        'Lazy Loading'                   : 'lazy_loading',
        'List View CRUD Operations'      : 'list_view_crud',
        'Pin/Unpin Functionality'        : 'pin_unpin'
    ]
    return mapping.get(displayName, displayName)
}

def getTestPath(String testSuite) {
    def paths = [
        'all'              : 'tests/',
        'column_names'     : 'tests/all_tabs_column_name/',
        'fields_comparison': 'tests/all_tabs_fields_comparison/',
        'fields_display'   : 'tests/all_tabs_fields_display_functionality/',
        'lazy_loading'     : 'tests/all_tabs_lazy_loading/',
        'list_view_crud'   : 'tests/all_tabs_list_view_crud/',
        'pin_unpin'        : 'tests/all_tabs_pin_unpin_functionality/'
    ]
    return paths.get(testSuite, 'tests/')
}

// FIX 3 + FIX 9: getTestStatistics() now also computes and returns passRate,
//                 so the email function does not need to re-calculate it.
def getTestStatistics() {
    def stats = [total: 0, passed: 0, failed: 0, skipped: 0, passRate: 0.0]
    def jsonFile = env.PYTEST_JSON ?: 'reports/report.json'

    if (!fileExists(jsonFile)) {
        echo "pytest JSON report not found at '${jsonFile}'. Returning empty stats."
        return stats
    }

    try {
        def report  = readJSON file: jsonFile
        def summary = (report?.summary instanceof Map) ? report.summary : [:]

        stats.passed  = parseSummaryValue(summary, 'passed')
        stats.failed  = parseSummaryValue(summary, 'failed') + parseSummaryValue(summary, 'error')
        stats.skipped = parseSummaryValue(summary, 'skipped') +
                        parseSummaryValue(summary, 'xfailed') +
                        parseSummaryValue(summary, 'xpassed')
        stats.total   = stats.passed + stats.failed + stats.skipped

        // FIX 9: Centralised pass-rate calculation
        if (stats.total > 0) {
            double raw = ((stats.passed as double) * 1000.0d) / (stats.total as double)
            stats.passRate = ((Math.round(raw) as long) / 10.0d)
        }

        echo "pytest stats: total=${stats.total} passed=${stats.passed} failed=${stats.failed} skipped=${stats.skipped} passRate=${stats.passRate}%"
    } catch (MissingMethodException e) {
        echo "Pipeline Utility Steps readJSON not available: ${e.getMessage()}"
        echo "Install/enable the Pipeline Utility Steps plugin to improve report parsing."
    } catch (Exception e) {
        echo "Error parsing pytest JSON report: ${e.getMessage()}"
    }

    return stats
}

def parseSummaryValue(Map summary, String key) {
    def raw = summary?."${key}"
    if (raw == null) return 0
    if (raw instanceof Number) return (raw as Number).intValue()
    def normalized = raw.toString().trim()
    return (normalized ==~ /^\d+$/) ? (normalized as int) : 0
}

def collectRecipientEmails(String defaultEmail, String additionalEmails) {
    def recipients = []
    def seen       = [] as Set
    [defaultEmail, additionalEmails].findAll { it?.trim() }.each { source ->
        source.split(/[,\s;]+/).collect { it.trim() }.findAll { it }.each { mail ->
            def key = mail.toLowerCase()
            if (!seen.contains(key)) {
                seen.add(key)
                recipients.add(mail)
            }
        }
    }
    return recipients
}

// FIX 3: Accepts pre-computed testStats so the JSON is never read twice.
def sendEmailNotification(String buildStatus, Map testStats) {
    def recipients = collectRecipientEmails(params.DEFAULT_EMAIL as String, params.ADDITIONAL_EMAILS as String)
    if (recipients.isEmpty() && env.EMAIL_RECIPIENT?.trim()) {
        recipients = [env.EMAIL_RECIPIENT]
    }
    if (recipients.isEmpty()) {
        echo "No recipients configured, skipping email."
        return
    }

    def subject      = "Dakota Regression Test Report | ${new Date().format('MMM dd, yyyy')}"
    def durationStr  = (currentBuild.durationString ?: 'N/A').replace(' and counting', '')

    // FIX 9: passRate already on testStats — no recalculation needed
    def passRate       = testStats.passRate
    def passRateColor  = passRate >= 90 ? '#16a34a' : (passRate >= 70 ? '#f59e0b' : '#dc2626')
    def healthLabel    = passRate >= 90 ? 'Healthy'  : (passRate >= 70 ? 'Degraded' : 'Critical')
    def healthBg       = passRate >= 90 ? '#dcfce7'  : (passRate >= 70 ? '#fef3c7'  : '#fee2e2')
    def healthBorder   = passRate >= 90 ? '#86efac'  : (passRate >= 70 ? '#fcd34d'  : '#fca5a5')

    def environmentLabel = ((params.ENVIRONMENT ?: 'UAT').toUpperCase() == 'PROD') ? 'Production' : 'UAT'
    def jobUrl           = env.BUILD_URL ?: ''
    def allureUrl        = "${jobUrl}allure"
    def allureAvailable  = params.RUN_ALLURE && fileExists(env.ALLURE_DIR)

    def body = """
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body style="margin:0;padding:0;background:#eef2f7;font-family:'Trebuchet MS','Segoe UI',Arial,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="padding:22px 10px;background:linear-gradient(135deg,#eaf0fb 0%,#f8fafd 100%);">
      <tr>
        <td align="center">
          <table width="100%" cellpadding="0" cellspacing="0" style="max-width:700px;background:#ffffff;border-radius:26px;overflow:hidden;box-shadow:0 24px 60px rgba(15,23,42,0.14);">

            <!-- HERO -->
            <tr>
              <td style="padding:0;background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 45%,#0ea5e9 100%);">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding:28px 26px;">
                      <h1 style="margin:0;color:#ffffff;font-size:30px;line-height:1.2;font-weight:900;">
                        Dakota Regression Test Results
                      </h1>
                      <p style="margin:8px 0 0;color:#bfdbfe;font-size:13px;">
                        ${environmentLabel} &nbsp;·&nbsp; ${params.PORTAL ?: 'All Marketplace Access'} &nbsp;·&nbsp; ${new Date().format('MMM dd, yyyy HH:mm')}
                      </p>
                    </td>
                    <td align="right" style="padding:28px 26px;white-space:nowrap;">
                      <span style="display:inline-block;padding:6px 14px;background:${healthBg};border:1px solid ${healthBorder};border-radius:20px;font-size:12px;font-weight:800;color:${passRateColor};">
                        ${healthLabel}
                      </span>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- KPI STATS -->
            <tr>
              <td style="padding:16px 16px 4px;">
                <table width="100%" cellpadding="6" cellspacing="6">
                  <tr>
                    <td width="25%" style="background:#f4f7fb;border:1px solid #dbe3ef;border-radius:14px;padding:14px 12px;">
                      <div style="font-size:10px;color:#64748b;font-weight:800;letter-spacing:0.8px;">TOTAL TESTS</div>
                      <div style="margin-top:6px;font-size:28px;font-weight:900;color:#0f172a;">${testStats.total}</div>
                    </td>
                    <td width="25%" style="background:#ecfaf3;border:1px solid #c9efdc;border-radius:14px;padding:14px 12px;">
                      <div style="font-size:10px;color:#15803d;font-weight:800;letter-spacing:1px;">PASSED</div>
                      <div style="margin-top:6px;font-size:28px;font-weight:900;color:#15803d;">${testStats.passed}</div>
                    </td>
                    <td width="25%" style="background:#fef2f2;border:1px solid #f6cdd2;border-radius:14px;padding:14px 12px;">
                      <div style="font-size:10px;color:#b91c1c;font-weight:800;letter-spacing:1px;">FAILED</div>
                      <div style="margin-top:6px;font-size:28px;font-weight:900;color:#b91c1c;">${testStats.failed}</div>
                    </td>
                    <td width="25%" style="background:#f5f1ff;border:1px solid #dfd3ff;border-radius:14px;padding:14px 12px;">
                      <div style="font-size:10px;color:#7c3aed;font-weight:800;letter-spacing:1px;">SKIPPED</div>
                      <div style="margin-top:6px;font-size:28px;font-weight:900;color:#7c3aed;">${testStats.skipped}</div>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- DETAILS + ALLURE -->
            <tr>
              <td style="padding:10px 16px 18px;">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <!-- Execution details -->
                    <td width="54%" valign="top">
                      <table width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;">
                        <tr>
                          <td colspan="2" style="padding:14px 16px;background:#020617;color:#ffffff;">
                            <div style="font-size:15px;font-weight:900;">Execution Details</div>
                          </td>
                        </tr>
                        <tr>
                          <td style="padding:11px 14px;font-size:11px;font-weight:800;color:#1d4ed8;background:#f8fbff;border-bottom:1px dashed #cbd5e1;">Environment</td>
                          <td align="right" style="padding:11px 14px;font-size:12px;font-weight:800;color:#0f172a;background:#f8fbff;border-bottom:1px dashed #cbd5e1;">${environmentLabel}</td>
                        </tr>
                        <tr>
                          <td style="padding:11px 14px;font-size:11px;font-weight:800;color:#7c3aed;background:#f5f3ff;border-bottom:1px dashed #cbd5e1;">Portal</td>
                          <td align="right" style="padding:11px 14px;font-size:12px;font-weight:800;color:#0f172a;background:#f5f3ff;border-bottom:1px dashed #cbd5e1;">${params.PORTAL ?: 'All Marketplace Access'}</td>
                        </tr>
                        <tr>
                          <td style="padding:11px 14px;font-size:11px;font-weight:800;color:#15803d;background:#ecfdf5;border-bottom:1px dashed #cbd5e1;">Duration</td>
                          <td align="right" style="padding:11px 14px;font-size:12px;font-weight:800;color:#0f172a;background:#ecfdf5;border-bottom:1px dashed #cbd5e1;">${durationStr}</td>
                        </tr>
                        <tr>
                          <td style="padding:11px 14px;font-size:11px;font-weight:800;color:#b45309;background:#fffbeb;border-bottom:1px dashed #cbd5e1;">Browser</td>
                          <td align="right" style="padding:11px 14px;font-size:12px;font-weight:800;color:#0f172a;background:#fffbeb;border-bottom:1px dashed #cbd5e1;">${(params.BROWSER ?: 'chrome').toLowerCase()}</td>
                        </tr>
                        <tr>
                          <td style="padding:11px 14px;font-size:11px;font-weight:800;color:#b45309;background:#fffbeb;">Pass Rate</td>
                          <td align="right" style="padding:11px 14px;font-size:12px;font-weight:900;color:${passRateColor};background:#fffbeb;">${passRate}%</td>
                        </tr>
                      </table>
                    </td>

                    <!-- Allure card -->
                    <td width="46%" valign="top" style="padding-left:8px;">
                      <table width="100%" cellpadding="0" cellspacing="0" style="background:linear-gradient(135deg,#020617 0%,#0f172a 45%,#1d4ed8 100%);border-radius:16px;overflow:hidden;height:100%;">
                        <tr>
                          <td style="padding:18px 16px;">
                            <div style="color:#ffffff;font-size:24px;font-weight:900;line-height:1.3;">Allure Report</div>
                            <div style="margin-top:6px;color:#dbeafe;font-size:12px;line-height:1.6;">
                              Complete execution analytics, screenshots, logs, failed validations, and test evidence.
                            </div>
                            <div style="margin-top:16px;">
                              ${allureAvailable
                                ? "<a href=\"${allureUrl}\" style=\"display:inline-block;background:#ffffff;color:#0f172a;text-decoration:none;padding:10px 16px;border-radius:10px;font-size:11px;font-weight:900;letter-spacing:0.7px;\">OPEN REPORT &rarr;</a>"
                                : "<span style=\"display:inline-block;background:rgba(255,255,255,0.16);color:#ffffff;padding:10px 16px;border-radius:10px;font-size:10px;font-weight:800;\">REPORT NOT AVAILABLE</span>"
                              }
                            </div>
                            <div style="margin-top:14px;">
                              <a href="${jobUrl}" style="color:#93c5fd;font-size:11px;text-decoration:underline;">View Jenkins Build</a>
                            </div>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- FOOTER -->
            <tr>
              <td style="background:#000000;border-top:1px solid #111827;padding:12px 16px;">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="color:#ffffff;font-size:11px;font-weight:800;">Dakota Marketplace Automation</td>
                    <td align="right" style="color:#6b7280;font-size:11px;">Build #${env.BUILD_NUMBER ?: 'N/A'}</td>
                  </tr>
                </table>
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
        subject : subject,
        body    : body,
        mimeType: 'text/html',
        to      : recipients.join(', ')
    )
}