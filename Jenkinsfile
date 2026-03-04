pipeline {
    agent {
        kubernetes {
            label "moria"
            idleMinutes 5
            yamlFile "build-pod.yaml"
            defaultContainer "ez-docker-helm-build" 
        }
    }
    environment {
        DOCKER_IMAGE = "moria3/project_image"
        GITLAB_URL = "https://gitlab.com"
        PROJECT_ID = "58661381"
    }
    stages {
        stage("checkout") {
            steps {
                checkout scm
            }
        }
        stage("building docker image") {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:latest --no-cache ."
                }
            }
        }
        stage("push docker image") {
            when {
                branch "main"
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        sh "docker tag ${DOCKER_IMAGE}:latest ${DOCKER_IMAGE}"
                        sh "docker push ${DOCKER_IMAGE}"
                    }
                }
            }
        }
        stage("Create Merge Request") {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'gitlab-api', variable: 'GITLAB_API_TOKEN')]) {
                        def branchName = env.BRANCH_NAME
                        sh """
                            curl -s -o response.json -w "%{http_code}" --header "PRIVATE-TOKEN: \${GITLAB_API_TOKEN}" -X POST "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/merge_requests" \\
                            --form "source_branch=${branchName}" \\
                            --form "target_branch=main" \\
                            --form "title=MR from ${branchName} into main" \\
                            --form "remove_source_branch=true"
                        """
                        def responseCode = readFile('response.json').trim()
                        if (responseCode.startsWith("20")) {
                            echo "Merge request created successfully."
                        }
                    }
                }
            }
        }
    }
}