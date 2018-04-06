import boto3
bucketloc=raw_input("Enter the Location of the bucket to run the revision: ")

codedeploy=boto3.client('codedeploy')
revision= codedeploy.create_deployment(
    applicationName='',
    deploymentGroupName='',
    revision={
        'revisionType': input("Choose the revision type, 1. S3 2. GitHub ")
        if revisionType==1:
            's3Location':{
                'bucket': bucketloc,
                'bundleType': 'zip'
                }
        elif revisionType==2:
            'gitHubLocation':{
                'repository':'',
                'commitId': ''
                }
        },
    targetInstances={
        'tagFilters':[{
            'Key': '',
            'Value': '',
            'Type': ''
            }]
        })
