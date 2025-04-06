import boto3
import time
import os

# Set region
REGION = 'eu-west-1'

# Initialize clients
eb_client = boto3.client('elasticbeanstalk', region_name=REGION)
s3_client = boto3.client('s3', region_name=REGION)

# Configuration
APP_NAME = 'cpp-stockmanger'
ENV_NAME = 'cpp-stockmanager-env'
VERSION_LABEL = 'v1.0.0'
S3_BUCKET = 'neerajcppbucketown'
S3_KEY = 'application.zip'
SOLUTION_STACK = '64bit Amazon Linux 2023 v4.5.0 running Python 3.13'
INSTANCE_PROFILE = 'jenkins_role'

# RDS Configuration (for environment variables)
DB_NAME = 'stockmanagedb'
DB_USERNAME = 'neerajdb'
DB_PASSWORD = 'Born2000'

def create_s3_bucket(bucket_name):
    """Create S3 bucket if it doesn’t exist"""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': REGION}
        )
        print(f"Created bucket {bucket_name}")

def create_application(app_name):
    """Create EB application"""
    try:
        eb_client.create_application(ApplicationName=app_name, Description='My Django Application with RDS')
        print(f"Created application {app_name}")
    except eb_client.exceptions.TooManyApplicationsException:
        print(f"Application {app_name} already exists")

def create_environment(app_name, env_name, solution_stack, db_endpoint):
    """Create EB environment with RDS settings"""
    try:
        eb_client.create_environment(
            ApplicationName=app_name,
            EnvironmentName=env_name,
            SolutionStackName=solution_stack,
            OptionSettings=[
                {'Namespace': 'aws:autoscaling:launchconfiguration', 'OptionName': 'InstanceType', 'Value': 't2.micro'},
                {'Namespace': 'aws:elasticbeanstalk:container:python', 'OptionName': 'WSGIPath', 'Value': 'stockmanage.wsgi:application'},
                {'Namespace': 'aws:elasticbeanstalk:environment:proxy:staticfiles', 'OptionName': '/static', 'Value': 'staticfiles'},
                {'Namespace': 'aws:autoscaling:launchconfiguration', 'OptionName': 'IamInstanceProfile', 'Value': INSTANCE_PROFILE},
                {'Namespace': 'aws:elasticbeanstalk:application:environment', 'OptionName': 'DJANGO_SETTINGS_MODULE', 'Value': 'stockmanage.settings'},
                {'Namespace': 'aws:elasticbeanstalk:application:environment', 'OptionName': 'DB_NAME', 'Value': DB_NAME},
                {'Namespace': 'aws:elasticbeanstalk:application:environment', 'OptionName': 'DB_USER', 'Value': DB_USERNAME},
                {'Namespace': 'aws:elasticbeanstalk:application:environment', 'OptionName': 'DB_PASSWORD', 'Value': DB_PASSWORD},
                {'Namespace': 'aws:elasticbeanstalk:application:environment', 'OptionName': 'DB_HOST', 'Value': db_endpoint},
                {'Namespace': 'aws:elasticbeanstalk:application:environment', 'OptionName': 'DB_PORT', 'Value': '5432'}
            ]
        )
        print(f"Creating environment {env_name}")
    except eb_client.exceptions.TooManyEnvironmentsException:
        print(f"Environment {env_name} already exists")

def upload_to_s3(bucket, file_path, key):
    s3_client.upload_file(file_path, bucket, key)
    print(f"Uploaded {file_path} to s3://{bucket}/{key}")

def create_application_version(app_name, version_label, s3_bucket, s3_key):
    eb_client.create_application_version(
        ApplicationName=app_name,
        VersionLabel=version_label,
        SourceBundle={'S3Bucket': s3_bucket, 'S3Key': s3_key}
    )
    print(f"Created version {version_label}")

def update_environment(app_name, env_name, version_label):
    eb_client.update_environment(
        ApplicationName=app_name,
        EnvironmentName=env_name,
        VersionLabel=version_label
    )
    print(f"Deploying {version_label} to {env_name}")

def wait_for_environment(env_name):
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
    create_s3_bucket(S3_BUCKET)
    db_endpoint = input("Enter the RDS endpoint (e.g., cpp-stockmanage-db.xxxxx.eu-west-1.rds.amazonaws.com): ")
    os.system('zip -r application.zip . -x "*.git*" "*.pyc" "__pycache__/*" "db.sqlite3"')
    create_application(APP_NAME)
    upload_to_s3(S3_BUCKET, 'application.zip', S3_KEY)
    create_application_version(APP_NAME, VERSION_LABEL, S3_BUCKET, S3_KEY)
    create_environment(APP_NAME, ENV_NAME, SOLUTION_STACK, db_endpoint)
    wait_for_environment(ENV_NAME)
    time.sleep(5)
    update_environment(APP_NAME, ENV_NAME, VERSION_LABEL)

if __name__ == "__main__":
    main()