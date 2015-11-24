#!/usr/bin/env python

import boto3
import requests
from sys import exit
from os import path, remove
from subprocess import call
from datetime import datetime, timedelta

TIMESTAMP_FILE = 'shutdown.timestamp'
NOW = datetime.now()

def get_instance_id():
    return requests.get('http://instance-data/latest/meta-data/instance-id').text

def shutdown_self():
    ec2 = boto3.resource('ec2')
    try:
        
        server_start_time = datetime.fromtimestamp(path.getmtime(TIMESTAMP_FILE))
        print (server_start_time)
        if ((NOW - timedelta(minutes=110)) > server_start_time):
            try:
                remove(TIMESTAMP_FILE)
            except OSError:
                pass
            ec2.instances.filter(InstanceIds=[get_instance_id(),]).stop()
    except:
        call(['touch', TIMESTAMP_FILE])


if __name__ == "__main__":
    shutdown_self()
