#!/usr/bin/env python3
import boto3
import json
import botocore.exceptions


s3client = boto3.client('s3')

bucket_list = s3client.list_buckets()

for bucket in bucket_list['Buckets']:
    bucket_name = bucket['Name']

    objects = s3client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in objects:
        for obj in objects['Contents']:
            object_key = obj['Key']
            s3client.delete_object(Bucket=bucket_name, Key=object_key)
            print(f"Deleted object: {object_key} in bucket: {bucket_name}")
    s3client.delete_bucket(Bucket=bucket_name)
    print(f"Deleted bucket: {bucket_name}")

def Get_Image(ec2client):
    image_response = ec2client.describe_images(
        Filters=[
            {
                'Name': 'description',
                'Values': ['Amazon Linux 2 AMI*']
            },
            {
                'Name': 'architecture',
                'Values': ['x86_64']
            },
            {
                'Name': 'owner-alias',
                'Values': ['amazon']
            }
        ]
    )
    return image_response['Images'][0]['ImageId']

def Create_EC2(AMI, ec2client):

    DRYRUN = False

    try:
        response = ec2client.run_instances(
            ImageId=AMI,
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            DryRun=DRYRUN
        )
        return response['Instances'][0]['InstanceId']
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'UnauthorizedOperation':
            print("UnauthorizedOperation: You may not have permissions to create EC2 instances in this region.")
            print("Please check your AWS configuration, specifically the region in ~/.aws/config.")
        elif "InvalidAMIID.NotFound" in str(error):
            print("InvalidAMIID: The specified AMI ID does not exist or is invalid.")
        elif "InvalidInstanceID.NotFound" in str(error):
            print("InvalidInstanceID: The specified instance ID does not exist.")
        else:
            print(f"An error occurred while creating EC2 instance: {error}")

def main():
    client = boto3.client('ec2')
    AMI = Get_Image(client)

    instance_id = Create_EC2(AMI, client)

    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    print(f"Before Waiting: Instance is {instance.state['Name']}")
    instance.wait_until_running()
    instance.load()
    print(f"After Waiting: Instance is {instance.state['Name']}")
    
if __name__ == "__main__":
    main()
