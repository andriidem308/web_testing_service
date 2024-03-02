from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage.filesystem import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage


class LocalStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.MEDIA_ROOT
        super().__init__(*args, **kwargs)


app_storage = default_storage
if settings.WORKFLOW == 's3':
    app_storage = S3Boto3Storage()
if settings.WORKFLOW == 'local':
    app_storage = LocalStorage()
