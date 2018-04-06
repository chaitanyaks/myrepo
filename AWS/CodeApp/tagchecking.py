import boto3
client=boto3.client('ec2')
response = client.describe_tags(
    Filters=[
        {
            'Name': 'resource-id',
            'Values': [
                'i-038a2770edf893202',
            ],
        },
    ],
)

print(response)
