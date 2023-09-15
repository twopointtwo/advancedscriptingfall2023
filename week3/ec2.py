#!/usr/bin/env python3
import boto3
import json

client = boto3.client('ec2')

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

    response = ec2client.run_instances(
        ImageId=AMI,
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN
    )
    return response['Instances'][0]['InstanceId']

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
    print(f"Public IP Address: is {instance.public_ip_address}")
    print(f"Instance Tags: {instance.tags}")
    print(instance.create_tags(Tags=[{'Key': 'Name', 'Value': 'Haene'}]))
    instance.terminate()
    print(f"Before Terminated: Instance is {instance.state['Name']}")
    instance.wait_until_terminated()
    instance.load()
    print(f"After Terminated: Instance is {instance.state['Name']}")

#print(instance.instance_id)

if __name__ == "__main__":
    main()

