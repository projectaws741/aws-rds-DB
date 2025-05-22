pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "projectaws/aws-rds-db"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKERFILE_PATH = "db-app/Dockerfile"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -f ${DOCKERFILE_PATH} ."
            }
        }
        stage('Verify Docker Access') {
            steps {
                sh 'whoami && groups && docker ps'
            }
        }
        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo "✅ Docker image pushed: ${DOCKER_IMAGE}:${IMAGE_TAG}"
        }
        failure {
            echo "❌ Build failed. Check the logs."
        }
    }
}
