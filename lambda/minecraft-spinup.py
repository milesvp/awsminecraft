import json
import boto3

print('Loading function')


def lambda_handler(event, context):
    response = None
    ec2_client = boto3.client('ec2')
    print (ec2_client.describe_availability_zones()['AvailabilityZones'][0]['RegionName'])
    print (ec2_client.describe_subnets())
    for reservation in ec2_client.describe_instances()['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name' and 'minecraft-msm' == tag['Value']:
                    response = ec2_client.start_instances(InstanceIds=[instance['InstanceId']])
    print("Received event: " + json.dumps(event, indent=2))
    print(response)
    return response
