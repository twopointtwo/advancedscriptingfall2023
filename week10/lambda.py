import boto3

lambda_client = boto3.client('lambda')
iam = boto3.client('iam')

def create_lambda(function_name):
    role_response = iam.get_role(RoleName='LabRole')
    with open('lambda_stop_function.zip', 'rb') as handler:
        zipped_code = handler.read()

    response = lambda_client.create_function(
        FunctionName=function_name,
        Role=role_response['Role']['Arn'],
        Publish=True,
        PackageType='Zip',
        Runtime='python3.9',
        Code={
            'ZipFile': zipped_code
        },
        Handler='lambda_stop_function.lambda_handler'
    )

def invoke_lambda(function_name):
    invoke_response = lambda_client.invoke(FunctionName=function_name)
    return invoke_response

def main():
    function_name = 'stopEC2'
    try:
        function = lambda_client.get_function(FunctionName=function_name)
        print("Function Already Exists")
    except:
        print("Creating Function")
        create_lambda(function_name)

    print("Invoking Lambda Function")
    invoke_response = invoke_lambda(function_name)
    print(invoke_response)

if __name__ == "__main__":
    main()
