import boto3
import IAMRoles,createrepo,rolecreate,attachpolicy,createpolicy
import DevEnv,createrepo,createcodebuildproject,Codedeploy

client=boto3.client('codepipeline')
pipelinename = raw_input("Enter the name for codepipeline: ")
codecommit = raw_input("Enter the repo name for the codecommit: ")
def CP():
    arn = CPRole()
    CDAppName, CDDepGroup = CD()
    
    pipeline = client.create_pipeline(
        pipeline={
            'name' : pipelinename,
            'roleArn' : arn,
            'artifactStore' : {
                'type': 'S3',
                'location': 'sindhu-codeapp'
             },   
            'stages': [
                {
                    'name': 'Source',
                
                    'actions':[{
                        'name': 'source',
                        'actionTypeId':{
                            'category': 'Source',
                            'owner': 'AWS',
                            'provider': 'CodeCommit',
                            'version': '1'
                        },
                        'runOrder': 123,
                        'configuration':{
                            'RepositoryName': 'IdeaTool',
                            'BranchName': 'master'
                        },
                        'outputArtifacts':[
                            {
                                'name': 'codeappsource'
                            },
                        ],
                    
                    },
                ]
            },
        
            {
                    'name': 'Build',
                
                    'actions':[{
                        'name': 'build',
                        'actionTypeId':{
                            'category': 'Build',
                            'owner': 'AWS',
                            'provider': 'CodeBuild',
                            'version': '1'
                        },
                        'runOrder': 123,
                        'configuration':{
                            'ProjectName':  'IdeaBuildProject'
                        
                        },
                        'inputArtifacts': [
                                  {
                                      'name': 'codeappsource'
                                  },
                              ],
                        'outputArtifacts':[
                            {
                                'name': 'codeappbuild'
                            },
                        ],
                    
                    },
                ]
            },
        
            {
                    'name': 'Deploy',
                    'actions':[{
                        'name': 'deploy',
                        'actionTypeId':{
                            'category': 'Deploy',
                            'owner': 'AWS',
                            'provider': 'CodeDeploy',
                            'version': '1'
                        },
                        'runOrder': 123,
                        'configuration':{
                            'ApplicationName' : CDAppName,
                            'DeploymentGroupName': CDDepGroup
                        },
                        'inputArtifacts': [
                                  {
                                      'name': 'codeappbuild'
                                  },
                              ],   
                    },
                    ]
            },
            ],
            'version': 123
        }
        
        )
