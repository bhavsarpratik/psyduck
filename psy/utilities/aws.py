import os
import re
import subprocess

import boto3


def set_parameter_value_kms(parameter_name, value):
    os.system('aws ssm put-parameter --name %s --value %s --type SecureString --overwrite' % (
        parameter_name, value))


def get_parameter_value_kms(parameter_name, region, profile=None):
    if profile is None:
        ssmclient = boto3.client('ssm', region_name=region)
    else:
        session = boto3.session.Session(profile_name=profile)
        ssmclient = session.client('ssm', region_name=region)
    value = ssmclient.get_parameter(Name=parameter_name, WithDecryption=True)['Parameter']['Value']
    return value

def get_s3_resource(profile):
    '''

    :param profile: profile name to be provided
    :return: s3 resource instance which could be from default session or profile specific
    '''
    if profile is None:
        s3 = boto3.resource('s3')
    else:
        session = boto3.session.Session(profile_name=profile)
        s3 = session.resource('s3')
    return s3

def get_s3_client(profile):
    '''

    :param profile: profile name to be provided
    :return: s3 client instance which could be from default session or profile specific
    '''
    if profile is None:
        s3 = boto3.client('s3')
    else:
        session = boto3.session.Session(profile_name=profile)
        s3 = session.client('s3')

    return s3

def split_s3_bucket_key(uri):
    '''

    :param uri: s3 file link  in format "s3://.../../" or "s3a://.../.../"
    :return: bucket and key of the absolution location in s3
    '''
    m = re.match(r'^s3a?://(.*?)/(.*)', uri)
    bucket, key = m.group(1), m.group(2)
    return bucket, key


def get_filelist_from_s3_bucket(bucketname, profile=None):
    '''

    :param bucketname:
    :param profile:
    :return: list of keys
    '''
    s3 = get_s3_resource(profile)
    files = []
    for object in s3.Bucket(bucketname).objects.all():
        files.append(object.key)
    return files


def get_all_s3_keys(bucketname,profile=None):
    """Get a list of all keys in an S3 bucket."""
    keys = []
    s3=get_s3_client(profile)
    kwargs = {'Bucket': bucketname}
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            keys.append(obj['Key'])

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

    return keys


def get_s3_file_contents(s3_filename, encoding='utf-8', profile=None):
    """Get a file from AWS.

    :param s3_filename: filename in format "s3://.../../" or "s3a://.../.../"
    :param encoding:
    :param profile:
    :returns: File contents in a string

    Note: this is designed only for small config files, etc.
    """
    print("loading {0} from s3".format(s3_filename))
    bucket, key = split_s3_bucket_key(s3_filename)
    s3=get_s3_resource(profile)
    obj = s3.Object(bucket, key)

    contents = obj.get()['Body'].read().decode(encoding)
    return contents


def download_file_from_s3(s3_filename, downloaded_file, profile=None):
    '''

    :param s3_filename: s3 file link  in format "s3://.../../" or "s3a://.../.../"
    :param downloaded_file: download as filename
    :param profile:
    :return:
    '''
    try:
        s3 = get_s3_resource(profile)
        bucket, key = split_s3_bucket_key(s3_filename)
        s3.Bucket(bucket).download_file(key, downloaded_file)
    except Exception as e:
        print(e)
        raise AssertionError("Unable to download the file")




def upload_file_to_s3(file_to_upload, bucketname, key_, content_type=None, make_public=False, profile=None):
    '''

    :param file_to_upload:
    :param bucketname:
    :param key_:
    :param content_type: string
    :param make_public: bool
    :param profile:
    :return: downaloadable S3 file link
    '''
    try:
        s3 = get_s3_resource(profile)
        print("Uploading " + file_to_upload)
        extra_args = {}
        if (make_public == True):
            extra_args['ACL'] = "public-read"
        if content_type!=None:
            extra_args['ContentType'] = content_type

        s3.meta.client.upload_file(file_to_upload, bucketname, key_, ExtraArgs=extra_args)
        downloadable_file_path = "/".join(["https://s3.amazonaws.com", bucketname, key_])
        return downloadable_file_path
    except Exception as e:
        print(e)
        raise AssertionError("Unable to upload the file")
