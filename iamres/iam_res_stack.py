import aws_cdk as cdk

from aws_cdk import (
    Stack,
    aws_iam as iam
)
from constructs import Construct

class IamResStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Create IAM Policy
        newpolicy = iam.Policy(self, "ATS-CUSTOMLAMBDAPOLICY",
                     policy_name="ATS-CUSTOMLAMBDAPOLICY",
                     statements=[
                        iam.PolicyStatement(
                            actions=["elasticloadbalancing:DescribeSSLPolicies","ssm:SendCommand","elasticloadbalancing:ModifyListener","ec2:DescribeInstances","elasticloadbalancing:DescribeTags","ec2:CreateTags","logs:CreateLogGroup","logs:PutLogEvents","elasticloadbalancing:DescribeLoadBalancerAttributes","elasticloadbalancing:DescribeLoadBalancers","logs:CreateLogStream","elasticloadbalancing:RemoveTags","elasticloadbalancing:DescribeTargetGroupAttributes","elasticloadbalancing:DescribeListeners","ec2:DescribeAvailabilityZones","elasticloadbalancing:DescribeAccountLimits","elasticloadbalancing:AddTags","elasticloadbalancing:DescribeTargetHealth","elasticloadbalancing:DescribeTargetGroups","elasticloadbalancing:DescribeListenerCertificates","elasticloadbalancing:DescribeRules","ec2:DescribeInstanceStatus","ec2:DescribeInstances","ec2:CreateNetworkInterface","ec2:AttachNetworkInterface","ec2:DescribeNetworkInterfaces","ec2:DeleteNetworkInterface"],
                            resources=["*"])
                               ]
                           )


        # Create IAM ROLE
        newrole = iam.Role(self, "ATSCUSTOMLAMBDAROLE", role_name="ATSCUSTOMLAMBDAROLE",assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))

        # Attach Managed Policies and New Policy to Role
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess"))
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaExecute"))
        newrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaRole"))
        newrole.attach_inline_policy(newpolicy)
