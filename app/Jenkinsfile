pipeline {
    agent any

    environment {
        AWS_REGION       = 'ap-south-1'
        AWS_ACCOUNT_ID   = '343218198881'
        ECR_REPOSITORY   = 'testwebsite'
        ECR_REGISTRY     = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG        = "${env.BUILD_ID}"
        IMAGE_URI        = "${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
        CREDENTIALS_ID   = 'aws-ecr-cred'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Spike741/chatbot.git'
            }
        }

       // stage('Build and Test Python App') {
         //   steps {
           //     bat 'python --version'
             //   bat 'pip install --upgrade pip'
               // bat 'pip install -r requirements.txt'
                // Optional: Add Python linting or unit tests here
                // bat 'pytest'  // if you have tests
           // }
      //  }

        stage('Configure AWS Credentials') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.CREDENTIALS_ID}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        bat "aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%"
                        bat "aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%"
                        bat "aws configure set default.region ${env.AWS_REGION}"
                        bat 'aws sts get-caller-identity'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def dockerImage = docker.build("${env.IMAGE_URI}")
                }
            }
        }

        stage('Login to ECR and Push Image') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.CREDENTIALS_ID}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        bat """
                        aws ecr get-login-password --region ${env.AWS_REGION} | docker login --username AWS --password-stdin ${env.ECR_REGISTRY}
                        """
                        def dockerImage = docker.image("${env.IMAGE_URI}")
                        dockerImage.push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! Docker image pushed to ECR.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for errors.'
        }
    }
}
