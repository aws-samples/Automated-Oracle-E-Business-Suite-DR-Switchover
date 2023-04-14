#!/usr/bin/env python3
import os
import sys

import aws_cdk as cdk

from iamres.iam_res_stack import IamResStack
from atsobject.ats_obj_stack import AtsObjectStack

app = cdk.App()

vpc_id=app.node.try_get_context("vpc_id")
sec_grp_id=app.node.try_get_context("sec_grp_id")

## Calling stack IamResStack

IamResStack(app, "IamResStack",
            env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
        )

## Calling stack AtsObjectStack
AtsObjectStack(app, "AtsObjectStack", vpc_id, sec_grp_id,
                    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
              )
app.synth()
