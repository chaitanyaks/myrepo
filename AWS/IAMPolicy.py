import boto3
import json
iam = boto3.client('iam')
'''Aspolicy = { 'Version' : '2012-10-17'}
#print type(policy)
Aspolicy['Statement'] = [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
Aspolicy_json = json.dumps(policy, indent=2)
policy= {'Version': '2012-10-17'}
policy['Statement']= [
        {
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
policy_json = json.dumps(policy, indent=2)
#print policy_json'''
#policy1=iam.create_policy(PolicyName='Instanceprofile',PolicyDocument= policy_json,Description='Instance Profile for EC2')

'''fr=open("assumerole.json",'r')
fr1=fr.read()

policyfile=open("InstanceProfilePolicy.json",'r')
pf=policyfile.read()
role = iam.create_role(RoleName='instanceprof',AssumeRolePolicyDocument=fr1 ,Description='ec2')
policy=iam.create_policy(PolicyName='Instanceprofile',PolicyDocument= pf,Description='Instance Profile for EC2')

Attachpolicy=iam.attach_role_policy(RoleName=role['Role']['RoleName'],PolicyArn=policy['Policy']['Arn'])'''
instpolicy=iam.create_instance_profile(InstanceProfileName='InsProf')
print instpolicy


'Roles': [
                {
                    'Path': 'string',
                    'RoleName': 'string',
                    'RoleId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'AssumeRolePolicyDocument': 'string',
                    'Description': 'string'
                },
                                       
iam.delete_instance_profile(InstanceProfileName='InstanceProfiles')
