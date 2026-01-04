pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning the GitHub repo...'
                git branch: 'main', url: 'https://github.com/qadri625/fare-calculator.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                sh 'docker build -t fare-calculator:latest .'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests inside Docker container'
                sh 'docker run --rm fare-calculator:latest python3 -m unittest discover'
            }
        }

        stage('Run App') {
            steps {
                echo 'Running Docker container'
                sh 'docker run -d -p 5005:5005 fare-calculator:latest'
            }
        }
    }
}

