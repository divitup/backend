import boto3
from inits.secret import region_name, get_secret
import uuid

# @TODO: unify naming conventions

# Configure Boto3 to interact with S3
credentials = get_secret("divitup-S3-access")
s3 = boto3.client('s3',
                  aws_access_key_id=credentials['aws_access_key_id'],
                  aws_secret_access_key=credentials['aws_secret_access_key'],
                  region_name=region_name)
bucket_name = 'divup-images'


def s3_upload(session_id, s3_path, image_file):

    s3.upload_fileobj(image_file, bucket_name, s3_path)

    return session_id, s3_path
