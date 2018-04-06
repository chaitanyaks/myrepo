import boto3
ec2 = boto3.resource('ec2')
Sg=boto3.client('ec2')
securitygroup=Sg.create_security_group(GroupName='SecurityGroup_CodeApp',Description='Security group for codeapp')
SecurityGrp=securitygroup['GroupId']
print SecurityGrp
rule=Sg.authorize_security_group_ingress(GroupName='SecurityGroup_CodeApp',GroupId=SecurityGrp,
                                         IpPermissions:[
                                             {
                                             'IpProtocol': 'tcp',
                                             'FromPort':22,
                                             'ToPort':22,
                                             'IpRanges':[{
                                                 'CidrIp': '0.0.0.0/0'
                                                 }]
                                              },
                                             {
                                                 
                                            
                                                 
                                                                                                  
                                                        
                                            ] )

#print securitygrp
#instance=ec2.create_instances(
