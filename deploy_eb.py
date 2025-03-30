import boto3
import time

# Initialize clients
eb_client = boto3.client('elasticbeanstalk')
s3_client = boto3.client('s3')

# Configuration
APP_NAME = 'cpp-stockmanage'
ENV_NAME = 'cpp-stockmanage-env'
VERSION_LABEL = 'v1.0.0'
S3_BUCKET = 'neerajcppbucket'  # Create this manually first
S3_KEY = 'application.zip'
SOLUTION_STACK = '64bit Amazon Linux 2 v3.3.13 running Python 3.8'
INSTANCE_PROFILE = 'aws-elasticbeanstalk-ec2-role'

def create_s3_bucket(bucket_name):
    """Create an S3 bucket if it doesn’t exist"""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}  
        )
        print(f"Created bucket {bucket_name}")

def create_application(app_name):
    """Create EB application"""
    try:
        eb_client.create_application(
            ApplicationName=app_name,
            Description='My Django Application with SQLite'
        )
        print(f"Created application {app_name}")
    except eb_client.exceptions.TooManyApplicationsException:
        print(f"Application {app_name} already exists")

def create_environment(app_name, env_name, solution_stack):
    """Create EB environment"""
    try:
        eb_client.create_environment(
            ApplicationName=app_name,
            EnvironmentName=env_name,
            SolutionStackName=solution_stack,
            OptionSettings=[
                {
                    'Namespace': 'aws:autoscaling:launchconfiguration',
                    'OptionName': 'InstanceType',
                    'Value': 't2.micro'
                },
                {
                    'Namespace': 'aws:elasticbeanstalk:container:python',
                    'OptionName': 'WSGIPath',
                    'Value': 'stockmanage.wsgi:application'
                },
                {
                    'Namespace': 'aws:elasticbeanstalk:environment:proxy:staticfiles',
                    'OptionName': '/static',
                    'Value': 'staticfiles'
                },
                {
                    'Namespace': 'aws:elasticbeanstalk:application:environment',
                    'OptionName': 'DJANGO_SETTINGS_MODULE',
                    'Value': 'stockmanage.settings'
                }
            ]
        )
        print(f"Creating environment {env_name}")
    except eb_client.exceptions.TooManyEnvironmentsException:
        print(f"Environment {env_name} already exists")

def upload_to_s3(bucket, file_path, key):
    """Upload zip to S3"""
    s3_client.upload_file(file_path, bucket, key)
    print(f"Uploaded {file_path} to s3://{bucket}/{key}")

def create_application_version(app_name, version_label, s3_bucket, s3_key):
    """Create application version"""
    eb_client.create_application_version(
        ApplicationName=app_name,
        VersionLabel=version_label,
        SourceBundle={'S3Bucket': s3_bucket, 'S3Key': s3_key}
    )
    print(f"Created version {version_label}")

def update_environment(app_name, env_name, version_label):
    """Deploy version to environment"""
    eb_client.update_environment(
        ApplicationName=app_name,
        EnvironmentName=env_name,
        VersionLabel=version_label
    )
    print(f"Deploying {version_label} to {env_name}")

def wait_for_environment(env_name):
    """Wait for environment to be ready"""
    while True:
        response = eb_client.describe_environments(EnvironmentNames=[env_name])
        env = response['Environments'][0]
        status = env['Status']
        print(f"Environment status: {status}")
        if status == 'Ready':
            print(f"Environment URL: {env['CNAME']}")
            break
        time.sleep(10)

def main():
    # Step 1: Create S3 bucket
    create_s3_bucket(S3_BUCKET)

    # Step 2: Zip the project (include db.sqlite3)
    import os
    os.system('zip -r application.zip . -x "*.git*" "*.pyc" "__pycache__/*"')

    # Step 3: Create EB application
    create_application(APP_NAME)

    # Step 4: Upload zip to S3
    upload_to_s3(S3_BUCKET, 'application.zip', S3_KEY)

    # Step 5: Create application version
    create_application_version(APP_NAME, VERSION_LABEL, S3_BUCKET, S3_KEY)

    # Step 6: Create environment
    create_environment(APP_NAME, ENV_NAME, SOLUTION_STACK)

    # Step 7: Wait for environment to be ready
    wait_for_environment(ENV_NAME)

    # Step 8: Deploy the version
    time.sleep(5)  # Give version time to process
    update_environment(APP_NAME, ENV_NAME, VERSION_LABEL)

if __name__ == "__main__":
    main()