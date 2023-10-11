import boto3
import argparse

ec2_client = boto3.client('ec2')

def list_security_group_permissions(group_name):
    response = ec2_client.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': [group_name]}])
    
    for security_group in response['SecurityGroups']:
        print(f"Security Group Name: {security_group['GroupName']}")
        
        for rule in security_group['IpPermissions']:
            from_port = rule.get('FromPort', 'N/A')
            to_port = rule.get('ToPort', 'N/A')
            ip_ranges = [ip_range['CidrIp'] for ip_range in rule['IpRanges']]
            
            if '0.0.0.0/0' in ip_ranges:
                print(f"Port Range: {from_port}-{to_port}")
                print("IP Ranges Allowed: 0.0.0.0/0 (Open to the public internet!)")
                print("WARNING: Open to the public internet!\n")
            else:
                print(f"Port Range: {from_port}-{to_port}")
                print(f"IP Ranges Allowed: {', '.join(ip_ranges)}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="List EC2 Security Group Permissions")
    parser.add_argument('-s', '--security-group', help="Name of the security group to inspect")
    args = parser.parse_args()
    
    if args.security_group:
        list_security_group_permissions(args.security_group)
    else:
        response = ec2_client.describe_security_groups()
        for security_group in response['SecurityGroups']:
            list_security_group_permissions(security_group['GroupName'])
