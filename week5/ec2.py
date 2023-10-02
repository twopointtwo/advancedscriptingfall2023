#!/usr/bin/env python3

import boto3

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
    DryRun=DRYRUN,
    SecurityGroupIds=['sg-0635021150d9779d6'],
    UserData='''#!/bin/bash -ex
 # Updated to use Amazon Linux 2
 yum -y update
 yum -y install httpd php mysql php-mysql
 /usr/bin/systemctl enable httpd
 /usr/bin/systemctl start httpd
 cd /var/www/html
 wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/CUR-TF-100-ACCLFO2/lab6-scaling/lab-app.zip
 unzip lab-app.zip -d /var/www/html/
 chown apache:root /var/www/html/rds.conf.php
    '''
    )

    return response['Instances'][0]['InstanceId']

def main():
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