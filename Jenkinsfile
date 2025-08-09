pipeline{
    agent any 

    stages{

        stage("Cloning code from Github ...."){
            steps{
                script{
                    echo 'Cloning from Github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/igamelinia/Game-Recommendation_System.git']])
                }
            }
        }
    }


}