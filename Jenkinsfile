pipeline {
    agent any

    environment {
        CLUSTER_USER = 'ilaya'
        CLUSTER_HOST = '192.168.18.139'
        TARGET_DIR = '/home/ilaya/jenkins_test/'
        SSH_CREDENTIALS_ID = 'a6026357-ee3d-4415-9c8a-4f392a72b161'
        GIT_URL = 'https://github.com/ilayabharathispark/pyspark.git'
    }

    stages {
        stage('Retrieve Branches') {
            steps {
                script {
                    def branches = sh(script: "git ls-remote --heads ${GIT_URL} | awk '{print \$2}' | sed 's/refs\\/heads\\///'", returnStdout: true).trim().split('\n')
                    def branchChoices = branches.collect { it }

                    // Store branches in a file to read later for parameterization
                    writeFile file: 'branches.txt', text: branchChoices.join('\n')
                }
            }
        }

        stage('Dynamic Choice Parameter') {
            steps {
                script {
                    def branchChoices = readFile('branches.txt').trim().split('\n')
                    def branchName = input message: 'Select the branch to build', parameters: [choice(name: 'BRANCH_NAME', choices: branchChoices, description: 'Select the branch to build')]

                    env.BRANCH_NAME = branchName
                }
            }
        }

        stage('Clone repository') {
            steps {
                script {
                    // Clone the selected branch from your GitHub repository
                    git branch: "${env.BRANCH_NAME}", url: "${env.GIT_URL}"
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
