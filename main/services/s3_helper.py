import json

import boto3

from web_testing_service import settings

from storages.backends.s3boto3 import S3Boto3Storage

# class S3MediaStorage(S3Boto3Storage):
#     location = 'problems/test_files/'


class S3ProblemTestFilesStorage(S3Boto3Storage):
    location = 'problems/test_files/'


def upload_file_to_s3(test_file):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3_path = f'problems/test_files/{test_file.name}'

    s3.upload_fileobj(test_file, bucket_name, s3_path)



# def read_file_from_s3(s3_path):
#     s3_client = boto3.client('s3',
#                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
#
#     response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_path)
#     print(response)
#     file_content = response['Body'].read()
#     print(file_content)
#
#     file_content_str = file_content.decode('utf-8')
#
#     json_data = json.loads(file_content_str)
#     print("Printing jsondata")
#     print(json_data)
#     return json_data


# def read_file_from_s3(s3_path, local_path):
#     s3_client = boto3.client('s3',
#                              aws_access_key_id=settings.aws_access_key_id,
#                              aws_secret_access_key=settings.aws_secret_access_key)
#     try:
#         response = s3_client.get_object(Bucket=settings.aws_storage_bucket_name, Key=s3_path)
#         print('a')
#         print(response['Body'].read().decode('utf-8'))
#         print('a')
#         file_content = response['Body'].read()
#         with open(local_path, 'wb') as local_file:
#             local_file.write(file_content)
#         return True
#
#     except Exception as e:
#         print(e)
#         return False