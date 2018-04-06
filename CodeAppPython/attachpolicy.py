import boto3
import logging

logging.basicConfig(level = logging.INFO)

def attachpolicy(rolename,arn):
    try:
        client = boto3.client('iam')
        #policy = iam.Policy(arn)
        response = client.attach_role_policy(
            RoleName=rolename,
            PolicyArn=arn
            )
        logging.info("attached policy with arn {0} to role {1}".format(arn,rolename))
        return True
    except Exception as err:
        logging.exception(err)

