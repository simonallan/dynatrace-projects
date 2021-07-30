from aws_cdk.aws_ec2 import SubnetConfiguration, SubnetType, Vpc

from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elbv2_targets,
    aws_iam as iam,
    core as cdk
)


class TransitVpcStack(cdk.Stack):

    transitvpc = ()

    def __init__(self, scope: cdk.Construct, construct_id: str, target_vpc: Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        servicename = "dynatrace"

        allowed_principles = iam.ArnPrincipal("arn:aws:iam::701500798470:root")

        transit_vpc_cidr = "172.30.192.0/24"

        peered_vpc = {
            "peer_region": target_vpc.env.region,
            "peer_owner_id": target_vpc.env.account,
            "peer_vpc_id": target_vpc.vpc_id,
            "peer_vpc_cidr": target_vpc.vpc_cidr_block
        }

        # Default tags for all stack objects
        cdk.Tags.of(self).add("product", servicename + "-transit")
        cdk.Tags.of(self).add("Environment", "dev")
        cdk.Tags.of(self).add("Support-Level", "verylow")
        cdk.Tags.of(self).add("Cost-Centre", "cc-abc000")
        cdk.Tags.of(self).add("Sub-Project-Code", "AWS-421")
        cdk.Tags.of(self).add("Name", "dynatrace-transit")
        cdk.Tags.of(self).add("delete_date", "2021-07-01")

        # Create Transit VPC
        self.transitvpc = ec2.Vpc(self, servicename + "-transit-vpc",
                                  cidr=transit_vpc_cidr,
                                  max_azs=3,  # must match the Consumer VPC's AZ layout
                                  subnet_configuration=[
                                      SubnetConfiguration(
                                          name="Isolated",
                                          subnet_type=SubnetType.ISOLATED,
                                          cidr_mask=27
                                      )
                                  ],
                                  )

        # Peering connection
        # Depends-on: "transitvpc"
        peer = ec2.CfnVPCPeeringConnection(self, servicename + "-transit-peering",
                                           peer_region=peered_vpc["peer_region"],
                                           peer_owner_id=peered_vpc["peer_owner_id"],
                                           peer_vpc_id=peered_vpc["peer_vpc_id"],
                                           vpc_id=self.transitvpc.vpc_id
                                           )

        # After peering, add routes to isolated subnets
        for i, isolated_subnet in enumerate(self.transitvpc.isolated_subnets):
            ec2.CfnRoute(self, "peer-route-" + str(i+1),
                         route_table_id=isolated_subnet.route_table.route_table_id,
                         destination_cidr_block=peered_vpc["peer_vpc_cidr"],
                         vpc_peering_connection_id=peer.ref
                         )

        # Create Network Load Balancer
        lb = elbv2.NetworkLoadBalancer(self, "lb",
                                       vpc=self.transitvpc,
                                       cross_zone_enabled=True
                                       )

        lb.node.add_dependency = peer

        # # Build target group
        target1 = elbv2_targets.IpTarget(
            ip_address="10.1.6.27",  # prod-dyna01_sg-public-a | "i-0245516a0e64965ba"
            availability_zone="eu-west-2a"
        )

        target2 = elbv2_targets.IpTarget(
            ip_address="10.1.6.75",  # prod-dyna01_sg-public-b | "i-08a66ba1f1fc2c47b"
            availability_zone="eu-west-2b"
        )

        # ActiveGate traffic
        activegate_listener = lb.add_listener("activegate-listener", port=443
                                              )

        activegate_listener.add_targets("activegate-target",
                                        targets=[target1, target2],
                                        port=443
                                        )

        # OneAgent traffic
        oneagent_listener = lb.add_listener("oneagent-listener", port=9999
                                            )

        oneagent_listener.add_targets("oneagent-target",
                                      targets=[target1, target2],
                                      port=9999
                                      )

        # Create an Endpoint Service to connect to
        private_service = ec2.VpcEndpointService(self, servicename + "-service",
                                                 vpc_endpoint_service_load_balancers=[
                                                     lb],
                                                 vpc_endpoint_service_name=servicename + "-service",
                                                 allowed_principals=[
                                                     allowed_principles],
                                                 )

        # Outputs:

        outputs = cdk.CfnOutput(self, "transit-vpc-id",
                                description=servicename + " transit VPC ID",
                                value=self.transitvpc.vpc_id
                                )

        outputs = cdk.CfnOutput(self, "target-vpc-id",
                                description="target VPC ID",
                                value=target_vpc.vpc_id
                                )

        outputs = cdk.CfnOutput(self, "target-vpc-region",
                                description="target VPC region",
                                value=target_vpc.env.region
                                )

        outputs = cdk.CfnOutput(self, "target-vpc-cidr",
                                description="target VPC CIDR block",
                                value=target_vpc.vpc_cidr_block
                                )

        outputs = cdk.CfnOutput(self, "service-endpoint-name",
                                description=servicename + " private service name",
                                value=private_service.vpc_endpoint_service_name
                                )

        outputs = cdk.CfnOutput(self, "service-endpoint-ID",
                                description=servicename + " private service ID",
                                value=private_service.vpc_endpoint_service_id
                                )

        # ToDo:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Configure routes for peered VPC
        # - perhaps this should not be automated?
        # Paramaterise in line with CDKPipeLine stages
        # Create Pipeline
        # - https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.pipelines/README.html
        # Better names for objects created
        # Dynamic Target Groups and Listeners
