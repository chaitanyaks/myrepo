import boto3,json,time

class AWS_services_del():
    def __init__(self):
        self.ec2=None
        self.iam=None
        self.client=None
    def connect(self):

        self.ec2 = boto3.resource("ec2")
        self.iam = boto3.client("iam")
        self.client = boto3.client("ec2")

    
    def remove_role_from_instanceprofile(self,instanceprofile=None,rolename=None):
        try:
            remove=self.iam.remove_role_from_instance_profile(InstanceProfileName=instanceprofile,RoleName=rolename)
        except Exception as a:
            print "Role was removed from instance profile policy:", a.message          
            
        
    def dettach_role_policy(self,rolename=None,policyarn="arn:aws:iam::384461511758:policy/",name=None):
        try:

            detach=self.iam.detach_role_policy(RoleName=rolename,PolicyArn="arn:aws:iam::384461511758:policy/"+name)
        
        except Exception as b:
            print "policy was detached from the role:", b.message
    def role_delete(self,name=None):
        try:
            
            role = self.iam.delete_role(RoleName = name)

        except Exception as c:
            print "Role does not found:", c.message

    def policy_delete(self,arn="arn:aws:iam::384461511758:policy/",name=None):
        try:
            policy=self.iam.delete_policy(PolicyArn=arn+name)
        except Exception as d:
            print"Policy does not found:", d.message

    def instanceprof_delete(self,name):
        try:
            insprf=self.iam.delete_instance_profile(InstanceProfileName=name)
        except Exception as e:
            print"Instance profile does not found:", e.message

    def keypair_delete(self,name=None):
        delete=self.client.delete_key_pair(KeyName=name)

    def securitygroup_delete(self,name=None):
        delete=self.client.delete_security_group(GroupName=name)
        
            
    
            

if __name__ == "__main__":
    A=AWS_services_del()
    A.connect()
    A.dettach_role_policy(rolename='ec2',name='ec2')
    A.dettach_role_policy(rolename='codebuild',name='codebuild')
    A.dettach_role_policy(rolename='codedeploy',name='codedeploy')
    A.dettach_role_policy(rolename='codepipeline',name='codepipeline')
    A.remove_role_from_instanceprofile(instanceprofile='ec2insprf1',rolename='ec2')
    A.role_delete(name='ec2')
    A.role_delete(name='codebuild')
    A.role_delete(name='codedeploy')
    A.role_delete(name='codepipeline')
    A.policy_delete(name='ec2')
    A.policy_delete(name='codebuild')
    A.policy_delete(name='codedeploy')
    A.policy_delete(name='codepipeline')
    A.instanceprof_delete(name='ec2insprf1')
    A.keypair_delete(name='keypair2')
    A.securitygroup_delete(name='secgrp1')

