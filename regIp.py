#!/usr/bin/env python
### BEGIN INIT INFO
# Provides:       regIP
# Required-Start: $local_fs $network
# Required-Stop:  $local_fs $network
# Should-Start:   
# Should-Stop:    
# Default-Start:  2 3 4 5
# Default-Stop:   0 1 6
# Short-Description: regIP: registers public IP with route53
# Description: regIP: registers public IP with route53
### END INIT INFO

import boto3
import requests
from sys import exit

def get_public_ip():
    return requests.get('http://instance-data/latest/meta-data/public-ipv4').text

def get_instance_id():
    return requests.get('http://instance-data/latest/meta-data/instance-id').text

def get_env(instance_id):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    role = ''
    for tag in instance.tags:
      if 'role' == tag['Key']:
        role = tag['Value']
    if not role:
      exit(0)
    if role == 'prod':
      return ''
    return '-' + role
    

def register_ip(ip):
    r53_client = boto3.client('route53')
    zone = r53_client.list_hosted_zones_by_name(DNSName='awscnames.net')['HostedZones'][0]
    ec2_client = boto3.client('ec2')
    env = get_env(get_instance_id())
    response = r53_client.change_resource_record_sets(
        HostedZoneId=zone['Id'],
        ChangeBatch={
            'Changes': [ {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'minecraft{}.awscnames.net.'.format(env),
                    'Type': 'A',
                    'TTL': 10,
                    'ResourceRecords': [{
                        'Value': ip
                    }, ],
                }
            }, ]
        }
    )

if __name__ == "__main__":
    register_ip(get_public_ip())
