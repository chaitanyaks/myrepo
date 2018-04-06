#!/usr/bin/env python
import boto3
import logging
def createrole(rolename):
    logging.basicConfig(level = logging.INFO)
    client = boto3.client('iam')
    response = client.create_role(
        RoleName = rolename,
        AssumeRolePolicyDocument = """{
              "Statement": [
                {
                  "Effect": "Allow",
                  "Principal": {
                    "Service": [
                      "codebuild.amazonaws.com"
                    ]
                  },
                  "Action": [
                    "sts:AssumeRole"
                  ]
                }
              ]
            }"""
        )

    try:
        logging.info("created a role \n arn is '{0}'".format(response['Role']['Arn']))
        return response['Role']['Arn']
    except Exception as err:
        logging.exceptiontion(err)

if __name__ == "__main__":
    #rolename = "pythontestrole" 
    rolename = raw_input("enter the role name to create: ")
    createrole(rolename)
