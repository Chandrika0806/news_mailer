pipeline {
    agent any

    triggers {
        cron('0 7,14,20 * * *')  // 7 AM, 2 PM, 8 PM daily
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
