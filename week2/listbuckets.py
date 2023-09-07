#!/usr/bin/env python3
import boto3

s3client = boto3.client('s3')

bucket_list = s3client.list_buckets()

for bucket in bucket_list['Buckets']:
    print(f"Bucket Name is: {bucket['Name']}")

