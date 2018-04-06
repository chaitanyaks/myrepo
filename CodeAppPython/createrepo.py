#!/usr/bin/env python
import boto3
import logging
def createrepo(reponame):
    logging.basicConfig(level = logging.INFO)
    client = boto3.client('codecommit')
    response = client.create_repository(
        repositoryName=reponame,
        repositoryDescription='This repo is created by Sagar to test creation of\
     using python script'
    )

    try:
        logging.info("created a repo, and below is the URL to clone \n{0}".format(response['repositoryMetadata']['cloneUrlHttp']))
        return format(response['repositoryMetadata']['cloneUrlHttp'])
    except Exception as err:
        logging.exception(err)

if __name__ == "__main__":
    #reponame = raw_input("enter repo name to create : ")
    reponame = "testrepo"
    print createrepo('CA')

##a=createrepo('CA')
##print a
