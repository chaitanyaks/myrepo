import boto3,json,time
from IAMRoles import EC2Role

ec2 = boto3.resource('ec2')
iam = boto3.client('iam')
client=boto3.client('ec2')
tagkey=raw_input("Enter the tag key for the EC2 Instance: ")
tagvalue=raw_input("Enter the tag value for the EC2 Instance: ")
securitygroup=raw_input("Enter the security group name: ")
keypairname=raw_input("Enter keypair name: ")

def EC2Ins():
    
    userdata= """#!/usr/bin/env python3

    import os,sys,time

    os.system("sudo apt-get -y update")

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
    os.system("sudo ./install auto")"""

    # Security Group Creation with rule 22, 8080, 3306

    security=client.create_security_group(GroupName=securitygroup,Description='Security group for codeapp')
    SecurityGrp=security['GroupId']
    print SecurityGrp
    rule=client.authorize_security_group_ingress(GroupName=securitygroup,
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
    # KeyPair creation

    key=ec2.create_key_pair(KeyName= keypairname)
    keypair=key.name
    fp=open('keypair.pem','w')
    fp.writelines(key.key_material)
    fp.close()
    print key.key_material
    print keypair

    # Launching EC2 Instances

    instance=ec2.create_instances(ImageId='ami-efd0428f',
                              SecurityGroups=['SecurityGroup_CodeApp'],
                              SecurityGroupIds=[SecurityGrp],
                              InstanceType='t2.micro',
                              MinCount=1,
                              MaxCount=1,
                              KeyName= keypair,
                              UserData= userdata,
                              IamInstanceProfile={
                                  'Name': EC2Role('InstanceProfileRoles')
                                  
                                  },
                                  
                              
                              TagSpecifications=[{
                                  'ResourceType': 'instance',
                                  'Tags':[
                                      {
                                          'Key': tagkey,
                                          'Value': tagvalue
                                          }]
                                  }
                                  
                                      ]
                              )

EC2Ins()
                                         
