pipeline{
    agent any 

    environment {
        VENV_DIR = 'venv'

    }

    stages{

        stage("Cloning code from Github ...."){
            steps{
                script{
                    echo 'Cloning from Github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/igamelinia/Game-Recommendation-System.git']])
                }
            }
        }

        stage("Build Virtual Environment ...."){
            steps{
                script{
                    echo 'Build Virtual Environment...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc 
                    '''
                }
            }
        }


        stage("DVC pull .."){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'DVC pull ...'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull \
                        artifacts/weights

                        '''
                    }
                }
            }
        }



        
    }


}