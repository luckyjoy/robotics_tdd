pipeline {
    agent any

    environment {
        PYTHON = 'python3'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                ${PYTHON} -m pip install --upgrade pip
                ${PYTHON} -m pip install -r requirements.txt
                ${PYTHON} -m pip install pytest pytest-cov flake8
                '''
            }
        }

        stage('Lint') {
            steps {
                sh 'flake8 src tests'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest -m sim --cov=src --cov-report=xml -v'
            }
        }

        stage('Publish Reports') {
            steps {
                junit '**/test-results.xml' allowEmptyResults: true
                publishCoverage adapters: [coberturaAdapter('coverage.xml')]
            }
        }
    }
}
