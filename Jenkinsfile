pipeline {
    agent {label 'Built-In Node'}

    environment {
        AWS_REGION       = 'ap-south-1'
        AWS_ACCOUNT_ID   = '343218198881'
        ECR_REPOSITORY   = 'testwebsite'
        ECR_REGISTRY     = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG        = '1'
        IMAGE_URI        = "${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
        CREDENTIALS_ID   = 'aws-ecr-cred'
        IMAGE_ID         = ''
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Spike741/chatbot_with_docker.git'
            }
        }

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

        stage('Delete Existing Image in ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.CREDENTIALS_ID}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        // Try to delete the image with tag '1' if it exists
                        bat """
                        aws ecr batch-delete-image --repository-name ${env.ECR_REPOSITORY} --image-ids imageTag=${env.IMAGE_TAG} || exit 0
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the image and tag as '1'
                    bat "docker build -t ${env.IMAGE_URI} ."
                    // Get the image ID of the just-built image and store in env.IMAGE_ID
                    def imageId = bat(script: "docker images --format \"{{.ID}}\" ${env.IMAGE_URI}", returnStdout: true).trim()
                    env.IMAGE_ID = imageId
                    echo "Built image ID: ${env.IMAGE_ID}"
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
                        bat "docker push ${env.IMAGE_URI}"
                    }
                }
            }
        }
    }

    post {
    success {
        echo 'Pipeline completed successfully! Triggering second pipeline now.'
        build job: 'docker_2', wait: false
    }
    failure {
        echo 'Pipeline failed! Second pipeline will NOT run.'
    }
}
}    
    

