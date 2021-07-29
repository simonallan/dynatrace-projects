#!/usr/bin/env python3
import os
from aws_cdk import core as cdk

from dynatrace_activegate.dynatrace_activegate_stack import DynatraceActivegateStack


app = cdk.App()
DynatraceActivegateStack(app, 'DynatraceActivegateStack',
                         vpc_id='vpc-0ed78d1d0d9b9015e',
                         env=cdk.Environment(
                             account='063411552818', region='eu-west-2'),
                         ) # Shared Services account shared-dev-vpc

app.synth()
