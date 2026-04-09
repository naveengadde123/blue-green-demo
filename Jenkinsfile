pipeline {
    agent any

    environment {
        IMAGE = "bluegreen-app"
        BLUE = "blue-container"
        GREEN = "green-container"
        CURRENT = "blue"
    }

    stages {

        stage('Clone Code') {
            steps {
                git 'https://github.com/naveengadde123/blue-green-demo.git'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Check Running Container') {
            steps {
                script {
                    def blueRunning = sh(script: "docker ps -q -f name=blue-container", returnStdout: true).trim()
                    if (blueRunning) {
                        env.CURRENT = "blue"
                    } else {
                        env.CURRENT = "green"
                    }
                }
            }
        }

        stage('Deploy New Version') {
            steps {
                script {
                    if (env.CURRENT == "blue") {
                        sh '''
                        docker stop green-container || true
                        docker rm green-container || true
                        docker run -d -p 5002:5000 --name green-container bluegreen-app
                        '''
                    } else {
                        sh '''
                        docker stop blue-container || true
                        docker rm blue-container || true
                        docker run -d -p 5001:5000 --name blue-container bluegreen-app
                        '''
                    }
                }
            }
        }

        stage('Switch Traffic') {
            steps {
                script {
                    if (env.CURRENT == "blue") {
                        sh '''
                        sudo sed -i 's/5001/5002/' /etc/nginx/sites-available/default
                        '''
                    } else {
                        sh '''
                        sudo sed -i 's/5002/5001/' /etc/nginx/sites-available/default
                        '''
                    }
                    sh 'sudo systemctl reload nginx'
                }
            }
        }

        stage('Remove Old Version') {
            steps {
                script {
                    if (env.CURRENT == "blue") {
                        sh 'docker stop blue-container || true'
                    } else {
                        sh 'docker stop green-container || true'
                    }
                }
            }
        }
    }
}