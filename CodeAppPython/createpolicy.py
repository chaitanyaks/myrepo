import boto3
import logging

logging.basicConfig(level = logging.INFO)

def createpolicy(policyname):
    try:
        client = boto3.client('iam')
        policy = client.create_policy(
    		PolicyName=policyname,
    		PolicyDocument="""{
              "Statement": [
                {
                  "Effect": "Allow",
                  "Action": "*",
                  "Resource": "*"
                }
              ],
              "Version": "2012-10-17"
            }"""
    		)
        logging.info("created policy and arn is {0}".format(policy['Policy']['Arn']))
        return policy['Policy']['Arn']


    except Exception as err:
    	logging.exception(err)

if __name__ == "__main__":
	policyname = "codebuildservicetest1"
 	print createpolicy(policyname)