import boto3
#from CodeDeployCodeApp import CD
codedeploy=boto3.client('codedeploy')
bucketloc=raw_input("Enter the Location of the bucket to run the revision: ")
def deploy():
    
    
    revision= codedeploy.create_deployment(
    applicationName='testx',
    deploymentGroupName='testx',
    revision={
        
        'revisionType': 'S3',
        's3Location':{
            'bucket': 'sindhu-ideatool',
            'key'
            'bundleType': 'zip'
            }
        
        },
    targetInstances={
        'tagFilters':[{
            'Key': 'Nexii-CodeApp',
            'Value': 'Nexii-CodeApp',
            'Type': 'KEY_AND_VALUE'
            }]
        })

deploy()
