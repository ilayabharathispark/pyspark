
pipeline {
    agent any

    environment {
        // Define variables for your cluster and paths
        TARGET_DIR = '/home/ilaya/jenkins_test/' // Change to your target directory
        CLUSTER_USER = 'ilaya' // Username for SSH
        CLUSTER_HOST = '192.168.18.139' // IP or domain of the cluster
        SSH_CREDENTIALS_ID = '01b9f900-2d73-4175-836d-2ba89f99d2de' // Jenkins SSH credentials ID
    }

    stages {
        stage('Clone repository') {
            steps {
                // Clone your GitHub repository
                git branch: 'pyspark', url: 'https://github.com/ilayabharathispark/pyspark.git'
            }
        }

        stage('Deploy DAG and Script') {
            steps {
                // SSH and SCP commands to transfer the folders to your Hadoop cluster
                sshagent(['SSH_CREDENTIALS_ID']) {
                    sh """
                    # Create target directories on the cluster if they don't exist
                    ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'mkdir -p ${TARGET_DIR}/dag'
                    ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'mkdir -p ${TARGET_DIR}/script'

                    # Copy the 'dag' and 'script' folders from the Jenkins workspace to the cluster
                    scp -r ${WORKSPACE}/dag ${CLUSTER_USER}@${CLUSTER_HOST}:${TARGET_DIR}/dag
                    scp -r ${WORKSPACE}/script ${CLUSTER_USER}@${CLUSTER_HOST}:${TARGET_DIR}/script
                    """
                }
            }
        }
    }
}






















