import boto3

#

# Configure Boto3 to interact with S3
s3 = boto3.client('s3', aws_access_key_id='YOUR_AWS_ACCESS_KEY', aws_secret_access_key='YOUR_AWS_SECRET_KEY', region_name='YOUR_REGION')
bucket_name = 'your-s3-bucket-name'