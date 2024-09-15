pipeline {
    agent any


   parameters {
        choice(name: 'BRANCH_NAME', choices: ['main', 'pyspark', 'feature-branch'], description: 'Select the branch to build')
    }

    environment {
        CLUSTER_USER = 'ilaya' // Replace with your cluster username
        CLUSTER_HOST = '192.168.18.139' // Replace with your cluster IP or domain
        TARGET_DIR = '/home/ilaya/jenkins_test/' // Replace with the target directory on your cluster
        SSH_CREDENTIALS_ID = 'a6026357-ee3d-4415-9c8a-4f392a72b161' // Replace with your SSH credentials ID
    }

    stages {
        stage('Clone repository') {
            steps {
                // Clone your GitHub repository
                git branch: 'pyspark', url: 'https://github.com/ilayabharathispark/pyspark.git'
            }
        }

        stage('Add Host Key') {
            steps {
                script {
                    sh """
                    # Add the cluster's host key to the known_hosts file
                    ssh-keyscan -H ${CLUSTER_HOST} >> ~/.ssh/known_hosts
                    """
                }
            }
        }

        stage('Deploy DAG and Script') {
            steps {
                sshagent([SSH_CREDENTIALS_ID]) {
                    sh """
                    # Create target directories on the cluster if they don't exist
                    ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'mkdir -p ${TARGET_DIR}/dag'
                    ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'mkdir -p ${TARGET_DIR}/script'

                    # Copy the 'dag' and 'script' folders from the Jenkins workspace to the cluster
                    scp -r ${WORKSPACE}/dags ${CLUSTER_USER}@${CLUSTER_HOST}:${TARGET_DIR}/dag
                    scp -r ${WORKSPACE}/scripts ${CLUSTER_USER}@${CLUSTER_HOST}:${TARGET_DIR}/script
                    """
                }
            }
        }
    }
}
