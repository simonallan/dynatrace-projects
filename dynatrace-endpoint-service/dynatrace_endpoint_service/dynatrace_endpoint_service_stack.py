from os import name
from aws_cdk import (
    aws_ec2 as ec2,
    core as cdk
)


class DynatraceEndpointServiceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cdk.Tags.of(self).add('Product', 'dynatrace-endpoint')
        cdk.Tags.of(self).add('Environment', 'integration')
        cdk.Tags.of(self).add('Support-Level', 'verylow')
        cdk.Tags.of(self).add('Cost-Centre', 'cc-abc000')
        cdk.Tags.of(self).add('Sub-Project-Code', 'spc-xyz000')
        cdk.Tags.of(self).add('Name', 'dynatrace-endpoint')

        # Endpoint Service name created by the Transit-VPC stack
        endpoint_service_name = "com.amazonaws.vpce.eu-west-2.vpce-svc-025328360521f0768"

        # Name of internal service
        service_name = "dynatrace"

        vpc = ec2.Vpc.from_lookup(self, 'VPC', vpc_id=vpc_id)

        provider_endpoint_sg = ec2.SecurityGroup(self, service_name + "-service-sg",
                                                 description="allows oneagent traffic",
                                                 vpc=vpc,
                                                 )

        # Allow traffic from shared VPC
        provider_endpoint_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4("172.20.0.0/18"),
            connection=ec2.Port.tcp(9999),
            description="allow oneagent traffic"
        )

        # Create Service Endpoint
        provider_endpoint = ec2.InterfaceVpcEndpoint(self, service_name + "-endpoint",
                                                     vpc=vpc,
                                                     service=ec2.InterfaceVpcEndpointService(
                                                         endpoint_service_name),
                                                     private_dns_enabled=False,
                                                     security_groups=[
                                                         provider_endpoint_sg],
                                                     subnets=ec2.SubnetType.PUBLIC
                                                     )

        # Create unique name for endpoint
        unique_name = service_name + "-endpoint-" + provider_endpoint.vpc_endpoint_id
        cdk.Tags.of(provider_endpoint).add("Name", unique_name)

        outputs = cdk.CfnOutput(self, service_name + "-endpoint-unique-name",
                                description= "Endpoint unique name",
                                value=unique_name
        )

        outputs = cdk.CfnOutput(self, service_name + "-endpoint-id",
                                description= "Endpoint ID",
                                value=provider_endpoint.vpc_endpoint_id
        )

        # Task List:
        # Output DNS service URL
