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
    cmd_id=event["SwitchoverDB"]["CommandId"]
    inst_id=event["SwitchoverDB"]["InstanceId"]
    
    
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
    

    # fetching command output
    output = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=inst_id)
    print(output)
    
    if output["Status"] == "Pending" or output["Status"] == "InProgress":
       statusCode=200
       return {
           'StatusCode': statusCode,
           'Status':'Pending'
       }
    
    print(output["Status"])   
    if output["Status"] != "Pending":
       if output["Status"] == "Success":
          cmd_output = output["StandardOutputContent"]
          last_char=cmd_output[-1]
          print(last_char)
          if last_char != "0":
             statusCode=201
             return {
              'StatusCode':statusCode,
              'Status':'Failed'
              }
          else :
             statusCode=200
             return {
              'StatusCode': statusCode,     
              'Status':'Completed'
              }
       elif output["Status"] == "Failed":
        statusCode=201
        return {
                'StatusCode': statusCode,
                'Status':'Failed'
               }
    #cmd_status = output["StandardOutputContent"]
 
  except Exception as e:
    statusCode=201
    print('***Error - Error in Command Execution Check Log in instance auto_switch folder.')
    print(type(e), ':', e)
    return {
             'StatusCode': statusCode,
             'Status':'Failed'
           }
