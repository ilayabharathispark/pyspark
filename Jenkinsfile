pipeline {
    agent any


   parameters {
        choice(name: 'BRANCH_NAME', choices: ['main', 'pyspark', 'feature-branch'], description: 'Select the branch to build')
    }

    gitParameter(
                branchFilter: 'origin/(.*)',
                defaultVaule: 'pyspark',
                name: 'BRANCH',
                type:'PT_BRANCH',
                selectedValues:'DEFAULT',
                sortMode:'ASCENDING_SMART',
                description: 'Select Branch',
                useRepostories: 'https://github.com/ilayabharathispark/pyspark.git'

                 )

    environment {
        CLUSTER_USER = 'ilaya' // Replace with your cluster username
        CLUSTER_HOST = '192.168.18.139' // Replace with your cluster IP or domain
        DAG_TARGET_DIR = '/home/ilaya/airflow/' // Replace with the DAG_TARGET_DIR on your cluster
        PYSPARK_SCRIPT_TARGET_DIR = '/home/ilaya/pyspark/' // Replace with the PYSPARK_SCRIPT_TARGET_DIR on your cluster
        SSH_CREDENTIALS_ID = 'a6026357-ee3d-4415-9c8a-4f392a72b161' // Replace with your SSH credentials ID
    }

    stages {
        stage('Clone repository') {
            steps {
                script {
                    def branchName = params.BRANCH_NAME
                    // Clone the selected branch from your GitHub repository
                    git branch: branchName, url: 'https://github.com/ilayabharathispark/pyspark.git'
                }
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
                    ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'mkdir -p ${DAG_TARGET_DIR}/dags'
                    ssh ${CLUSTER_USER}@${CLUSTER_HOST} 'mkdir -p ${PYSPARK_SCRIPT_TARGET_DIR}/scripts'

                    # Copy the files from 'dag' and 'script' folders from the Jenkins workspace to the cluster
                    scp -r ${WORKSPACE}/dags/* ${CLUSTER_USER}@${CLUSTER_HOST}:${DAG_TARGET_DIR}/dags
                    scp -r ${WORKSPACE}/scripts/* ${CLUSTER_USER}@${CLUSTER_HOST}:${PYSPARK_SCRIPT_TARGET_DIR}/scripts
                    """
                }
            }
        }
    }
}
