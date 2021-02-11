import boto3
import time
from pprint import pprint

def lambda_handler(event, context):
    
    #boto3 client
    client = boto3.client('ec2')
    ssm = boto3.client('ssm')
    
    #getting isntance information
    describeInstance = client.describe_instances()
    
    InstanceId = []
    
    #fetch instance id of the running instance
    for instances in describeInstance['Reservations']:
        for instance in instances['Instances']:
            if instance['State']['Name'] == 'running':
                InstanceId.append(instance['InstanceId'])
    
    print(InstanceId)
    
    for instanceid in InstanceId:
        response = ssm.send_command(
            InstanceIds = [instanceid],
            DocumentName = 'AWS-RunShellScript',
            Parameters = {'commands':['cd /home/ec2-user/environment; ./run.sh']},)
    
        command_id = response['Command']['CommandId']
        time.sleep(3)
        
        output = ssm.get_command_invocation(
            CommandId = command_id,
            InstanceId = instanceid
        )
    
        pprint(output)
    
    return 
