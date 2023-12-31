import boto3,json,datetime,random,argparse,string

import botocore

client = boto3.client('s3')

bucket_name = "hsafavi-fall2023-buckettest"

parser = argparse.ArgumentParser(description="Arguments to supply bucket name for our s3website")
parser.add_argument('-s','--sitename',dest='site_name', default='', type=str, help='Enter a unique bucket name for your s3website')

args = parser.parse_args()

if not args.site_name:
    print(f"No site_name was provided, we will use a random generator")
    bucket_name += "".join(random.choices(string.ascii_lowercase, k=10))
else:
    print(f"You specified a bucket name of {args.site_name}.")
    bucket_name = args.site_name
try:
    bucket_response = client.create_bucket(Bucket=bucket_name)

    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::%s/*" % bucket_name
        }]
    }

    bucket_policy_string = json.dumps(bucket_policy)

    client.delete_public_access_block(Bucket=bucket_name)

    bucket_policy_response = client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=bucket_policy_string
    )

    put_bucket_response = client.put_bucket_website(
        Bucket=bucket_name, 
        WebsiteConfiguration={ 
            'ErrorDocument': {'Key': 'error.html'}, 
            'IndexDocument': {'Suffix': 'index.html'}, 
        } 
    )

    indexFile = open('index.html', 'rb')
    put_index_response = client.put_object(Body=indexFile, Bucket=bucket_name, Key='index.html',ContentType='text/html')
    indexFile.close()
    print(put_index_response)

    errorFile = open('error.html', 'rb')
    put_error_response = client.put_object(Body=errorFile, Bucket=bucket_name, Key='error.html', ContentType='text/html')
    errorFile.close()
    print(put_error_response)

except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == 'InvalidToken':
        print("Please update your AWS credentials file with a valid token")
    elif error.response['Error']['Code'] == 'IllegalLocationConstraintException':
        print("The location selected is incompatible for the region specific endpoint the request was sent to.")

except client.meta.client.exceptions.BucketAlreadyExists as err:
        print("Bucket {} already exists!".format(err.response['Error']['BucketName']))
        print("Re-run the script with a valid bucket name")
else:
        print(f"Some other error occurred: {error}")