import boto3

s3=boto3.resource('s3')
'''for bucket in s3.buckets.all():
    print bucket.name'''
data= open('F:\Boto3\sind.txt','rb')
s3.Bucket('sindhu-codeapp').put_object(Key='sind.txt', Body=data)

