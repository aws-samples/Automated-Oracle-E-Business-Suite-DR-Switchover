import time
import json
import boto3
import os
import datetime

statusCode=200

def lambda_handler(event, context):
  try:
    # Initialize session and client
    global statusCode
    statusCode=200
    region=event["Region"]

    tgt_db=event["Target"]
    prm_db=event["PrimaryInfo"]["PrimaryDB"]
    
    ec2_client = boto3.client(
                 "ec2",
                 region_name=region
                 )
                 
    ec2_resource = boto3.resource(
                 "ec2",
                 region_name=region
                  )
                 
    ssm = boto3.client(
                 "ssm",
                 region_name=region
                 )
    
    response_ssm = ssm.get_parameters(
                            Names=['ATS-'+tgt_db+'-Nodetab'],
                            WithDecryption=True
                            ).get("Parameters")
    
    value=response_ssm[0]["Value"]
    
    db_servers=[]
    db_server=[]
    
    for i in value.split('\n'):
        #print(i)
        if (i.split(':'))[1] != prm_db:
           db_servers.append(i.split(':')[2])

    db_server=[*set(db_servers)]
    
    reservations = ec2_client.describe_instances(Filters=[
          {
            "Name": "instance-state-name",
            "Values": ["running"],
            "Name": "tag:Name",
            "Values": [db_server[0]]
          }
        ]).get("Reservations")

   # if reservations['ResponseMetadata']['HTTPStatusCode'] == 200:
    #    statusCode=201
    #    raise Exception ("Issue in Identifying EC2 Instance")
    #print (json.dumps(reservations,indent=4,sort_keys=True,default=str))
    
    if not reservations:
       raise Exception ("Issue in Fetching EC2 Instance Check if Tagging is correct")
        
    instance_id=""   
    for reservation in reservations:
        for instance in reservation["Instances"]:
             if not instance:
                raise Exception ("Issue in Identifying EC2 Instance")
             instance_id = instance["InstanceId"]
             response = ssm.send_command(
             InstanceIds=[instance_id],
             DocumentName="AWS-RunShellScript",
             Parameters={
               "commands": ["runuser -l  rdsdb -c 'cd auto_switch; sh atsdbctl -target_db "+tgt_db+" -action SWITCHOVER_DB'"]
            },  # Command to Start APP Service
        ) 
        
        # fetching command id for the output
        command_id = response["Command"]["CommandId"]
        
        time.sleep(5)
        
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
           raise Exception ("Issue in Switching Over Database")

        return {
                 'StatusCode': statusCode,
                 'CommandId' : command_id,
                 'InstanceId': instance_id
               }

  except Exception as e:
    statusCode=201
    print('***Error - Failed to run ssm send command to switchover database.')
    print(type(e), ':', e)
    return {
              'StatusCode': statusCode,
              'CommandId' : "NULL",
              'InstanceId': "NULL" 
           }
