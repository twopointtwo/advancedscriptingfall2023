import boto3

def remove_port_22(ec2_client, security_group_id):
    response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
    security_group = response['SecurityGroups'][0]

    print(f"\tSecurity Group ID: {security_group_id}")
    print(f"\tIngress rules for {security_group_id}:")
    
    for rule in security_group['IpPermissions']:
        if rule['IpProtocol'] == 'tcp' and rule['FromPort'] == 22 and rule['ToPort'] == 22:
            for cidr_range in rule['IpRanges']:
                if cidr_range['CidrIp'] == '0.0.0.0/0':
                    print(f"\tSSH port open to 0.0.0.0/0 in {security_group_id}. Removing rule...")
                    ec2_client.revoke_security_group_ingress(
                        GroupId=security_group_id,
                        IpPermissions=[rule]
                    )
                    print(f"\tRule removed for SSH in {security_group_id}")

def list_instance_security_groups(ec2_client):
    instances = ec2_client.describe_instances()["Reservations"]

    for instance in instances:
        instance_id = instance["Instances"][0]["InstanceId"]
        instance_security_groups = [sg["GroupId"] for sg in instance["Instances"][0]["SecurityGroups"]]
        
        print(f"Instance ID: {instance_id}")
        print(f"Security Groups: {', '.join(instance_security_groups)}")

        for security_group_id in instance_security_groups:
            remove_port_22(ec2_client, security_group_id)

def main(event, context):
    ec2_client = boto3.client('ec2')
    list_instance_security_groups(ec2_client)

if __name__ == "__main__":
    ec2_client = boto3.client('ec2')
    list_instance_security_groups(ec2_client)
