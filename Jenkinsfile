pipeline {
    agent any

    environment {
        BLUE_PORT = "3000"
        GREEN_PORT = "3001"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'npm install'
            }
        }

        stage('Deploy to GREEN') {
            steps {
                echo "Deploying to GREEN..."

                bat '''
                set PORT=%GREEN_PORT%
                start /B node app.js
                '''
            }
        }

        stage('Test GREEN') {
            steps {
                echo "Testing GREEN..."

                bat '''
                curl http://localhost:%GREEN_PORT%
                '''
            }
        }

        stage('Switch Traffic') {
            steps {
                echo "Switching traffic to GREEN..."

                echo "Now GREEN is LIVE on port 3001"
            }
        }
    }
}