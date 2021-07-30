from aws_cdk.aws_ec2 import CfnVPCPeeringConnection, Instance, RouterType, Subnet, SubnetConfiguration, SubnetType, Vpc

from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elbv2_targets,
    core as cdk
)



class TargetVpcStack(cdk.Stack):

    targetvpc = ()

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        target_vpc_id   = "vpc-17f02973"

        cdk.Tags.of(self).add("product", "dynatrace-transit")
        cdk.Tags.of(self).add("Environment", "dev")
        cdk.Tags.of(self).add("Support-Level", "verylow")
        cdk.Tags.of(self).add("Cost-Centre", "cc-abc000")
        cdk.Tags.of(self).add("Sub-Project-Code", "AWS-421")
        cdk.Tags.of(self).add("Name", "dynatrace-target")
        cdk.Tags.of(self).add("delete_date", "2021-07-01")

        # Returns target VPC data dynamically
        self.vpc_id = Vpc.from_lookup(self, "target", vpc_id=target_vpc_id)
