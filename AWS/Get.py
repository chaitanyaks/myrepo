'''import boto3


# Create IAM client
iam = boto3.client('iam')

# Get a policy
response = iam.get_policy(
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)
print response['Policy']

IamInstanceProfile={
                                  'Arn': 'arn:aws:iam::384461511758:role/CodeDeployDemo-EC2-Instance-Profile'
                                  'Name': 'CodeDeployDemo-EC2-Instance-Profile'
                                  },
'''

AssumeRolePolicy= { 'Version' : '2012-10-17','Statement':[{"Effect": "Allow","Principal": { "Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}
print AssumeRolePolicy
