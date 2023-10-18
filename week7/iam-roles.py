import boto3
import datetime
import pytz
from botocore.exceptions import ClientError

iam_client = boto3.client('iam')

current_date_utc = datetime.datetime.now(pytz.utc)

ninety_days_ago = current_date_utc - datetime.timedelta(days=90)

response = iam_client.list_roles()

for role in response['Roles']:
    role_name = role['RoleName']
    role_creation_date = role['CreateDate']

    print(f"Role {role_name} -- Created: {role_creation_date}")

    try:
        attached_policies_response = iam_client.list_attached_role_policies(RoleName=role_name)
        for attached_policy in attached_policies_response['AttachedPolicies']:
            attached_policy_name = attached_policy['PolicyName']
            print(f"... has managed policy name: {attached_policy_name}")

    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print(f"... has managed policy name: Access Denied - You don't have permission to list attached policies.")
        else:
            print(f"... has managed policy name: ERROR - {e}")

    try:
        inline_policies_response = iam_client.list_role_policies(RoleName=role_name)
        for inline_policy_name in inline_policies_response['PolicyNames']:
            print(f"... has inline/unmanaged policy name: {inline_policy_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print(f"... has inline/unmanaged policy name: Access Denied - You don't have permission to list inline policies.")
        else:
            print(f"... has inline/unmanaged policy name: ERROR - {e}")

    print()
