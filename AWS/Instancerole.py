import boto3,json

iam = boto3.client('iam')

'''#IAM role creation for EC2 Instance
AssumeRolePolicyEC2= { 'Version' : '2012-10-17','Statement':[{"Effect": "Allow","Principal": { "Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}
AssumeRole_json=json.dumps(AssumeRolePolicyEC2,indent=2)

role_EC2 = iam.create_role(RoleName='Instanceprofilerole',AssumeRolePolicyDocument= AssumeRole_json ,Description='Instance Profile role for EC2')

# IAM Instance profile policy creation and attaching the policy to the role.

policyEC2= {'Version': '2012-10-17','Statement': [{"Action": ["ec2:*","codedeploy:*","autoscaling:Describe*","s3:Get*","s3:List*"],"Effect": "Allow","Resource": "*"}]}
policy_json=json.dumps(policyEC2,indent=2)

InstanceRolePolicy=iam.create_policy(PolicyName='Instancerole',PolicyDocument= policy_json,Description='Instance role policy')
Attachpolicy=iam.attach_role_policy(RoleName=role_EC2['Role']['RoleName'],PolicyArn=InstanceRolePolicy['Policy']['Arn'])
InstanceRoleInstanceProfile= iam.create_instance_profile(InstanceProfileName='InstanceProfile')
AttachInstancepolicy= iam.add_role_to_instance_profile(InstanceProfileName=InstanceRoleInstanceProfile['InstanceProfile']['InstanceProfileName'],RoleName=role_EC2['Role']['RoleName'])'''

# Service Role for CodeDeploy
def CD():
    AssumeRolePolicyCD= {'Version' : '2012-10-17','Statement':[{"Sid": "1","Effect": "Allow","Principal": {"Service": ["codedeploy.us-west-2.amazonaws.com"]},"Action": "sts:AssumeRole"}]}
    AssumeRoleCD_json=json.dumps(AssumeRolePolicyCD,indent=2)
    role_CD= iam.create_role(RoleName='CDRole',AssumeRolePolicyDocument= AssumeRoleCD_json, Description='CodeDeploy Role')
                        
    policyCD= {'Version': '2012-10-17','Statement':[{"Effect": "Allow","Resource": ["*"],"Action": ["ec2:Describe*"]},{"Effect": "Allow","Resource": ["*"],"Action": ["autoscaling:*"]}]}
    policyCD_json=json.dumps(policyCD,indent=2)
    RolePolicyCD=iam.create_policy(PolicyName='CodeDeployPolicy1',PolicyDocument= policyCD_json,Description= 'Policy for codedeploy')
    AttachCDPolicy= iam.attach_role_policy(RoleName= role_CD['Role']['RoleName'],PolicyArn= RolePolicyCD['Policy']['Arn'])
    return role_CD['Role']['Arn']
CD()

                         

