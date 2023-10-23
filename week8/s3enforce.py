#!/usr/bin/env python3

import boto3


def CreateBucket(bucket_name):
    s3client = boto3.client('s3')
    response = s3client.create_bucket(Bucket=bucket_name)
    return response


def DeleteBucket(bucket_name):
    s3client = boto3.client('s3')
    response = s3client.delete_bucket(Bucket=bucket_name)
    return response

def EnforceVersioning(bucket_name):
    s3client = boto3.client('s3')
    response = s3client.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={
            'MFADelete': 'Disabled',
            'Status': 'Enabled',
        }
    )
    return response

def SetBucketPolicy(bucket_name, policy):
    s3client = boto3.client('s3')
    response = s3client.put_bucket_policy(Bucket= bucket_name, Policy=policy)
    return response

def main():
    bucket_name = "hsafavi-demo-v1"
    response = CreateBucket(bucket_name)
    version_response = EnforceVersioning(bucket_name)

if __name__ == "__main__":
    main()