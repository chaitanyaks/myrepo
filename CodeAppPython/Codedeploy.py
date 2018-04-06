import boto3,json,time
from DevEnv import EC2Ins
from IAMRoles import CDRole

codedeploy=boto3.client('codedeploy')
iam=boto3.client('iam')

appName=raw_input("Enter the Application Name for CodeDeploy: ")
depgroup=raw_input("Enter the Deployment Group Name: ")

tagkey=raw_input("Enter the tag key for the EC2 Instance: ")
tagvalue=raw_input("Enter the tag value for the EC2 Instance: ")

def CD():
    """
    Creates application and deployment group for codedeploy.
    """
    key,value=EC2Ins(tagkey,tagvalue)
    arn= CDRole()
    
    application=codedeploy.create_application(applicationName=appName)

    
    deploymentgroup=codedeploy.create_deployment_group(
        applicationName=appName,
        deploymentGroupName=depgroup,
        ec2TagFilters=[
            {
                'Key': key,
                'Value': value,
                'Type':'KEY_AND_VALUE'
                },
            ],
        
        serviceRoleArn= arn
        )
    return application, deploymentgroup
app,dep=CD()
print "CodeDeploy with applicationid %s and deployment group id %s are created successfully" %(app['applicationId'],dep['deploymentGroupId'])
