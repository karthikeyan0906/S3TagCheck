import json

import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    tmp = []

    buckets = s3.list_buckets()

    for bucketName in buckets['Buckets']:
        try:
            bucket_tagging = s3.get_bucket_tagging(Bucket=(bucketName['Name']))
        except:
            # print("No tags set on bucket: ", bucketName['Name'])
            tmp.append(bucketName['Name'])

    SENDER = "team@gmail.com"
    RECIPIENT = "abc@gmail.com"
    AWS_REGION = "us-east-1"
    # The subject line for the email.
    SUBJECT = "List of S3 Buckets which don't have tags on Dev Account-bundle"
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "No tags set on bucket:" + str(tmp)
    # BODY_TEXT = (Mail_Text)

    # The character encoding for the email.
    client = boto3.client('ses', region_name=AWS_REGION)
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Script Execution completed ')
    }
