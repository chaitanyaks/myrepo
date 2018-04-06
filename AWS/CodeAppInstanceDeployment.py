import boto3,json,time

ec2 = boto3.resource('ec2')
iam = boto3.client('iam')
client=boto3.client('ec2')
userdata= """#!/usr/bin/env python3

import os,sys,time
os.system("sudo apt-get -y update")
time.sleep(20)
os.system("sudo apt-get install -y ruby2.3")
time.sleep(20)
os.system("sudo apt-get install -y awscli")
time.sleep(20)
os.chdir("/home/ubuntu")
time.sleep(20)
os.system("sudo aws s3 cp s3://aws-codedeploy-us-west-2/latest/install . --region us-west-2")
time.sleep(20)
os.system("sudo chmod +x ./install")
time.sleep(20)
os.system("sudo ./install auto")
tume.sleep(20)"""
#IAM role creation for EC2 Instance
AssumeRolePolicy= { 'Version' : '2012-10-17','Statement':[{"Effect": "Allow","Principal": { "Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}
AssumeRole_json=json.dumps(AssumeRolePolicy,indent=2)

role = iam.create_role(RoleName='Instanceprofilerole4',AssumeRolePolicyDocument= AssumeRole_json ,Description='Instance Profile role for EC2')

# IAM Instance profile policy creation and attaching the policy to the role.

policy= {'Version': '2012-10-17','Statement': [{"Action": ["ec2:*","codedeploy:*","autoscaling:Describe*","s3:Get*","s3:List*"],"Effect": "Allow","Resource": "*"}]}
policy_json=json.dumps(policy,indent=2)

InstanceRolePolicy=iam.create_policy(PolicyName='Instancerole4',PolicyDocument= policy_json,Description='Instance role policy')
Attachpolicy=iam.attach_role_policy(RoleName=role['Role']['RoleName'],PolicyArn=InstanceRolePolicy['Policy']['Arn'])
InstanceRoleInstanceProfile= iam.create_instance_profile(InstanceProfileName='InstanceProfile4')
time.sleep(50)
AttachInstancepolicy= iam.add_role_to_instance_profile(InstanceProfileName=InstanceRoleInstanceProfile['InstanceProfile']['InstanceProfileName'],RoleName=role['Role']['RoleName'])
time.sleep(100)

securitygroup=client.create_security_group(GroupName='SecurityGroup_CodeApp3',Description='Security group for codeapp')
SecurityGrp=securitygroup['GroupId']
print SecurityGrp
rule=client.authorize_security_group_ingress(GroupName='SecurityGroup_CodeApp3',
                                         GroupId=SecurityGrp,
                                         IpPermissions=[
                                             {
                                                 'IpProtocol': 'tcp',
                                                 'FromPort':22,
                                                 'ToPort':22,
                                                 'IpRanges':[
                                                     {
                                                         'CidrIp': '0.0.0.0/0'
                                                         }
                                                     ]
                                                 },
                                             {
                                                 'IpProtocol': 'tcp',
                                                 'FromPort':8080,
                                                 'ToPort':8080,

                                                 'IpRanges':[
                                                     {
                                                         'CidrIp': '0.0.0.0/0'
                                                         }
                                                     ]
                                                 },
                                             {
                                                 'IpProtocol': 'tcp',
                                                 'FromPort':3306,
                                                 'ToPort':3306,
                                                 'IpRanges':[
                                                     {
                                                        'CidrIp': '0.0.0.0/0'
                                                        }
                                                     ]
                                                 }
                                             ])
key=ec2.create_key_pair(KeyName= 'CodeAppTool3')
keypair=key.name
fp=open('keypair.pem','w')
fp.writelines(key.key_material)
fp.close()
print key.key_material
print keypair

instance=ec2.create_instances(ImageId='ami-efd0428f',
                              SecurityGroups=['SecurityGroup_CodeApp3'],
                              SecurityGroupIds=[SecurityGrp],
                              InstanceType='t2.micro',
                              MinCount=1,
                              MaxCount=1,
                              KeyName= keypair,
                              UserData= userdata,
                              IamInstanceProfile={
                                  'Name': InstanceRoleInstanceProfile['InstanceProfile']['InstanceProfileName']
                                  
                                  },
                                  
                              
                              TagSpecifications=[{
                                  'ResourceType': 'instance',
                                  'Tags':[
                                      {
                                          'Key': 'CodeAppTool1',
                                          'Value':'CodeAppTool1'
                                          }]
                                  }
                                  
                                      ]
                              )
                                         
