import boto3,json,time

iam=boto3.client('iam')

RoleNameEC2=raw_input("Enter the role name to create for EC2: ")
PolicyNameEC2= raw_input("Enter the policy name to create for EC2: ")
InstanceProfileRoleEC2=raw_input("Enter the instance profile role to create for EC2: ")

RoleNameCD= raw_input("Enter the role name to create for codedeploy: ")
PolicyNameCD= raw_input("Enter the policy name to create for codedeploy: ")

def EC2Role():
    
    """
    Creates IAM Instance Profile role for EC2 Instance
    """
    
    AssumeRolePolicy= { 'Version' : '2012-10-17','Statement':[{"Effect": "Allow","Principal": { "Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}
    AssumeRole_json=json.dumps(AssumeRolePolicy,indent=2)

    role = iam.create_role(RoleName= RoleNameEC2,AssumeRolePolicyDocument= AssumeRole_json ,Description='Instance Profile role for EC2')

    # IAM Instance profile policy creation and attaching the policy to the role.

    policy= {'Version': '2012-10-17','Statement': [{"Action": ["ec2:*","codedeploy:*","autoscaling:Describe*","s3:Get*","s3:List*"],"Effect": "Allow","Resource": "*"}]}
    policy_json=json.dumps(policy,indent=2)

    InstanceRolePolicy=iam.create_policy(PolicyName= PolicyNameEC2,PolicyDocument= policy_json,Description='Instance role policy')
    Attachpolicy=iam.attach_role_policy(RoleName=role['Role']['RoleName'],PolicyArn=InstanceRolePolicy['Policy']['Arn'])
    time.sleep(10)
    #print type(args),args
    InstanceRoleInstanceProfile= iam.create_instance_profile(InstanceProfileName= InstanceProfileRoleEC2)
    AttachInstancepolicy= iam.add_role_to_instance_profile(InstanceProfileName=InstanceRoleInstanceProfile['InstanceProfile']['InstanceProfileName'],RoleName=role['Role']['RoleName'])
    time.sleep(20)
    response= InstanceRoleInstanceProfile['InstanceProfile']['InstanceProfileName']

    return response

def CDRole():
    # Service role for codedeploy

    AssumeRolePolicyCD= {'Version' : '2012-10-17','Statement':[{"Sid": "1","Effect": "Allow","Principal": {"Service": ["codedeploy.us-west-2.amazonaws.com"]},"Action": "sts:AssumeRole"}]}
    AssumeRoleCD_json=json.dumps(AssumeRolePolicyCD,indent=2)
    role_CD= iam.create_role(RoleName= RoleNameCD,AssumeRolePolicyDocument= AssumeRoleCD_json, Description='CodeDeploy Role')
                        
    policyCD= {'Version': '2012-10-17','Statement':[{"Effect": "Allow","Resource": ["*"],"Action": ["ec2:Describe*"]},{"Effect": "Allow","Resource": ["*"],"Action": ["autoscaling:*"]}]}
    policyCD_json=json.dumps(policyCD,indent=2)
    RolePolicyCD=iam.create_policy(PolicyName= PolicyNameCD,PolicyDocument= policyCD_json,Description= 'Policy for codedeploy')
    AttachCDPolicy= iam.attach_role_policy(RoleName= role_CD['Role']['RoleName'],PolicyArn= RolePolicyCD['Policy']['Arn'])
    time.sleep(20)
    response= role_CD['Role']['Arn']

    return response



    
