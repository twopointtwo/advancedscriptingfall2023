#!/usr/bin/env python3

import boto3,s3enforce,json

def CreateTrail(trail_name, bucket_name):
    trailclient = boto3.client('cloudtrail')
    try:
        response = trailclient.create_trail(S3BucketName=bucket_name, Name=trail_name)  # Corrected 'trial_name' to 'trail_name'
        return response
    except trailclient.exceptions.TrailAlreadyExistsException as error:
        response = trailclient.start_logging(Name=trail_name)  
        return response
    
def main():
    sts_client = boto3.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]

    bucket_name = "hsafavi-cloud-trail-demo"
    trail_name = "hsafavi-ct-demo" 
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{account_id}/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }

    response = s3enforce.CreateBucket(bucket_name)
    policy_response = s3enforce.SetBucketPolicy(bucket_name, json.dumps(policy))

    response = CreateTrail(trail_name, bucket_name)
    print(response)

if __name__ == "__main__":
    main()
