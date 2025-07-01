pipeline {
    agent any

    triggers {
        cron('30 7,14,19 * * *')
    }

    stages {
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Send News Mail') {
            steps {
                bat 'python news_sender.py'
            }
        }
    }
}
