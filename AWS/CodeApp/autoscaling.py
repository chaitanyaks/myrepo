import boto3
#import launchconfig
autos1=boto3.client('autoscaling')
#launchconfig():
ascaling=autos1.create_launch_configuration(
    LaunchConfigurationName='codeappLC111',
    ImageId='ami-efd0428f',
        #InstanceId='i-01d40f5f49970765f',
    InstanceType='t2.micro',
    KeyName='test1',
    SecurityGroups=['sg-86805cfe'],
        #UserData=''
        BlockDeviceMappings=[
                {
                    #'VirtualName':'ephemeral1',
                    'DeviceName':'/dev/sda1',
                    'Ebs': {
                         'SnapshotId': '1122',
                          'VolumeSize': 23,
                          'VolumeType': 'standard',
                          'DeleteOnTermination': True,
                         'Iops': 100,
                         'Encrypted': True
                          },
                  },
                
        ],
    InstanceMonitoring={
              'Enabled': True
    },
    IamInstanceProfile='asgrole',
    EbsOptimized=False,
    AssociatePublicIpAddress=True,
        #SubnetId='subnet-4854b63f'
        #PlacementTenancy=Default
)
   # return "LaunchConfigurationName"
#def asgroup():
asg=autos1.create_auto_scaling_group(
    AutoScalingGroupName='asg111',
    LaunchConfigurationName='codeappLC111',
    #InstanceId='i-01d40f5f49970765f',
        #ImageId='ami-efd0428f',
    MinSize=1,
    MaxSize=4,
    DesiredCapacity=1,
    DefaultCooldown=300,
    AvailabilityZones=['us-west-2b'],
##    HealthCheckType='EC2',
##    HealthCheckGracePeriod=300,
    NewInstancesProtectedFromScaleIn=True,
    VPCZoneIdentifier='subnet-4854b63f',
        
     Tags=[
            {
                'ResourceId': 'asg111',
                'ResourceType': 'auto-scaling-group',
                'Key': 'test10',
                'Value': 'test10',
                'PropagateAtLaunch': True
            },
          ]
)
print asg
    #return "AutoScalingGroupName"

#asgroup()
