import boto3,json,time
from DeployEnvModule import EC2


appName=raw_input("Enter the Application Name for CodeDeploy: ")
depgroup=raw_input("Enter the Deployment Group Name: ")

codedeploy=boto3.client('codedeploy')
iam=boto3.client('iam')

# Service role for codedeploy

AssumeRolePolicyCD= {'Version' : '2012-10-17','Statement':[{"Sid": "1","Effect": "Allow","Principal": {"Service": ["codedeploy.us-west-2.amazonaws.com"]},"Action": "sts:AssumeRole"}]}
AssumeRoleCD_json=json.dumps(AssumeRolePolicyCD,indent=2)
role_CD= iam.create_role(RoleName='CDRole',AssumeRolePolicyDocument= AssumeRoleCD_json, Description='CodeDeploy Role')
                        
policyCD= {'Version': '2012-10-17','Statement':[{"Effect": "Allow","Resource": ["*"],"Action": ["ec2:Describe*"]},{"Effect": "Allow","Resource": ["*"],"Action": ["autoscaling:*"]}]}
policyCD_json=json.dumps(policyCD,indent=2)
RolePolicyCD=iam.create_policy(PolicyName='CodeDeployPolicy',PolicyDocument= policyCD_json,Description= 'Policy for codedeploy')
AttachCDPolicy= iam.attach_role_policy(RoleName= role_CD['Role']['RoleName'],PolicyArn= RolePolicyCD['Policy']['Arn'])
time.sleep(100)
# Codedeploy application

application=codedeploy.create_application(applicationName=appName)

# Codedeploy deployment group

deploymentgroup=codedeploy.create_deployment_group(
    applicationName=appName,
    deploymentGroupName=depgroup,
    ec2TagFilters=[
        {
            'Key': EC2.tagkey,
            'Value': EC2.tagvalue,
            'Type':'KEY_AND_VALUE'
            },
        ],
    serviceRoleArn= role_CD['Role']['Arn']
    )
time.sleep(50)
'''bucketloc=raw_input("Enter the Location of the bucket to run the revision: ")
revision= codedeploy.create_deployment(
    applicationName='appName',
    deploymentGroupName='depgroup',
    revision={
        rev=input("Choose the revision type, 1. S3 2. GitHub ")
        'revisionType': S3,
        's3Location':{
            'bucket': bucketloc,
            'bundleType': 'zip'
            }
        
            'gitHubLocation':{
                'repository':'string',
                'commitId': 'string'
                }
        },
    targetInstances={
        'tagFilters':[{
            'Key': 'tool2',
            'Value': 'tool2',
            'Type': 'KEY_AND_VALUE'
            }]
        })'''


