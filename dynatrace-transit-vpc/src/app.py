#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from dynatrace_transit_vpc.transit_vpc_stack import TransitVpcStack
from dynatrace_transit_vpc.target_vpc_stack import TargetVpcStack


app = cdk.App()

ireland = TargetVpcStack(app, "TargetVpcStack",
                         env=cdk.Environment(
                             account='614844069056', region="eu-west-1"),
                         )

london = TransitVpcStack(app, "TransitVpcStack",
                         target_vpc=ireland.vpc_id,
                         env=cdk.Environment(
                             account='614844069056', region="eu-west-2"),
                         )

app.synth()
