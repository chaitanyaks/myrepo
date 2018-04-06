import boto3

ec2 = boto3.resource('ec2')


def keypair(Name):
    key=ec2.create_key_pair(KeyName= Name)
    keypair=key.name
    fp=open(keypair+'.pem','w')
    fp.writelines(key.key_material)
    fp.close()
    print key.key_material
    print keypair

    return keypair


