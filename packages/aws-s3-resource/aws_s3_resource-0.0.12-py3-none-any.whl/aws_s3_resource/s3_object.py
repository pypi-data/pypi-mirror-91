import os
import uuid

import boto3
from botocore.client import ClientError

from . import S3
from .s3_bucket_error import NumberRandomCharsException


class S3Object(S3):

    @staticmethod
    def create_name(object_suffix, num_random_chars=6):
        if num_random_chars < NumberRandomCharsException.min_num_chars or \
                num_random_chars > NumberRandomCharsException.max_num_chars:
            raise NumberRandomCharsException

        return ''.join([str(uuid.uuid4()).replace('-', '')[:num_random_chars], '-', object_suffix])

    @staticmethod
    def get_object_key(file_name, with_random_prefix=True, num_random_chars=6):
        if with_random_prefix:
            return S3Object.create_name(file_name, num_random_chars)
        else:
            return file_name

    @classmethod
    def upload(cls, bucket_name, file_dict, with_random_prefix=True, num_random_chars=6):
        if 'file_path' in file_dict:
            _, file_name = os.path.split(file_dict['file_path'])
        else:
            file_name = file_dict['file_name']

        object_key = cls.get_object_key(file_name, with_random_prefix, num_random_chars)

        if 'file_path' in file_dict:
            cls.resource.Object(bucket_name, object_key).upload_file(file_dict['file_path'])

        elif 'file_bytes' in file_dict:
            cls.resource.meta.client.put_object(Bucket=bucket_name, Key=object_key, Body=file_dict['file_bytes'])

        elif 'file_obj' in file_dict:
            cls.resource.meta.client.upload_fileobj(file_dict['file_obj'], bucket_name, object_key)

        else:
            raise NotImplementedError('The "file_dict" parameters should include file_obj or file_bytes or file_path')

        return object_key

    @classmethod
    def download(cls, bucket_name, object_key, file_dict=dict()):
        if 'file_path' in file_dict:
            return cls.resource.Object(bucket_name, object_key).download_file(file_dict['file_path'])

        elif 'file_obj' in file_dict:
            return cls.resource.meta.client.download_fileobj(bucket_name, object_key, file_dict['file_obj'])

        elif len(file_dict) == 0:
            # Get the file bytes
            return cls.resource.meta.client.get_object(Bucket=bucket_name, Key=object_key)['Body'].read()

        else:
            raise NotImplementedError(
                'The "file_dict" parameters should include file_obj, file_path, or empty dict to return the file bytes')

    @classmethod
    def delete(cls, bucket_name, object_key):
        return cls.resource.meta.client.delete_object(Bucket=bucket_name, Key=object_key)

    @classmethod
    def list_all(cls, bucket_name, prefix=None, extensions=None, keys_only=True, as_generator=False):
    
        """
        bucket_name: string
        prefix: string
        extensions: tuple of strings
        keys_only: bool
        as_generator: bool
        """
        
        bucket = cls.resource.Bucket(bucket_name)  
        
        objects = bucket.objects.all() if prefix is None else bucket.objects.filter(Prefix=prefix)
        
        objects = objects if extensions is None else (obj for obj in objects if obj.key.endswith(extensions))
        
        objects = objects if not keys_only else (obj.key for obj in objects)
        
        return objects if as_generator else list(objects)

    @classmethod
    def is_available(cls, bucket_name, object_key):
        try:
            cls.resource.Object(bucket_name, object_key).load()

        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False

        else:
            return True

    @classmethod
    def num_objects(cls, bucket_name):
        return len(cls.list_all(bucket_name, False))

    @classmethod
    def generate_presigned_url(cls, bucket_name, object_name, expiration):
        """Generate a presigned URL to share an S3 object    :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        response = cls.resource.meta.client.generate_presigned_url('get_object',
                                                                   Params={'Bucket': bucket_name,
                                                                           'Key': object_name},
                                                                   ExpiresIn=expiration)

        return response
