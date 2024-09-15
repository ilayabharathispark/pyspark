
pipeline {
    agent any

    environment {
        // Define your environment variables here if needed
        CLUSTER_PATH = '/home/ilaya/jenkins_test/'
        REPO_URL = 'https://github.com/ilayabharathispark/pyspark.git'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
                git url: "${env.REPO_URL}", branch: 'pyspark'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Define the paths for `dags` and `script` folders
                    def dagsPath = "${env.WORKSPACE}/dags"
                    def scriptPath = "${env.WORKSPACE}/script"

                    // Deploy `dags` folder
                    sh "rsync -avz ${dagsPath}/ ilaya@192.168.18.139:${env.CLUSTER_PATH}/dags/"

                    // Deploy `script` folder
                    sh "rsync -avz ${scriptPath}/ ilaya@192.168.18.139:${env.CLUSTER_PATH}/script/"
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully.'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}























