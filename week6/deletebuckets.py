import boto3
s3 = boto3.client('s3')

response = s3.list_buckets()

for bucket in response['Buckets']:
    print(f"Deleting bucket {bucket['Name']}")
    objects_response = s3.list_objects_v2(Bucket=bucket['Name'])
    if objects_response.get('Contents'):
        for object in objects_response['Contents']:
            print(f"...Deleting Object {object['Key']}")
            delete_object_response = s3.delete_object(Bucket=bucket['Name'],Key=object['Key'])
    delete_bucket_response = s3.delete_bucket(Bucket=bucket['Name'])