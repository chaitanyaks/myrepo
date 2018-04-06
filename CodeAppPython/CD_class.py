import boto3
from test_policies import AWSDeployEnv
class codedeploy():
    def __init__(self):
        self.codedeploy=None

    def connection(self):
        #AWS_Roles.connect(self)
        self.codedeploy=boto3.client('codedeploy')
        

    def application(self,name=None):
        self.appname=name
        app=self.codedeploy.create_application(applicationName=name)
        return app
        
    def deploymentgroup(self,role1,name=None,key1=None,value1=None):
        deploymentgroup=self.codedeploy.create_deployment_group(
            applicationName=self.appname,
            deploymentGroupName=name,
            ec2TagFilters=[{
                'Key': key1,
                'Value': value1,
                'Type': 'KEY_AND_VALUE'
                },
            ],

            serviceRoleArn= role
            )
        return app,deploymentgroup
        
        
B=codedeploy()

B.connect()
    
ec2_asmdoc=B.assumepolicy(t='ec2')
print "ec2_asmdoc:",ec2_asmdoc
codebuild_asmdoc=B.assumepolicy(t='codebuild')
codedeploy_asmdoc=B.assumepolicy(t='codedeploy')
codepipeline_asmdoc=B.assumepolicy(t='codepipeline')
ec2poldoc=B.policydocument(t='ec2')
print "ec2poldoc:",ec2poldoc
cbpoldoc=B.policydocument(t='codebuild')
cdpoldoc=B.policydocument(t='codedeploy',)
dppoldoc=B.policydocument(t='codepipeline')
ec2policy=B.policy(t='ec2',name='ec21')
    
cbpolicy=B.policy(t='codebuild',name='codebuild1')
cdpolicy=B.policy(t='codedeploy',name='codedeploy1')
cppolicy=B.policy(t='codepipeline',name='codepipeline1')
ec2rolename,ec2rolearn=B.role(t='ec2',name='ec21')
cbrolename,cbrolearn=B.role(t='codebuild',name='codebuild1')
cdrolename,cdrolearn=B.role(t='codedeploy',name='codedeploy1')
cprolename,cprolearn=B.role(t='codepipeline',name='codepipeline1')
instanceprofile=B.instanceprofile(t=ec2rolename,name='ec2insprf1')
B.attachpolicy(t='ec2')
B.attachpolicy(t='codebuild')
B.attachpolicy(t='codedeploy')
B.attachpolicy(t='codepipeline')
SG=B.securitygroup(name='secgrp1')
keypair = B.keypair(name='keypair1')
userdata = B.userdata()
key,value=B.EC2Ins(image_id='ubuntu16',tagkey='keys1',tagvalue='values1',role=instanceprofile,userdata=userdata)
B.connection()
appname=B.application(name='test2')
app,dg=B.deploymentgroup(name='DG',role1=cdrolearn,key1=key,value1=value)
print "ec2_asmdoc:",ec2_asmdoc
print "ec2poldoc:",ec2poldoc

print "appname:",appname
print "app:",app
print "dg:",dg
    
'''if __name__== "__main__":
    B=codedeploy()
    B.connect()
    
    ec2_asmdoc=B.assumepolicy(t='ec2')
    print "ec2_asmdoc:",ec2_asmdoc
    codebuild_asmdoc=B.assumepolicy(t='codebuild')
    codedeploy_asmdoc=B.assumepolicy(t='codedeploy')
    codepipeline_asmdoc=B.assumepolicy(t='codepipeline')
    ec2poldoc=B.policydocument(t='ec2')
    print "ec2poldoc:",ec2poldoc
    cbpoldoc=B.policydocument(t='codebuild')
    cdpoldoc=B.policydocument(t='codedeploy',)
    dppoldoc=B.policydocument(t='codepipeline')
    ec2policy=B.policy(t='ec2',name='ec21')
    
    cbpolicy=B.policy(t='codebuild',name='codebuild1')
    cdpolicy=B.policy(t='codedeploy',name='codedeploy1')
    cppolicy=B.policy(t='codepipeline',name='codepipeline1')
    ec2rolename,ec2rolearn=B.role(t='ec2',name='ec21')
    cbrolename,cbrolearn=B.role(t='codebuild',name='codebuild1')
    cdrolename,cdrolearn=B.role(t='codedeploy',name='codedeploy1')
    cprolename,cprolearn=B.role(t='codepipeline',name='codepipeline1')
    instanceprofile=B.instanceprofile(t=ec2rolename,name='ec2insprf1')
    B.attachpolicy(t='ec2')
    B.attachpolicy(t='codebuild')
    B.attachpolicy(t='codedeploy')
    B.attachpolicy(t='codepipeline')
    SG=B.securitygroup(name='secgrp1')
    keypair = B.keypair(name='keypair1')
    userdata = B.userdata()
    key,value=B.EC2Ins(image_id='ubuntu16',tagkey='keys1',tagvalue='values1',role=instanceprofile,userdata=userdata)
    B.connection()
    appname=B.application(name='test2')
    app,dg=B.deploymentgroup(name='DG',role1=cdrolearn,key1=key,value1=value)
    print "ec2_asmdoc:",ec2_asmdoc
    print "ec2poldoc:",ec2poldoc

    print "appname:",appname
    print "app:",app
    print "dg:",dg'''
