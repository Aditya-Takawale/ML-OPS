pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "sincere-blade-454507-s9"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        IMAGE_NAME = "gcr.io/${GCP_PROJECT}/hotel-res-pred:latest"
    }

    stages {
        
        stage('Cloning Github Repo') {
            steps {
                echo 'Cloning repository from GitHub...'
                checkout scmGit(
                    branches: [[name: '*/main']], 
                    extensions: [], 
                    userRemoteConfigs: [[
                        credentialsId: 'github-token', 
                        url: 'https://github.com/kunjesh04/Hotel-Reservation-Prediction.git'
                    ]]
                )
            }
        }
        
        stage('Setting up Virtual Environment') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh '''
                python -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        
        stage('Building and Pushing Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Authenticating with Google Cloud...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        echo 'Building Docker Image...'
                        docker build -t ${IMAGE_NAME} .

                        echo 'Pushing Docker Image to GCR...'
                        docker push ${IMAGE_NAME}
                        '''
                    }
                }
            }
        }

        stage('Deploying to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying to Google Cloud Run...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy hotel-res-pred \
                            --image=${IMAGE_NAME} \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Deployment Successful! Hotel Reservation Prediction App is live.'
        }
        failure {
            echo '❌ Deployment Failed! Check Jenkins logs for details.'
        }
        always {
            echo '📝 Pipeline execution complete.'
        }
    }
}
