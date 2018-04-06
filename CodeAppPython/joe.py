import boto3,botocore,time,yaml
import os
class submodules():
    def __init__(self):
         self.key=None
         self.sgname=None
         self.inspname=None
         self.polname=None
         self.rolename=None
    def yaml_loader(self,filepath):
        with open(filepath,"r")as file_descriptor:
            self.data=yaml.load(file_descriptor)
            print self.data
        return self.data
    
    def keyname(self,key):
        self.key=key
        k=boto3.client('ec2')
        
       
        kn= k.create_key_pair(
                KeyName=self.key
            )
        try:
    
            fw=open(kn['KeyName']+'.pem','w')
            f = fw.writelines(kn['KeyMaterial'])
            fw.close()
            print "Generated keyPair %s in the %s path "%(kn['KeyName'],os.path)


        except botocore.exceptions.ClientError as e:
            if 'InvalidKeyPair.Duplicate' in e.message:
                print "Keyapir %s already exists" %kn['KeyName']
            else:
                raise

        return kn['KeyName']

    def security_group(self,sgname,polname,rolename):
        self.sgname=sgname
        
        
        sg=boto3.client('ec2')
        
        sg1=sg.create_security_group(
                        GroupName=self.sgname,
                        Description='creating security group fro codeapp'
            )
        sgid1= sg1['GroupId']
    
        sgingress = sg.authorize_security_group_ingress(
                              GroupName=self.sgname,
                              GroupId=sgid1,
              
                              IpPermissions=[
                                  {
                                      'IpProtocol': 'TCP',
                                      'FromPort': 8080,
                                      'ToPort': 8080,
                                
                                      'IpRanges': [
                                          {         
                                              'CidrIp': '0.0.0.0/0'
                                          },
                                        ],
                          
                          
                                    },
                                    {
                                      'IpProtocol': 'TCP',
                                      'FromPort': 22,
                                      'ToPort': 22,
                                
                                      'IpRanges': [
                                           {         
                                              'CidrIp': '0.0.0.0/0'
                                            },
                                        ],
                                                    
                                     },
                                    {
                                      'IpProtocol': 'TCP',
                                      'FromPort': 3306,
                                      'ToPort': 3306,
                                
                                      'IpRanges': [
                                              {         
                                                  'CidrIp': '0.0.0.0/0'
                                              },
                                        ],
                                                   
                                    },
          ]
    
      )
        print "security group name:  %s \nsecurity group id:  %s:" %(self.sgname,sgid1)
        return sgid1

    def userdata(self):
            name="""#!/usr/bin/env python3
import os,sys,time
os.system('sudo apt-get -y update')
time.sleep(20)
os.system('sudo apt-get install -y ruby2.3')
os.system('sudo apt-get install -y awscli')
os.chdir('sudo cd /home/ubuntu')
os.system('aws s3 cp s3://aws-codedeploy-us-west-2/latest/install . --region us-west-2')
os.system('sudo chmod +x ./install')
os.system('sudo ./install auto')
"""
            print name
            time.sleep(20)
            return name
   
    def iamrole(self,inspname,polname,rolename):
            self.inspname=inspname
            self.polname=polname
            self.rolename=rolename
            
            iam=boto3.client('iam')
            
            policy1="""{

             "Version": "2012-10-17",
             "Statement": [
                {
                  "Effect": "Allow",
                  "Action": [
                             "ec2:RunInstances",
                             "ec2:AssociateIamInstanceProfile",
                             "ec2:ReplaceIamInstanceProfileAssociation"
                             ],
                  "Resource": "*"
                },
                {
                  "Effect": "Allow",
                  "Action": "iam:PassRole",
                  "Resource": "*"
                }
              ]
            }"""
            policy2="""{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":["ec2.amazonaws.com"]},"Action":["sts:AssumeRole"]}]}"""
            
            cp = iam.create_instance_profile(InstanceProfileName=self.inspname)
            cp1=iam.create_policy(PolicyName=self.polname,
                                  PolicyDocument=policy1
                )
            cr = iam.create_role(RoleName=self.rolename,AssumeRolePolicyDocument=policy2)
            cins=iam.add_role_to_instance_profile(
                                                InstanceProfileName=self.inspname,
                                                RoleName=self.rolename
            )
            print "instance profile name: ",cp['InstanceProfile']['InstanceProfileName']
            return cp['InstanceProfile']['InstanceProfileName']
    
filepath='test1yaml.yaml'    
m=submodules()
data=m.yaml_loader(filepath)
print data
ak=m.keyname(data['servicetype']['key'])

asp=m.security_group(data['servicetype']['sgname'])

au=m.userdata()

aiam=m.iamrole(data['servicetype']['inspname'],data['servicetype']['polname'],data['servicetype']['rolename'])



#print cp['InstanceProfile']['InstanceProfileName']
