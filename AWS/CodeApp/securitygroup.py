import boto3

client=boto3.client('ec2')

def securitygroup(Name):
    security=client.create_security_group(GroupName=Name,Description='Security group for codeapp')
    SecurityGrp=security['GroupId']
    
    rule=client.authorize_security_group_ingress(GroupName=Name,
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
    return SecurityGrp

