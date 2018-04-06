'''import boto3,json,time
def obj():
    ec2 = boto3.resource('ec2')
    iam = boto3.client('iam')
    client=boto3.client('ec2')
    codedeploy=boto3.client('codedeploy')
    return ec2, iam, client, codedeploy


##ec2, iam, client, codedeploy= obj()
##print ec2, iam, client, codedeploy'''

import boto3
from botocore.exceptions import ClientError
while True:
    asgrole=raw_input("Enter the user: ")
    try:
        iam = boto3.client('iam')
        user = iam.create_user(UserName=asgrole)
        print "Created user: %s" % user
        break
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print "User already exists"
            
            
        else:
            print "Unexpected error: %s" % e
    
