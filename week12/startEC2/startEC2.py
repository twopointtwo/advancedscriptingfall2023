import json
import boto3
import time

def startEC2():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:env',
                'Values': ['dev']
            }
        ]
    )
    instance_list = ['i-0727a9ab17419b6e3']
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_list.append(instance['InstanceId'])
    start_response = ec2.start_instances(InstanceIds=instance_list)
    return start_response

def lambda_handler(event, context):
    start_time = time.time()  # Record current time
    response = startEC2()

    elapsed_time = time.time() - start_time  # Calculate elapsed time

    for instance in response['StartingInstances']:
        print(instance['InstanceId'])
    
    if elapsed_time >= 50:  # Check if close to Lambda timeout
        print("Approaching Lambda timeout. Handle accordingly.")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
