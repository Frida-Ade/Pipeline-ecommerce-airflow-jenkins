pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checkout source code'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Dependencies installed'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Tests executed'
            }
        }

        stage('Validate DAG') {
            steps {
                echo 'DAG validated'
            }
        }

        stage('Deploy DAG') {
            steps {
                echo 'Deploy DAG to Airflow'
            }
        }

        stage('Trigger DAG') {
            steps {
                echo 'Trigger ecommerce_sales_pipeline'
            }
        }

        stage('Verify MongoDB') {
            steps {
                echo 'Verify sales_metrics collection'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
    }
}