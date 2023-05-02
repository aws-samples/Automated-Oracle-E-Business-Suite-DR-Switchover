import aws_cdk as cdk

from aws_cdk import (
    Stack,
    aws_iam as iam
)
from constructs import Construct

class IamResStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM ROLE
        newrole = iam.Role(self, "ATSCUSTOMLAMBDAROLE", role_name="ATSCUSTOMLAMBDAROLE",assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))

        # Attach Managed Policies and New Policy to Role
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess"))
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaExecute"))
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaRole"))
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonSSMAutomationRole"))
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
