import boto3,json,time
#from IAMRoles import EC2Role
#import securitygroup,keypair,userdata

class Aws_Operations(object):
    def __init__(self):
        self.ec2=None
        self.iam = None
        self.client = None

    def connect(self):
        """
        asss
        connect(self):connect is used to connect AWS.
        Variables:

        Return:
            None
        
        
        """


        self.ec2 = boto3.resource('ec2')
        self.iam = boto3.client('iam')
        self.client = boto3.client('ec2')
        
    def Assumepolicy(self):
        """
        variables:
        
        Asmpolicy[0]: This assume policy document is for EC2 instance
        Asmpolicy[1]: This assume policy document is for codebuild
        Asmpolicy[2]: This assume policy document is for codedeploy
        Asmpolicy[3]: This assume policy document is for codepipeline

        return:
        Assume policy document with JSON structure to create role for EC2 instance,codebuild,codedeploy,codepipeline
        
        """

        EC2_Asmpolicy = { 'Version' : '2012-10-17','Statement':[{"Effect" : "Allow","Principal" : { "Service" : "ec2.amazonaws.com"},"Action" : "sts:AssumeRole"}]}
        EC2_Asmpolicy_json = json.dumps(EC2_Asmpolicy,indent = 2)
        
        CB_Asmpolicy = {'Version' : '2012-10-17', "Statement": [{"Effect": "Allow","Principal": {"Service": ["codebuild.amazonaws.com"]},"Action": ["sts:AssumeRole"]}]}
        CB_Asmpolicy_json = json.dumps(CB_Asmpolicy, indent = 2)

        CD_Asmpolicy = {'Version' : '2012-10-17','Statement' : [{"Sid" : "1","Effect" : "Allow","Principal" : {"Service" : ["codedeploy.us-west-2.amazonaws.com"]},"Action": "sts:AssumeRole"}]}
        CD_Asmpolicy_json = json.dumps(CD_Asmpolicy,indent = 2)

        CP_Asmpolicy = {'Version' : '2012-10-17',"Statement" : [{"Effect" : "Allow","Principal" : {"Service" : ["codepipeline.amazonaws.com"]},"Action" : ["sts:AssumeRole"]}]}
        CP_Asmpolicy_json = json.dumps(CP_Asmpolicy, indent = 2)

        time.sleep(10)

        return EC2_Asmpolicy_json, CB_Asmpolicy_json, CD_Asmpolicy_json, CP_Asmpolicy_json
        

    
    def policydoc(self):

        policydoc_ec2 = {'Version' : '2012-10-17','Statement' : [{"Action" : ["ec2:*","codedeploy:*","autoscaling:Describe*","s3:Get*","s3:List*"],"Effect" : "Allow","Resource" : "*"}]}
        EC2_policy_json = json.dumps(policydoc_ec2,indent = 2)

        policydoc_cb = {'Version' : '2012-10-17', "Statement": [{"Effect": "Allow","Action": "*","Resource": "*"}]}
        CB_policy_json = json.dumps(policydoc_cb, indent = 2)

        policydoc_cd = {'Version' : '2012-10-17','Statement' : [{"Effect" : "Allow","Resource" : ["*"],"Action" : ["ec2:Describe*"]},{"Effect" : "Allow","Resource" : ["*"],"Action": ["autoscaling:*"]}]}
        CD_policy_json = json.dumps(policydoc_cd,indent = 2)

        policydoc_cp = {'Version': '2012-10-17',  "Statement": [{"Action" : ["codecommit:*","codebuild:*"],"Resource" : "*","Effect" : "Allow"},
                                                       {"Action" : ["s3:GetObject","s3:GetObjectVersion","s3:GetBucketVersioning"],"Resource": "*","Effect": "Allow"},
                                                       {"Action" : ["s3:PutObject"],"Resource" : ["arn:aws:s3:::codepipeline*","arn:aws:s3:::elasticbeanstalk*"],"Effect": "Allow"},
                                                       {"Action" : ["codedeploy:*"],"Resource" : "*","Effect": "Allow"},
                                                       {"Action" : ["ec2:*","elasticloadbalancing:*","autoscaling:*","cloudwatch:*","s3:*","sns:*","cloudformation:*","rds:*","sqs:*","ecs:*","iam:PassRole"],"Resource": "*","Effect": "Allow"},
                                                       {"Action" : ["lambda:InvokeFunction","lambda:ListFunctions"],"Resource": "*","Effect": "Allow"}]}
        CP_policy_json = json.dumps(policydoc_cp, indent = 2)

        time.sleep(10)

        return EC2_policy_json,CB_policy_json,CD_policy_json,CP_policy_json

    def policy(self,**policy):
        print policy[0],policy[1],policy[2],policy[3]

        EC2_poldoc,CB_poldoc,CD_poldoc,CP_poldoc = self.policydoc()
        
        EC2_policy = self.iam.create_policy(PolicyName = policy[0],PolicyDocument = EC2_poldoc, Description = 'Policy for EC2')
        CB_policy = self.iam.create_policy(PolicyName = policy[1],PolicyDocument = CB_poldoc, Description = 'Policy for codebuild')
        CD_policy = self.iam.create_policy(PolicyName = policy[2],PolicyDocument = CD_poldoc, Description = 'Policy for codedeploy')
        CP_policy = self.iam.create_policy(PolicyName = policy[3], PolicyDocument = CP_poldoc, Description = 'Policy for Codepipeline')

        EC2_policyres = EC2_policy['Policy']['Arn']
        CB_policyres = CB_policy['Policy']['Arn']
        CD_policyres = CD_policy['Policy']['Arn']
        CP_policyres = CP_policy['Policy']['Arn']

        time.sleep(10)
        print "check:",EC2_policyres, CB_policyres, CD_policyres, CP_policyres
        return EC2_policyres, CB_policyres, CD_policyres, CP_policyres

    def role(self,*roles):
        
        EC2_Role,CB_Role,CD_Role,CP_Role = self.Assumepolicy()
        
        role_EC2 = self.iam.create_role(RoleName = roles[0] ,AssumeRolePolicyDocument = EC2_Role ,Description = 'Instance Profile role for EC2')

        role_CB = self.iam.create_role(RoleName = roles[1], AssumeRolePolicyDocument = CB_Role, Description = 'Role for codebuild')

        role_CD = self.iam.create_role(RoleName= roles[2], AssumeRolePolicyDocument = CD_Role, Description = 'Role for CodeDeploy')

        role_CP = self.iam.create_role(RoleName = roles[3], AssumeRolePolicyDocument = CP_Role, Description = 'Role for Codepipeline')

        self.role1 = role_EC2['Role']['RoleName']
        self.role2 = role_CB['Role']['RoleName']
        self.role3 = role_CD['Role']['RoleName']
        self.role4 = role_CP['Role']['RoleName']

        #EC2_Roleres = role_EC2['Role']['Arn']
        CB_roleres = role_CB['Role']['Arn']
        CD_roleres = role_CD['Role']['Arn']
        CP_roleres = role_CP['Role']['Arn']

        time.sleep(10)

        return CB_roleres, CD_roleres, CP_roleres
        
        

    def Attachpolicy(self,role,policy):
               
        pol1,pol2,pol3,pol4 = self.policy()
        print pol1,pol2,pol3,pol4

        EC2_AttachPolicy = self.iam.attach_role_policy(RoleName = self.role1,PolicyArn = pol1)
        CB_AttachPolicy = self.iam.attach_role_policy(RoleName = self.role1, PolicyArn = pol2)
        CD_AttachPolicy = self.iam.attach_role_policy(RoleName = self.role1, PolicyArn = pol3)
        CD_AttachPolicy = self.iam.attach_role_policy(RoleName = self.role1, PolicyArn = pol4)

        time.sleep(10)

    def InstanceProfile(self,ProfName=None):
         EC2_InstanceProfile = self.iam.create_instance_profile(InstanceProfileName = ProfName)
         AttachInstanceProfile = iself.iam.add_role_to_instance_profile(InstanceProfileName = EC2_InstanceProfile['InstanceProfile']['InstanceProfileName'],RoleName = self.role1)

         EC2_InstanceProf_Res = EC2_InstanceProfile['InstanceProfile']['InstanceProfileName']

         time.sleep(10)

         return EC2_InstanceProf_Res
        
        

    '''def SG(self,SG_Name=None):
        self.SG_Name = SG_Name
        security = self.client.create_security_group(GroupName = SG_Name, Description = 'security group for ec2 instance')
        security_id = security['GroupId']

        rule = client.authorize_security_ingress(GroupName = Name, GroupId = self.security_id,
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
        return security_id

    def keypair(self,keypair_Name=0):
        key = ec2.create_key_pair(KeyName = keypair_Name)
        fp=open(keypair+'.pem','w')
        fp.writelines(key.key_material)
        fp.close()
        
        return key.name

    def userdata(self):
        
        user_data = """#!/usr/bin/env python3
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
"""
        return user_data
        

        
        
    def EC2Ins(self,image_id,instance_type,tagkey,tagvalue,role=None):
        instance= self.ec2.create_instances(ImageId = image_id,
                                            SecurityGroups = [self.SG_Name],
                                            SecurityGroupIds = SG(),
                                            InstanceType = instance_type,
                                            MinCount = 1,
                                            MaxCount = 1,
                                            KeyName = keypair(),
                                            UserData = user_data(),
                                            IamInstanceProfile={
                                                'Name':
                                                },
                                            TagSpecifications=[{
                                                'ResourceType': 'instance',
                                                'Tags':[{
                                                    'Key': tagkey,
                                                    'Value': tagvalue
                                                    }
                                                ]
                                                }]
                                            )
        instance_id=instance[0].id
        response = self.client.describe_tags(
            Filters=[{
                'Name': 'resource_id',
                'Value': [instance_id,],
                },
            ],
            )
        key= response['Tags'][0]['Key']
        value= response['Tags'][0]['Value']
        return key, value
        pass'''

obj = Aws_Operations()
obj.connect()
obj.Assumepolicy()
obj.policydoc()
obj.policy('ec2pol5','cbpol5','cdpol5','cppol5')
obj.role('ec2rol4','cbrol4','cdrol4','cprol4')
obj.Attachpolicy()
obj.InstanceProfile('ec2ins2')

