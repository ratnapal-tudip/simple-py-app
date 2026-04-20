pipeline {
    agent any

    environment {
        PROJECT_ID = 'ratnapal-project'
        REGION = 'us-central1'
        REPO = 'py-app-registry'
        IMAGE = 'py-app'
        VM_IP = '136.119.177.244'
    }

    stages {

        stage('Build') {
            steps {
                sh 'docker build -t py-app .'
            }
        }
        
        stage('Debug Credentials') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'FILE')]) {
                    sh 'ls -l $FILE'
                }
            }
        }


        stage('Auth to GCP') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                    gcloud auth configure-docker $REGION-docker.pkg.dev -q
                    '''
                }
            }
        }

        stage('Tag & Push') {
            steps {
                sh '''
                docker tag py-app $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest
                docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest
                '''
            }
        }

        stage('Deploy to VM') {
            steps {
                sshagent(['vm-ssh-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ratnapal@$VM_IP '
                    
                    docker pull $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest &&
                    
                    docker stop py-app || true &&
                    docker rm -f py-app || true &&
                    
                    docker run -d -p 80:8000 --name py-app \
                    $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest
                    '
                    '''
                }
            }
        }
    

    }
}