pipeline {
    agent any

    environment {
        PYTHON_EXE = "python"
        ALLURE_RESULTS_DIR = "allure-results"
        LINUX_ALLURE_RESULTS_DIR = "linux-allure-results"
        ALLURE_REPORT_DIR = "allure-report-latest"
        ALLURE_HISTORY_DIR = "C:\\ProgramData\\Jenkins\\.jenkins\\jobs\\robotics_tdd\\allure-history"
        PATH = "${env.PATH};${env.USERPROFILE}\\AppData\\Roaming\\npm"
        DOCKER_IMAGE = "python:3.10-slim" // Corrected to use the slim image base for robustness
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                git url: 'https://github.com/luckyjoy/robotics_tdd.git', branch: 'main'
            }
        }

        stage('Install Dependencies (Windows)') {
            steps {
                echo 'Installing required packages on Windows...'
                bat """
                    "%PYTHON_EXE%" -m pip install --upgrade pip
                    if exist requirements.txt "%PYTHON_EXE%" -m pip install -r requirements.txt
                    "%PYTHON_EXE%" -m pip install pytest allure-pytest
                    npm install -g allure-commandline --force
                    where allure >nul 2>nul || (echo Allure CLI not found on PATH. Ensure npm global bin is on PATH & exit /b 1)
                """
            }
        }

        stage('Load Allure History') {
            steps {
                echo "Restoring Allure history..."
                bat """
                    if exist "%ALLURE_RESULTS_DIR%" rd /s /q "%ALLURE_RESULTS_DIR%"
                    mkdir "%ALLURE_RESULTS_DIR%"
                    if exist "%ALLURE_HISTORY_DIR%" xcopy /E /I /Y "%ALLURE_HISTORY_DIR%" "%ALLURE_RESULTS_DIR%\\history" >nul
                """
            }
        }

        stage('Run Pytest (Windows)') {
            steps {
                echo "Running tests with Allure on Windows..."
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    bat "\"%PYTHON_EXE%\" -m pytest -m navigation --alluredir=\"%ALLURE_RESULTS_DIR%\" --capture=tee-sys"
                }
                echo "Windows tests execution complete."
            }
        }

		stage('Run Linux Tests in Docker (PowerShell)') {
			steps {
				catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
					powershell '''
					$ErrorActionPreference = "Stop"

					Write-Host "========================================================="
					Write-Host "Checking Docker service and version..."
					docker version | Out-String | Write-Host
					Write-Host "========================================================="

					# Ensure results dir exists/clean
					if (Test-Path "$env:WORKSPACE\\linux-allure-results") { Remove-Item -Recurse -Force "$env:WORKSPACE\\linux-allure-results" }
					New-Item -ItemType Directory -Force -Path "$env:WORKSPACE\\linux-allure-results" | Out-Null

					Write-Host "========================================================="
					Write-Host "Running Robotics TDD Docker Simulation Tests..."
					Write-Host "Docker Image: $env:DOCKER_IMAGE"
					Write-Host "========================================================="

					# CORRECTED: Simply pull the image. Docker handles the inspection/caching without PowerShell erroring.
					docker pull $env:DOCKER_IMAGE

					docker run --rm -v "$env:WORKSPACE:/tests" -w /tests $env:DOCKER_IMAGE bash -lc \
						"pip install -q pytest allure-pytest && pytest -m navigation --alluredir=/tests/linux-allure-results"
					'''
				}
			}
		}

        stage('Add Allure Metadata') {
            steps {
                script {
                    echo 'Adding Allure metadata (categories, executor, environment)...'

                    def categoriesJson = """[
                        {
                            "name": "Safety Protocol Violation (Hard Stop)",
                            "messageRegex": ".*(ArmError|SafetyViolation|chest height|boundary|RuntimeError: No arm).*",
                            "description": "Failures indicating the robot attempted an unsafe operation.",
                            "matchedStatuses": ["failed", "broken"]
                        },
                        {
                            "name": "Core Logic / Navigation Defect",
                            "messageRegex": ".*(AssertionError|not approximately|less than|greater than|final position).*",
                            "description": "Standard TDD assertion failures.",
                            "matchedStatuses": ["failed"]
                        },
                        {
                            "name": "Simulation Environment or Stability Issue",
                            "messageRegex": ".*(Timeout|ConnectionError|simulated_robot initialization failed).*",
                            "traceRegex": ".*(PyBullet|Gazebo|mocked gripper).*",
                            "description": "Failures related to the simulation engine or hardware connection errors.",
                            "matchedStatuses": ["broken"]
                        }
                    ]""".stripIndent()
                    writeFile file: "${ALLURE_RESULTS_DIR}/categories.json", text: categoriesJson

                    def executorJson = """{
                        "name": "Robotics TDD Framework Runner",
                        "type": "CI_Pipeline",
                        "url": "${env.JENKINS_URL}",
                        "buildOrder": "${env.BUILD_ID}",
                        "buildName": "Robotics TDD #${env.BUILD_ID}",
                        "buildUrl": "${env.BUILD_URL}",
                        "reportUrl": "${env.BUILD_URL}Robotics-TDD-Allure-Report-Build-${env.BUILD_NUMBER}/index.html",
                        "data": {
                            "Validation Engineer": "TBD",
                            "Product Model": "TDD-Sim-PyBullet",
                            "Test Framework": "pytest"
                        }
                    }""".stripIndent()
                    writeFile file: "${ALLURE_RESULTS_DIR}/executor.json", text: executorJson

                    def envProps = """Project=Robotics TDD Simulation Framework
						Author=Bang Thien Nguyen
						Robot Model=Gazebo_Pioneer3DX
						Simulation Engine=PyBullet
						Operating System=Windows 11
						Docker_Image_Name=robotics-runner
						Docker_Build_Context=Repository Root (.)
						Docker_Runtime_Environment=Run Linux Tests in Docker (PowerShell)
						Docker_Key_Role=Provides isolated environment for Pytest and Allure data generation.
						Python Version=3.10.12
						Framework Version=1.0.0
						Test Type=Integration
						HTML Reporter=Allure Test Report 2.35.1
						Build Number=${env.BUILD_NUMBER}
						""".stripIndent()
                    writeFile file: "${ALLURE_RESULTS_DIR}/environment.properties", text: envProps
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo "Generating merged Allure HTML report..."
                bat """
                    if exist "%ALLURE_REPORT_DIR%" rd /s /q "%ALLURE_REPORT_DIR%"
                    mkdir "%ALLURE_REPORT_DIR%"
                    allure generate "%ALLURE_RESULTS_DIR%" "%LINUX_ALLURE_RESULTS_DIR%" -o "%ALLURE_REPORT_DIR%" --clean
                """
                // Persist history for next build
                bat """
                    if exist "%ALLURE_REPORT_DIR%\\history" (
                        if not exist "%ALLURE_HISTORY_DIR%" mkdir "%ALLURE_HISTORY_DIR%"
                        xcopy /E /I /Y "%ALLURE_REPORT_DIR%\\history" "%ALLURE_HISTORY_DIR%" >nul
                    )
                """
            }
        }

        stage('Archive & Publish Allure Report') {
            steps {
                script {
                    echo 'Archiving and publishing Allure report...'
                    archiveArtifacts artifacts: "${ALLURE_REPORT_DIR}/**/*", allowEmptyArchive: true
                    publishHTML(target: [
                        reportName: "Robotics-TDD-Allure-Report-Build-${env.BUILD_NUMBER}-CrossPlatform",
                        reportDir: "${ALLURE_REPORT_DIR}",
                        reportFiles: "index.html",
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    ])
                }
            }
        }
    }

    post {
        always {
            echo "Report (if archived): ${env.BUILD_URL}artifact/${ALLURE_REPORT_DIR}/index.html"
            cleanWs()
            echo "Pipeline finished."
        }
    }
}