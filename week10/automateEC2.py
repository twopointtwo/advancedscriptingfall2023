import boto3

ec2 = boto3.client('ec2')

def Stop_EC2():
    response = ec2.describe_instances()
    instances_to_stop = [
        instance['InstanceId'] 
        for reservation in response['Reservations'] 
        for instance in reservation['Instances'] 
        if instance['State']['Name'] in ['running', 'pending']
    ]
    return ec2.stop_instances(InstanceIds=instances_to_stop) if instances_to_stop else "No instances in a stoppable state"

def Start_EC2():
    response = ec2.describe_instances()
    instances_to_start = [
        instance['InstanceId'] 
        for reservation in response['Reservations'] 
        for instance in reservation['Instances'] 
        if instance['State']['Name'] == 'stopped'
    ]
    return ec2.start_instances(InstanceIds=instances_to_start) if instances_to_start else "No instances in a startable state"

def main():
    print(Stop_EC2())
    print(Start_EC2())

if __name__ == "__main__":
    main()
