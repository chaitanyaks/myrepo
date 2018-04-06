import boto3,json,time,botocore
import pdb
#pdb.set_trace()

class AWSDeployEnv():
    def __init__(self):
        self.ec2=None
        self.iam = None
        self.client = None

    def connect(self):
        
        self.ec2 = boto3.resource("ec2")
        self.iam = boto3.client("iam")
        self.client = boto3.client("ec2")
        

    def assumepolicy(self,t=None):

        """
        Creates assume policy document for roles
        
        :type assumepolicydocument: dictionary
        :param assumepolicydocument: Based on the AWS service, respective principal will be passed to the JSON assume policy document.

        :type assume_policy_json: JSON
        :param assume_policy_json: Dumps the assume_policy into JSON structure.
        """
        try:
            
            assumepolicydocument ={"ec2":"ec2.amazonaws.com", "codebuild":"codebuild.amazonaws.com", "codedeploy":"codedeploy.us-west-2.amazonaws.com","codepipeline":"codepipeline.amazonaws.com"}
            assume_service = assumepolicydocument[t]
            assume_policy = {"Version":"2012-10-17","Statement":[{"Effect" : "Allow","Principal" : { "Service" : assume_service},"Action" : "sts:AssumeRole"}]}
            assume_policy_json = json.dumps(assume_policy,indent = 2)
            time.sleep(5)
        
            return assume_policy_json
        except Exception as a:
            if EntityAlreadyExists in a:
                print "Assume policy document already for %s exists: " %t,a.message

    def policydocument(self,t=None):
        """
        Policy document creation for the AWS services.
        """

        try:
            
            statement = {'ec2':[{"Action" :["ec2:*","codedeploy:*","autoscaling:Describe*","s3:Get*","s3:List*"] ,"Effect" : "Allow","Resource" : "*"}],
                     'codebuild': [{"Effect": "Allow","Action": "*","Resource": "*"}],
                     'codedeploy': [{"Effect" : "Allow","Resource" : ["*"],"Action" : ["ec2:Describe*"]},{"Effect" : "Allow","Resource" : ["*"],"Action": ["autoscaling:*"]}],
                     'codepipeline':[{"Action" : ["codecommit:*","codebuild:*"],"Resource" : "*","Effect" : "Allow"},
                                                       {"Action" : ["s3:GetObject","s3:GetObjectVersion","s3:GetBucketVersioning"],"Resource": "*","Effect": "Allow"},
                                                       {"Action" : ["s3:PutObject"],"Resource" : ["arn:aws:s3:::codepipeline*","arn:aws:s3:::elasticbeanstalk*"],"Effect": "Allow"},
                                                       {"Action" : ["codedeploy:*"],"Resource" : "*","Effect": "Allow"},
                                                       {"Action" : ["ec2:*","elasticloadbalancing:*","autoscaling:*","cloudwatch:*","s3:*","sns:*","cloudformation:*","rds:*","sqs:*","ecs:*","iam:PassRole"],"Resource": "*","Effect": "Allow"},
                                                       {"Action" : ["lambda:InvokeFunction","lambda:ListFunctions"],"Resource": "*","Effect": "Allow"}]}
            policydocument= {'Version' : '2012-10-17','Statement' : statement[t]}
            policydocument_json = json.dumps(policydocument,indent = 2)
            time.sleep(5)

            return policydocument_json
        except Exception as b:
            print "Policy document already exists: ", b.message

    def policy(self,t=None,name=None):
        """
        Policy creation for the AWS Services
        """
        try:
            
            self.policyelements = {'ec2': ec2poldoc,'codebuild': cbpoldoc, 'codedeploy': cdpoldoc, 'codepipeline': dppoldoc}
            policy = self.iam.create_policy(PolicyName = name,PolicyDocument = self.policyelements[t] , Description = 'Policy creation for the AWS services')
            time.sleep(5)

            return policy['Policy']['Arn']
        except Exception as c:
            print "Policy already exists for %s: " %t,c.message

    def role(self,t=None,name=None):
        """
        Role creation for the AWS Services
        """

        try:
            
            assumepolicy_document = {'ec2': ec2_asmdoc, 'codebuild': codebuild_asmdoc, 'codedeploy': codedeploy_asmdoc, 'codepipeline': codepipeline_asmdoc }
        
            role = self.iam.create_role(RoleName = name ,AssumeRolePolicyDocument = assumepolicy_document[t] ,Description = 'Role creation for the AWS Services')
            time.sleep(5)

            return role['Role']['RoleName'], role['Role']['Arn']
        except Exception as d:
            print "Role already exists: ",d.message

    def attachpolicy(self,t=None):
        """
        Attaching policy to the role.
        """
        #pdb.set_trace()
        try:
            elements={ec2rolename:ec2policy}#,cbrolename:cbpolicy,cdrolename:cdpolicy,cprolename:cppolicy}
            role={'ec2':ec2rolename,'codebuild': cbrolename,'codedeploy': cdrolename, 'codepipeline': cprolename }
            policyarn={'ec2':ec2policy,'codebuild': cbpolicy, 'codedeploy': cdpolicy, 'codepipeline': cppolicy}
            attachPolicy1 = self.iam.attach_role_policy(RoleName = role[t],PolicyArn = policyarn[t])
            time.sleep(5)
        except Exception as e:
            print "Policy already attached to the role: ", e.message

    def instanceprofile(self,t=None,name=None):
        
        try:
            instanceprof = self.iam.create_instance_profile(InstanceProfileName = name)
            attachinstanceprofile = self.iam.add_role_to_instance_profile(InstanceProfileName = instanceprof['InstanceProfile']['InstanceProfileName'],RoleName = t)
            res = instanceprof['InstanceProfile']['InstanceProfileName']
            
            time.sleep(10)
            print res

            return res
        except Exception as f:
            print "Instance profile already exists: ", f.message

    def securitygroup(self,name=None):
        self.sg=name
        security = self.client.create_security_group(GroupName = name, Description = 'security group for ec2 instance')
        security_id = security['GroupId']

        rule = self.client.authorize_security_group_ingress(GroupName = name, GroupId = security_id,
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
        time.sleep(10)
        return security_id

    def keypair(self,name=None):
        
        key = self.ec2.create_key_pair(KeyName = name)
        fp=open(key.name+'.pem','w')
        fp.writelines(key.key_material)
        fp.close()

        time.sleep(10)
        
        return key.name

    def userdata(self):
        userdata = """#!/usr/bin/env python3
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
        time.sleep(5)
        return userdata

    def EC2Ins(self,image_id=None,instancetype='t2.micro',tagkey=None,tagvalue=None,role=None,userdata=None):
        images= {'ubuntu16': 'ami-efd0428f', 'ubuntu14':'ami-7c22b41c' }
        
        instance= self.ec2.create_instances(ImageId = images[image_id],
                                            SecurityGroups = [self.sg],
                                            SecurityGroupIds = [SG],
                                            InstanceType = instancetype,
                                            MinCount = 1,
                                            MaxCount = 1,
                                            KeyName = keypair,
                                            UserData = userdata,
                                            IamInstanceProfile={
                                                'Name': role
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
        time.sleep(20)
        instance_id=instance[0].id
        response = self.client.describe_tags(
            Filters=[{
                'Name': 'resource-id',
                'Values': [instance_id,],
                },
            ],
            )
        key= response['Tags'][0]['Key']
        value= response['Tags'][0]['Value']
        return key, value
    
        


'''if __name__ == "__main__":
    A=AWSDeployEnv()
    A.connect()
    ec2_asmdoc=A.assumepolicy(t='ec2')
    codebuild_asmdoc=A.assumepolicy(t='codebuild')
    codedeploy_asmdoc=A.assumepolicy(t='codedeploy')
    codepipeline_asmdoc=A.assumepolicy(t='codepipeline')
    ec2poldoc=A.policydocument(t='ec2')
    cbpoldoc=A.policydocument(t='codebuild')
    cdpoldoc=A.policydocument(t='codedeploy',)
    dppoldoc=A.policydocument(t='codepipeline')
    ec2policy=A.policy(t='ec2',name='ec2')
    cbpolicy=A.policy(t='codebuild',name='codebuild')
    cdpolicy=A.policy(t='codedeploy',name='codedeploy')
    cppolicy=A.policy(t='codepipeline',name='codepipeline')
    ec2rolename,ec2rolearn=A.role(t='ec2',name='ec2')
    cbrolename,cbrolearn=A.role(t='codebuild',name='codebuild')
    cdrolename,cdrolearn=A.role(t='codedeploy',name='codedeploy')
    cprolename,cprolearn=A.role(t='codepipeline',name='codepipeline')
    instanceprofile=A.instanceprofile(t=ec2rolename,name='ec2insprf')
    A.attachpolicy(t='ec2')
    A.attachpolicy(t='codebuild')
    A.attachpolicy(t='codedeploy')
    A.attachpolicy(t='codepipeline')
    SG=A.securitygroup(name='secgrp')
    keypair = A.keypair(name='keypair1')
    userdata = A.userdata()
    key,value=A.EC2Ins(image_id='ubuntu16',tagkey='keys',tagvalue='values',role=instanceprofile,userdata=userdata)
    



    print "ec2:",ec2_asmdoc
    print "codebuild:",codebuild_asmdoc
    print "codedeploy:",codedeploy_asmdoc
    print "codepipeline:",codepipeline_asmdoc
    print "ec2poldoc: ",ec2poldoc
    print "cbpoldoc: ",cbpoldoc
    print "cdpoldoc: ",cdpoldoc
    print "dppoldoc: ",dppoldoc
    print "ec2policy:",ec2policy
    print "cbpolicy:",cbpolicy
    print "cdpolicy:",cdpolicy
    print "SG:",SG
    print "key,value:", key,value



    #attatch=attach_policy(policy=[ec2,cd])'''
