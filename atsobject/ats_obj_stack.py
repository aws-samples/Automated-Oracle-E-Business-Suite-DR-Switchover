import aws_cdk as cdk
import boto3

from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_ec2 as ec2
    # aws_sqs as sqs,
)
from constructs import Construct

class AtsObjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc_id: str, sec_grp_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Fetching AWS Account# 

        sts = boto3.client('sts')
        aws_account_id = sts.get_caller_identity().get('Account')

        # Fetching the Role created in IamResStack stack

        role_name = 'ATSCUSTOMLAMBDAROLE'

        role = iam.Role.from_role_arn(
            self,
            'ATSCUSTOMROLE',
            role_arn=f'arn:aws:iam::{self.account}:role/{role_name}'
        )

        # Get VPC from ID
        vpc = ec2.Vpc.from_lookup(self, 'Vpc', vpc_id=vpc_id)

        # read security group
        lmd_sg = ec2.SecurityGroup.from_security_group_id(self, "LambdaSecurityGroup", sec_grp_id)

        # Select Private Subnet
        privatesubnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        
        lamdbasubnet=[]
        for subnet in privatesubnets.subnets:
            lamdbasubnet.append(subnet)

        # Define Lambda Functions
        lmd_ATS_EBS_SwitchoverDb = _lambda.Function(
                                   self,'ATS-EBS-SwitchoverDb',
                                   function_name='ATS-EBS-SwitchoverDb',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-SwitchoverDb'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-SwitchoverDb' 
                                      }
                                   )


        lmd_ATS_EBS_FetchPrimaryDb = _lambda.Function(
                                   self,'ATS-EBS-FetchPrimaryDb',
                                   function_name='ATS-EBS-FetchPrimaryDb',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-FetchPrimaryDb'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-FetchPrimaryDb'
                                      }
                                   )

       
        lmd_ATS_EBS_ELBSwitch = _lambda.Function(
                                   self,'ATS-EBS-ELBSwitch',
                                   function_name='ATS-EBS-ELBSwitch',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-ELBSwitch'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-ELBSwitch'
                                      }
                                   )

        lmd_ATS_EBS_StartApplication_Status = _lambda.Function(
                                   self,'ATS-EBS-StartApplication-Status',
                                   function_name='ATS-EBS-StartApplication-Status',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-StartApplication-Status'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-StartApplication-Status'
                                      }
                                   )

        lmd_ATS_EBS_StartApplication = _lambda.Function(
                                   self,'ATS-EBS-StartApplication',
                                   function_name='ATS-EBS-StartApplication',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-StartApplication'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-StartApplication'
                                      }
                                   )

        lmd_ATS_EBS_SwitchoverDb_Status = _lambda.Function(
                                   self,'ATS-EBS-SwitchoverDb-Status',
                                   function_name='ATS-EBS-SwitchoverDb-Status',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-SwitchoverDb-Status'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-SwitchoverDb-Status'
                                      }
                                   )

        lmd_ATS_EBS_StandbyMount = _lambda.Function(
                                   self,'ATS-EBS-StandbyMount',
                                   function_name='ATS-EBS-StandbyMount',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-StandbyMount'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-StandbyMount'
                                      }
                                   )

        lmd_ATS_EBS_StopApplication = _lambda.Function(
                                   self,'ATS-EBS-StopApplication',
                                   function_name='ATS-EBS-StopApplication',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-StopApplication'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-StopApplication'
                                      }
                                   )

        lmd_ATS_EBS_StopApplication_Status = _lambda.Function(
                                   self,'ATS-EBS-StopApplication-Status',
                                   function_name='ATS-EBS-StopApplication-Status',
                                   code=_lambda.Code.from_asset('./atsobject/lambda/ATS-EBS-StopApplication-Status'),
                                   handler="lambda_function.lambda_handler",
                                   runtime=_lambda.Runtime.PYTHON_3_8,
                                   role=role,
                                   timeout=cdk.Duration.seconds(63),
                                   memory_size=128,
                                   vpc=vpc,
                                   vpc_subnets=ec2.SubnetSelection(subnets=lamdbasubnet),
                                   security_groups=[lmd_sg],
                                   environment={
                                         'NAME':'ATS-EBS-StopApplication-Status'
                                      }
                                   )

       # Create Policy and Role For Step Function 
     
        # Define the policy statement
        statement01 = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["lambda:InvokeFunction"],
            resources=[
                        lmd_ATS_EBS_FetchPrimaryDb.function_arn,
                        lmd_ATS_EBS_StopApplication.function_arn,
                        lmd_ATS_EBS_StopApplication_Status.function_arn,
                        lmd_ATS_EBS_SwitchoverDb.function_arn,
                        lmd_ATS_EBS_SwitchoverDb_Status.function_arn,
                        lmd_ATS_EBS_StandbyMount.function_arn,
                        lmd_ATS_EBS_StartApplication.function_arn,
                        lmd_ATS_EBS_StartApplication_Status.function_arn,
                        lmd_ATS_EBS_ELBSwitch.function_arn+":*",
                        lmd_ATS_EBS_FetchPrimaryDb.function_arn+":*",
                        lmd_ATS_EBS_StopApplication.function_arn+":*",
                        lmd_ATS_EBS_StopApplication_Status.function_arn+":*",
                        lmd_ATS_EBS_SwitchoverDb.function_arn+":*",
                        lmd_ATS_EBS_SwitchoverDb_Status.function_arn+":*",
                        lmd_ATS_EBS_StandbyMount.function_arn+":*",
                        lmd_ATS_EBS_StartApplication.function_arn+":*",
                        lmd_ATS_EBS_StartApplication_Status.function_arn+":*",
                        lmd_ATS_EBS_ELBSwitch.function_arn+":*"
                     ]
                  )

        statement02 = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["states:ListStateMachines","states:ListActivities","states:DescribeStateMachine","states:DescribeStateMachineForExecution","states:ListExecutions",
                     "states:DescribeExecution","states:GetExecutionHistory","states:DescribeActivity","states:StartExecution","states:StopExecution","states:StartSyncExecution",
                     "states:GetActivityTask"],
            resources=[ "arn:aws:states:*:" + aws_account_id + ":stateMachine:EBIZ-SwitchOver" ]
                  )

        # Create the policy
        steppolicy = iam.Policy(
            self,
            "ATS-CUSTOMSTEPFUNCTIONPOLICY",
            policy_name="ATS-CUSTOMSTEPFUNCTIONPOLICY",
            statements=[statement01,statement02],
        ) 

        # Create IAM ROLE
        steprole = iam.Role(self, "ATSCUSTOMSTEPFUNCTIONROLE", role_name="ATSCUSTOMSTEPFUNCTIONROLE",assumed_by=iam.ServicePrincipal("states.amazonaws.com"))

        # Assign policy to role
        steprole.attach_inline_policy(steppolicy)
        

       # Define Step Function Tasks and Steps
        tsk_ATS_EBS_FetchPrimaryDB =  tasks.LambdaInvoke(
                                    self,'Fetch Primary DB',
                                    lambda_function=lmd_ATS_EBS_FetchPrimaryDb,
                                    input_path="$",
                                    result_selector={
                                                "StatusCode.$": "$.Payload.StatusCode",
                                                "PrimaryDB.$": "$.Payload.PrimaryDB"
                                                     },
                                    result_path="$.PrimaryInfo"
                                    )

        chc_FetchPrimaryDB = sfn.Choice(
                             self,'Validate Fetch Primary DB',
                             input_path="$",
                             output_path="$"
                             )

        fail_FetchPrimaryDB = sfn.Fail(
                              self, 'Fail - Failed to Fetch Primary DB Details',
                              error="FetchPrimaryDB LambdaError",
                              cause="Failed to Fetch Primary Database using ATS-EBS-SwitchoverDb Lambda Function"
                              )

        tsk_ATS_EBS_StopApplication =  tasks.LambdaInvoke(
                                    self,'Stop Primary Application',
                                    lambda_function=lmd_ATS_EBS_StopApplication,
                                    input_path="$",
                                    result_selector={
        					"StatusCode.$": "$.Payload.StatusCode",
        					"CommandId.$": "$.Payload.CommandId",
        					"InstanceId.$": "$.Payload.InstanceId"
                                                    },
                                    result_path="$.StopApps"
                                    )

        chc_StopPrmApplication = sfn.Choice(
                             self,'Validate Stop Primary Application Command',
                             input_path="$",
                             output_path="$"
                             )

        tsk_ATS_EBS_StopApplication_Status =  tasks.LambdaInvoke(
                                    self,'Stop Application Progress Check',
                                    lambda_function=lmd_ATS_EBS_StopApplication_Status,
                                    input_path="$",
                                    result_selector={
       					  "StatusCode.$": "$.Payload.StatusCode",
                                          "Status.$": "$.Payload.Status"
                                                    },
                                    result_path="$.StopAppsStatus"
                                    )

        chc_StopApplication_Status = sfn.Choice(
                             self,'Validate Stop Application Progress',
                             input_path="$",
                             output_path="$"
                             )
       
        chc_StopApplication_Progress = sfn.Choice(
                             self,'Stop Application Progress',
                             input_path="$",
                             output_path="$"
                             )
        
        fail_StopPrmApplication = sfn.Fail(
                              self, 'Fail - Failed to Stop Primary Application Services',
                              error="StopApplication LambdaError",
                              cause="Failed to Stop Primary Application Services using ATS-EBS-StopApplication Lambda Function"
                              )

        tsk_ATS_EBS_SwitchoverDb =  tasks.LambdaInvoke(
                                    self,'Switchover Database',
                                    lambda_function=lmd_ATS_EBS_SwitchoverDb,
                                    input_path="$",
                                    result_selector={
       							"StatusCode.$": "$.Payload.StatusCode",
        						"CommandId.$": "$.Payload.CommandId",
        						"InstanceId.$": "$.Payload.InstanceId"
                                                    },
                                    result_path="$.SwitchoverDB"
                                    )

        chc_ATS_EBS_SwitchoverDb = sfn.Choice(
                             self,'Validate Switchover Command',
                             input_path="$",
                             output_path="$"
                             )

        tsk_ATS_EBS_SwitchoverDb_Status =  tasks.LambdaInvoke(
                                    self,'Switchover Progress Check',
                                    lambda_function=lmd_ATS_EBS_SwitchoverDb_Status,
                                    input_path="$",
                                    result_selector={
       							"StatusCode.$": "$.Payload.StatusCode",
        						"Status.$": "$.Payload.Status"
                                                    },
                                    result_path="$.SwitchoverDBStatus"
                                    )

        chc_ATS_EBS_SwitchoverDb_Status = sfn.Choice(
                             self,'Validate Switchover Progress Check',
                             input_path="$",
                             output_path="$"
                             )

        chc_ATS_EBS_SwitchoverDb_Progress = sfn.Choice(
                             self,'Validate Switchover Progress',
                             input_path="$",
                             output_path="$"
                             )

        fail_ATS_EBS_SwitchoverDb = sfn.Fail(
                              self, 'Fail - Failed to Switchover Database',
                              error="Switchover Database Lambda Error",
                              cause="Failed to Switchover Database using ATS_EBS_SwitchoverDb Lambda Function"
                              )

        tsk_ATS_EBS_StandbyMount =  tasks.LambdaInvoke(
                                    self,'Mount Standby Database',
                                    lambda_function=lmd_ATS_EBS_StandbyMount,
                                    input_path="$",
                                    result_selector={
                                                        "StatusCode.$": "$.Payload.StatusCode"
                                                    },
                                    result_path="$.MountStandby"
                                    )

        chc_ATS_EBS_StandbyMount = sfn.Choice(
                             self,'Validate Mount Standby',
                             input_path="$",
                             output_path="$"
                             )

        fail_ATS_EBS_StandbyMount = sfn.Fail(
                              self, 'Fail - Failed to Mount Standby Database',
                              error="Mount Standby Lambda Error",
                              cause="Failed to Mount Standby Database using ATS_EBS_StandbyMount Lambda Function"
                              )


        tsk_ATS_EBS_StartApplication =  tasks.LambdaInvoke(
                                    self,'Start Primary Application',
                                    lambda_function=lmd_ATS_EBS_StartApplication,
                                    input_path="$",
                                    result_selector={
                                                        "StatusCode.$": "$.Payload.StatusCode",
                                                        "CommandId.$": "$.Payload.CommandId",
                                                        "InstanceId.$": "$.Payload.InstanceId"
                                                    },
                                    result_path="$.StartApps"
                                    )

        chc_ATS_EBS_StartApplication = sfn.Choice(
                             self,'Validate Start Application Command',
                             input_path="$",
                             output_path="$"
                             )

        tsk_ATS_EBS_StartApplication_Status =  tasks.LambdaInvoke(
                                    self,'Start Application Status',
                                    lambda_function=lmd_ATS_EBS_StartApplication_Status,
                                    input_path="$",
                                    result_selector={
                                                        "StatusCode.$": "$.Payload.StatusCode",
                                                        "Status.$": "$.Payload.Status"
                                                    },
                                    result_path="$.StartAppsStatus"
                                    )

        chc_ATS_EBS_StartApplication_Status = sfn.Choice(
                             self,'Validate Start Application Progress',
                             input_path="$",
                             output_path="$"
                             )

        chc_ATS_EBS_StartApplication_Progress = sfn.Choice(
                             self,'Start Application Progress Check',
                             input_path="$",
                             output_path="$"
                             )

        fail_ATS_EBS_StartApplication = sfn.Fail(
                              self, 'Fail - Failed to Start Application Services',
                              error="Start Application Services Lambda Error",
                              cause="Failed to Start Application using ATS_EBS_StartApplication Lambda Function"
                              )

        tsk_ATS_EBS_ELBSwitch =  tasks.LambdaInvoke(
                                    self,'ELB Switch',
                                    lambda_function=lmd_ATS_EBS_ELBSwitch,
                                    input_path="$",
                                    result_selector={
                                                        "StatusCode.$": "$.Payload.StatusCode"
                                                    },
                                    result_path="$.ELBSwitch"
                                    )

        chc_ATS_EBS_ELBSwitch = sfn.Choice(
                             self,'Validate ELB Switch',
                             input_path="$",
                             output_path="$"
                             )

        fail_ATS_EBS_ELBSwitch = sfn.Fail(
                              self, 'Fail - Failed to Switchover ELB Configuration',
                              error="ELB Switch Lambda Error",
                              cause="Failed to ELB Switch using ATS_EBS_ELBSwitch Lambda Function"
                              )

        success = sfn.Succeed(
                         self, "Success !"
                         )

        # Define Step Function Workflow
        definition = (
                      tsk_ATS_EBS_FetchPrimaryDB
                      .next(chc_FetchPrimaryDB
                        .when(
                              sfn.Condition.number_greater_than("$.PrimaryInfo.StatusCode",200),
                              fail_FetchPrimaryDB
                            )
                        .otherwise(
                              tsk_ATS_EBS_StopApplication
                              .next(chc_StopPrmApplication
                                .when(
                                    sfn.Condition.number_greater_than("$.StopApps.StatusCode",200),
                                    fail_StopPrmApplication
                                    )
                                .otherwise(
                                         tsk_ATS_EBS_StopApplication_Status
                                         .next(chc_StopApplication_Status
                                           .when(
                                                  sfn.Condition.number_greater_than("$.StopAppsStatus.StatusCode",200),
                                                  fail_StopPrmApplication
                                                )
                                           .otherwise(
                                                      chc_StopApplication_Progress
                                                        .when(
                                                                 sfn.Condition.string_equals("$.StopAppsStatus.Status","Completed"),
                                                                 tsk_ATS_EBS_SwitchoverDb
                                                                 .next(chc_ATS_EBS_SwitchoverDb
                                                                   .when(
                                                                         sfn.Condition.number_greater_than("$.SwitchoverDB.StatusCode",200), 
									 fail_ATS_EBS_SwitchoverDb
									)
                                                                   .otherwise(
                                                                         tsk_ATS_EBS_SwitchoverDb_Status
                                                                         .next(chc_ATS_EBS_SwitchoverDb_Status
                                                                           .when(
                                                                                  sfn.Condition.number_greater_than("$.SwitchoverDBStatus.StatusCode",200),
                                                                                  fail_ATS_EBS_SwitchoverDb  
                                                                                )
                                                                            .otherwise(
                                                                                     chc_ATS_EBS_SwitchoverDb_Progress 
                                                                                     .when(
                                                                                            sfn.Condition.string_equals("$.SwitchoverDBStatus.Status","Completed"),
                                                                                            tsk_ATS_EBS_StandbyMount
                                                                                            .next(chc_ATS_EBS_StandbyMount
                                                                                             .when(
                                                                                                   sfn.Condition.number_greater_than("$.MountStandby.StatusCode",200),
                                                                                                   fail_ATS_EBS_StandbyMount
                                                                                                  )
                                                                                             .otherwise(
                                                                                               	         tsk_ATS_EBS_StartApplication
                                                                                                         .next(chc_ATS_EBS_StartApplication
													   .when(
                                                                                                                  sfn.Condition.number_greater_than("$.StartApps.StatusCode",200),
                                                                                                                  fail_ATS_EBS_StartApplication
                                                                                                                )
                                                                                                            .otherwise(
															tsk_ATS_EBS_StartApplication_Status
                                                                                                                        .next(chc_ATS_EBS_StartApplication_Status
															 .when(
															         sfn.Condition.number_greater_than("$.StartAppsStatus.StatusCode",200),
                                                                                                                                 fail_ATS_EBS_StartApplication
                                                                                                                              )	
                                                                                                                         .otherwise(
																      chc_ATS_EBS_StartApplication_Progress
																      .when(
																	      sfn.Condition.string_equals("$.StartAppsStatus.Status","Completed"),
																	      tsk_ATS_EBS_ELBSwitch
																	      .next(chc_ATS_EBS_ELBSwitch
                                                                                                                                              .when(     
                                                                                                                                                     sfn.Condition.number_greater_than("$.ELBSwitch.StatusCode",200),
																		     fail_ATS_EBS_ELBSwitch
                                                                                                                                                   ) 
                                                                                                                                               .otherwise(
                                                                                                                                                     success
                                                                                                                                                   )
                                                                                                                                                  )
																           )
																       .otherwise(
	   				                                                                                                            sfn.Wait(self, "Wait - Waiting To Start Application", time=sfn.WaitTime.duration(cdk.Duration.seconds(15)))
                                                                                                                                                    .next(tsk_ATS_EBS_StartApplication_Status)
																		   
																	         )
                                                                                                                                   )
                                                                                                                             )
                                                                                                                      )
                                                                                                              )		
                                                                                                       ) 
                                                                                                 )
                                                                                           )
                                                                                      .otherwise (
                                                                                                     sfn.Wait(self, "Wait - Waiting To Switchover Database", time=sfn.WaitTime.duration(cdk.Duration.seconds(15)))
                                                                                                     .next(tsk_ATS_EBS_SwitchoverDb_Status)
                                                                                                 )
                                                                                       )
									      ) 
								              )            
								        )  	
                                                               ) 
                                                        .otherwise(

                                                                      sfn.Wait(self, "Wait - Waiting To Stop Application", time=sfn.WaitTime.duration(cdk.Duration.seconds(15))) 
                                                                      .next(tsk_ATS_EBS_StopApplication_Status)
                                                                 )
                                                      )
                                         ) 
                                       )
                                   )
                                   ) 
                           )
                       )

        # Create State Machine Based On the Workflow Definition
        state_machine = sfn.StateMachine(
                       self, 'EBIZ-SwitchOver',
                       state_machine_name='EBIZ-SwitchOver',
                       definition=sfn.Chain.start(definition),
                       role=steprole
                        )
