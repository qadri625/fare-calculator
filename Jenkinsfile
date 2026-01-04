pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fare-calculator'
        CONTAINER_1 = 'fare-app-1'
        CONTAINER_2 = 'fare-app-2'
        PORT_1 = '5005'
        PORT_2 = '5006'
    }

    stages {

        stage('Clean Workspace') {
            steps {
                echo 'Cleaning workspace...'
                deleteDir() // wipes old workspace to avoid conflicts
            }
        }

        stage('Checkout Code') {
            steps {
                echo 'Cloning GitHub repo...'
                git url: 'https://github.com/qadri625/fare-calculator.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Stop Old Containers') {
            steps {
                echo 'Stopping old containers if they exist...'
                sh """
                docker stop ${CONTAINER_1} || true
                docker rm ${CONTAINER_1} || true
                docker stop ${CONTAINER_2} || true
                docker rm ${CONTAINER_2} || true
                """
            }
        }

        stage('Run Containers') {
            steps {
                echo 'Starting new containers...'
                sh """
                docker run -d --name ${CONTAINER_1} -p ${PORT_1}:5005 ${IMAGE_NAME}:latest
                docker run -d --name ${CONTAINER_2} -p ${PORT_2}:5005 ${IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        success {
            echo 'Deployment successful! Both containers are running.'
        }
        failure {
            echo 'Something went wrong during the build/deployment.'
        }
    }
}

