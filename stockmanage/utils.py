# stockmanage/utils.py
import boto3
from django.conf import settings

def send_sns_notification(subject, message):
    sns_client = boto3.client('sns', region_name=settings.AWS_REGION)
    sns_client.publish(
        TopicArn=settings.SNS_TOPIC_ARN,
        Subject=subject[:100],
        Message=message
    )
    print(f"Sent SNS notification: {subject}")