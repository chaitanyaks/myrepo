

"""#!/usr/bin/env python3

import os,sys,time

os.system("sudo apt-get -y update")

os.system("sudo apt-get install -y ruby2.3")
time.sleep(20)
os.system("sudo apt-get install -y awscli")
time.sleep(20)
os.chdir("/home/ubuntu")
time.sleep(20)
os.system("sudo aws s3 cp s3://aws-codedeploy-us-west-2/latest/install . --region us-west-2")
time.sleep(20)
os.system("sudo chmod +x ./install")
time.sleep(20)
os.system("sudo ./install auto")"""




'''#!/bin/bash
sudo apt-get -y update
sudo apt-get install -y ruby2.0
sudo apt-get install -y awscli
cd /home/ubuntu
sudo aws s3 cp s3://aws-codedeploy-us-west-2/latest/install . --region us-west-2
sudo chmod +x ./install
sudo ./install auto'''
