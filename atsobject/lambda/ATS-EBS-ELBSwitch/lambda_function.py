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
    #src_db="awsqcdb"
    #tgt_db="awsdcdb"
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
                            Names=['R12-'+tgt_db+'-Nodetab'],
                            WithDecryption=True
                            ).get("Parameters")
    
    value=response_ssm[0]["Value"]
    
    app_servers=[]
    app_server=[]
    
    for i in value.split('\n'):
        #print(i)
        if (i.split(':'))[1] != prm_db:
           new_prm_db=i.split(':')[1]
           app_servers.append(i.split(':')[3])
              
    app_server=[*set(app_servers)]
    
    reservations = ec2_client.describe_instances(Filters=[
          {
            "Name": "instance-state-name",
            "Values": ["running"],
            "Name": "tag:Name",
            "Values": [app_server[0]]
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
               "commands": ["runuser -l  applmgr -c 'cd auto_switch; sh atsappctl -target_inst "+tgt_db+" -primary_db "+new_prm_db+" -action ELBSWITCH'"]
            },  # Command to Switchover DB Service
        ) 
        
        # fetching command id for the output
        command_id = response["Command"]["CommandId"]
        
        time.sleep(10)
        
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
           raise Exception ("Issue in Switching ELB Configuration")

        # fetching command output
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
        print(output)
        cmd_status = output["StandardOutputContent"]
        print(cmd_status)
        
        last_char=cmd_status[-1]
        print(last_char)
        if last_char != "0" and last_char != "00":
           raise Exception ("Issue in Switching ELB Configuration")
            
        return {
                 'StatusCode': statusCode
               }

  except Exception as e:
    statusCode=201
    print('***Error - Failed to run ssm send command to switch ELB configration.')
    print(type(e), ':', e)
    return {
              'StatusCode': statusCode
           }
    
