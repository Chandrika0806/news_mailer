pipeline {
    agent any

    stages {
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
