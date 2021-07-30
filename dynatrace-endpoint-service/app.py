#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from dynatrace_endpoint_service.dynatrace_endpoint_service_stack import DynatraceEndpointServiceStack


app = cdk.App()
DynatraceEndpointServiceStack(app, "DynatraceEndpointServiceStack",
                                vpc_id='vpc-0ed78d1d0d9b9015e',
                                env=cdk.Environment(
                                    account="701500798470", region="eu-west-2"),
                                ) # LZ Network account, shared-dev-vpc

app.synth()
