import boto3,json,time
from IAMRoles import EC2Role
import securitygroup,keypair,userdata

ec2 = boto3.resource('ec2')
iam = boto3.client('iam')
client=boto3.client('ec2')

secgrp=raw_input("Enter the security group name: ")
keypairname=raw_input("Enter keypair name: ")

def EC2Ins(*args):
    """
    Creates EC2 Instance with the following hardware requirments
    1. OS: Ubuntu 16.0
    2. InstanceType: t2.micro
    3. SecurityPorts: 22,8080,3306
    """
   
    InstProf= EC2Role()
    
    

    instance=ec2.create_instances(ImageId='ami-efd0428f',
                              SecurityGroups=[secgrp],
                              SecurityGroupIds=[securitygroup.securitygroup(secgrp)],
                              InstanceType='t2.micro',
                              MinCount=1,
                              MaxCount=1,
                              KeyName= keypair.keypair(keypairname),
                              UserData= userdata.userdata('userdataEC2'),
                              IamInstanceProfile={
                                  'Name': InstProf
                                  
                                  },
                                  
                              
                              TagSpecifications=[{
                                  'ResourceType': 'instance',
                                  'Tags':[
                                      {
                                          'Key': args[0],
                                          'Value': args[1]
                                          }]
                                  }
                                  
                                      ]
                              )
    
    instance_id=instance[0].id
    print instance_id
    response = client.describe_tags(
    Filters=[{
            'Name': 'resource-id',
            'Values': [
                instance_id,],
        },
    ],
    )
    key= response['Tags'][0]['Key']
    value= response['Tags'][0]['Value']
    
    return key, value
    



