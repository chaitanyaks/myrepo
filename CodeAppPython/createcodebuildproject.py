#!/usr/bin/env python
import boto3
import logging
import createrepo,rolecreate,attachpolicy,createpolicy
logging.basicConfig(level = logging.INFO)
def createproject(projectname,rolename):
    client = boto3.client('codebuild')
    response = client.create_project(
        name=projectname+"buildproject",
        description='This project is created by Sagar as part of python for AWS',
        source={
            'type': 'CODECOMMIT',
            'location': createrepo.createrepo(projectname+"repo")
        },
        artifacts={
        'type': 'S3',
        'location': 'sagarbucketforlearningdevops',
        'namespaceType': 'NONE',
        'name': projectname+'artifact',
        'packaging': 'ZIP'
        },
        environment={
        'type': 'LINUX_CONTAINER',
        'image': 'aws/codebuild/java:openjdk-8',
        'computeType': 'BUILD_GENERAL1_SMALL'
        },
        serviceRole=rolename,#rolecreate.createrole(projectname+"role"),
        timeoutInMinutes=15,
        tags=[
            {
                'key': 'owner',
                'value': 'Codebuildproject'
            },
        ]
    )

# try:
#     logging.info("created a code Build project, and below is the URL to clone \n{0}".format(response))
# except Exception as err:
#     logging.exception(err)

if __name__ == "__main__":
    try:
        projectname = raw_input("enter project name : ")
        servicename = "codebuild"#raw_input("enter service name : ")
        codebuildpolicyarn = "arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess"
        rolecreate.createrole(projectname+"role")
        codebuildpolicyarn = createpolicy.createpolicy(projectname+servicename+"policy")
        attachpolicy.attachpolicy(projectname+"role",codebuildpolicyarn)
        response =  createproject(projectname,projectname+"role")
        logging.info("created a code Build project with name {0}".format(projectname+"buildproject"))
    except Exception as err:
        logging.exception(err)

