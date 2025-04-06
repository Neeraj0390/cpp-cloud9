import boto3
import time

# Set region
REGION = 'eu-west-1'

# Initialize RDS client
rds_client = boto3.client('rds', region_name=REGION)

# RDS Configuration
DB_INSTANCE_IDENTIFIER = 'cpp-stockmanage-db'
DB_NAME = 'stockmanagedb'
DB_USERNAME = 'neerajdb'
DB_PASSWORD = 'Born2000'  
DB_INSTANCE_CLASS = 'db.t3.micro'
DB_ENGINE = 'postgres'
DB_ENGINE_VERSION = '16.6'

def create_rds_instance():
    """Create RDS PostgreSQL instance"""
    try:
        rds_client.create_db_instance(
            DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER,
            DBName=DB_NAME,
            MasterUsername=DB_USERNAME,
            MasterUserPassword=DB_PASSWORD,
            DBInstanceClass=DB_INSTANCE_CLASS,
            Engine=DB_ENGINE,
            EngineVersion=DB_ENGINE_VERSION,
            AllocatedStorage=20,
            PubliclyAccessible=True,  # For testing; set False in production
            VpcSecurityGroupIds=[get_default_security_group()]
        )
        print(f"Creating RDS instance {DB_INSTANCE_IDENTIFIER}")
    except rds_client.exceptions.DBInstanceAlreadyExistsFault:
        print(f"RDS instance {DB_INSTANCE_IDENTIFIER} already exists")

def get_default_security_group():
    """Get default VPC security group"""
    ec2_client = boto3.client('ec2', region_name=REGION)
    response = ec2_client.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': ['default']}])
    return response['SecurityGroups'][0]['GroupId']

def wait_for_rds_instance():
    """Wait for RDS instance to be available and return endpoint"""
    waiter = rds_client.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
    response = rds_client.describe_db_instances(DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER)
    endpoint = response['DBInstances'][0]['Endpoint']['Address']
    print(f"RDS endpoint: {endpoint}")
    return endpoint

def main():
    create_rds_instance()
    db_endpoint = wait_for_rds_instance()
    print(f"Use this endpoint for deployment: {db_endpoint}")

if __name__ == "__main__":
    main()