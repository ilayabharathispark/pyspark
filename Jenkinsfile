
pipeline {
    agent any

    environment {
        // Define variables for your cluster and paths
        TARGET_DIR = '/home/ilaya/jenkins_test/' // Change to your target directory
        CLUSTER_USER = 'ilaya' // Username for SSH
        CLUSTER_HOST = '192.168.18.139' // IP or domain of the cluster
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
                 script {
                    sh """
                    # Create target directories on the cluster if they don't exist
                    sshpass -p 'your-cluster-password' ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'mkdir -p ${TARGET_DIR}/dag'
                    sshpass -p 'your-cluster-password' ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'mkdir -p ${TARGET_DIR}/script'

                    # Copy the 'dag' and 'script' folders from the Jenkins workspace to the cluster
                    sshpass -p 'your-cluster-password' scp -r ${WORKSPACE}/dag ${CLUSTER_USER}@${CLUSTER_HOST}:${TARGET_DIR}/dag
                    sshpass -p 'your-cluster-password' scp -r ${WORKSPACE}/script ${CLUSTER_USER}@${CLUSTER_HOST}:${TARGET_DIR}/script
                    """
                }
            }
        }
    }
}






















