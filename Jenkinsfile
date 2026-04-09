pipeline {
    agent any

    environment {
        IMAGE = "bluegreen-app"
        BLUE = "blue-container"
        GREEN = "green-container"
    }

    stages {

        stage('Clone Code') {
            steps {
                git 'https://github.com/naveengadde123/blue-green-demo'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Deploy Green') {
            steps {
                sh '''
                docker stop $GREEN || true
                docker rm $GREEN || true
                docker run -d -p 5002:5000 --name $GREEN $IMAGE
                '''
            }
        }

        stage('Switch Traffic') {
            steps {
                sh '''
                sudo sed -i 's/5001/5002/' /etc/nginx/sites-available/default
                sudo systemctl reload nginx
                '''
            }
        }

        stage('Stop Blue') {
            steps {
                sh '''
                docker stop $BLUE || true
                docker rm $BLUE || true
                '''
            }
        }
    }
}