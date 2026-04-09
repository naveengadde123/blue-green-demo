pipeline {
    agent any

    environment {
        IMAGE = "bluegreen-app"
    }

    stages {

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Check Current Live') {
            steps {
                script {
                    def blueRunning = sh(script: "docker ps -q -f name=blue-container", returnStdout: true).trim()
                    if (blueRunning) {
                        env.CURRENT = "blue"
                    } else {
                        env.CURRENT = "green"
                    }
                    echo "Current running: ${env.CURRENT}"
                }
            }
        }

        stage('Deploy New Version') {
            steps {
                script {
                    if (env.CURRENT == "blue") {
                        // Deploy GREEN
                        sh '''
                        docker rm -f green-container || true
                        docker run -d -p 5002:5000 -e VERSION=GREEN --name green-container bluegreen-app
                        '''
                    } else {
                        // Deploy BLUE
                        sh '''
                        docker rm -f blue-container || true
                        docker run -d -p 5001:5000 -e VERSION=BLUE --name blue-container bluegreen-app
                        '''
                    }
                }
            }
        }

        stage('Switch Traffic') {
            steps {
                script {
                    if (env.CURRENT == "blue") {
                        // Switch to GREEN
                        sh '''
                        echo "server {
                            listen 80;
                            location / {
                                proxy_pass http://127.0.0.1:5002;
                            }
                        }" | sudo tee /etc/nginx/sites-available/default
                        '''
                    } else {
                        // Switch to BLUE
                        sh '''
                        echo "server {
                            listen 80;
                            location / {
                                proxy_pass http://127.0.0.1:5001;
                            }
                        }" | sudo tee /etc/nginx/sites-available/default
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