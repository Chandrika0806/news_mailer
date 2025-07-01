pipeline {
    agent any

    environment {
        // Example: put secret IDs here if needed later
        // NEWS_API = credentials('newsapi-key')
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Cloning repository...'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Script') {
            steps {
                sh 'python app.py'
            }
        }
    }
}
