// Jenkinsfile
// Pipeline: GitHub commit -> Jenkins build -> Docker image -> push to DockerHub
//
// IMPORTANT - before running this in Jenkins:
// 1. Replace YOUR_DOCKERHUB_USERNAME below with your real DockerHub username.
// 2. In Jenkins, create a credential of kind "Username with password"
//    with the ID exactly:  dockerhub-credentials
//    Username = your DockerHub username
//    Password = a DockerHub Access Token (not your DockerHub login password)

pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = "YOUR_DOCKERHUB_USERNAME/junaid-cicd-demo"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Junaid - Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build \
                          --build-arg BUILD_NUMBER=${BUILD_NUMBER} \
                          --build-arg BUILD_TIME=\$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
                          -t ${IMAGE_NAME}:${IMAGE_TAG} \
                          -t ${IMAGE_NAME}:latest \
                          .
                    """
                }
            }
        }

        stage('Junaid - Login to Dockerhub') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                '''
            }
        }

        stage('Junaid - Push Image to Dockerhub') {
            steps {
                sh """
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
        success {
            echo "Pipeline succeeded. Image pushed as ${IMAGE_NAME}:${IMAGE_TAG} and ${IMAGE_NAME}:latest"
        }
        failure {
            echo "Pipeline failed. Check the stage logs above for the error."
        }
    }
}
