from aws_cdk import (
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_iam as iam,
    core as cdk
)

# Nice!!
#
# from aws_cdk.aws_iam import (
#     Role,
#     ServicePrincipal,
#     ManagedPolicy
# )

# vpc_id = 'vpc-0a159c5653aea49f1'  # quickstart-vpc
keypair = 'dynatrace-activegate'
linux_ami = ec2.GenericLinuxImage({
    'eu-west-2': 'ami-00f7450c16148a7f2',
    'eu-west-3': 'ami-07bed4309217a9aab',
})  # AMI: CIS hardened Ubuntu Linux 20.04 LTS

with open("./dynatrace_activegate/user_data.sh") as f:
    user_data = f.read()


class DynatraceActivegateStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cdk.Tags.of(self).add('product', 'dynatrace-activegate')
        cdk.Tags.of(self).add('Environment', 'integration')
        cdk.Tags.of(self).add('Support-Level', 'verylow')
        cdk.Tags.of(self).add('Cost-Centre', 'cc-abc000')
        cdk.Tags.of(self).add('Sub-Project-Code', 'spc-xyz000')
        cdk.Tags.of(self).add('Name', 'dynatrace-activegate')

        vpc = ec2.Vpc.from_lookup(self, 'VPC', vpc_id=vpc_id)

        sg_activegate = ec2.SecurityGroup(self, 'sg_activegate',
                                          vpc=vpc,
                                          security_group_name='sg_activegate',
                                          description='Activegate SG attached to autoScaling group'
                                          )

        sg_activegate.add_ingress_rule(description='Allow Activegate traffic from dynatrace-transit-vpc',
                                       peer=ec2.Peer.ipv4('172.30.0.0/24'),
                                       connection=ec2.Port.tcp(443)
                                       ),
        sg_activegate.add_ingress_rule(description='Allow OneAgent traffic from dynatrace-transit-vpc',
                                       peer=ec2.Peer.ipv4('172.30.0.0/24'),
                                       connection=ec2.Port.tcp(9999)
                                       ),

        iam_activegate = iam.Role(self, 'iam_activegate',
                                  assumed_by=iam.ServicePrincipal(
                                      "ec2.amazonaws.com")
                                  )

        iam_activegate.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))

        asg_activegate = autoscaling.AutoScalingGroup(self, 'asg_activegate',
                                                      vpc=vpc,
                                                      vpc_subnets=ec2.SubnetSelection(
                                                          subnet_type=ec2.SubnetType.PUBLIC),
                                                      security_group=sg_activegate,
                                                      role=iam_activegate,
                                                      key_name=keypair,
                                                      user_data=ec2.UserData.custom(
                                                          user_data),
                                                      # desired_capacity=1, # Reset the size of your AutoScalingGroup
                                                      min_capacity=1,
                                                      max_capacity=2,
                                                      machine_image=linux_ami,
                                                      instance_type=ec2.InstanceType.of(
                                                          ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MEDIUM
                                                      ),
                                                      block_devices=[
                                                          autoscaling.BlockDevice(
                                                              device_name="/dev/sda1",
                                                              volume=autoscaling.BlockDeviceVolume.ebs(
                                                                  volume_size=24,
                                                                  delete_on_termination=True,
                                                              )
                                                          )
                                                      ],
                                                      )

        # ----------------------------------------------------------------------------------------------------------
        # TASK LIST
        # UserData - install dynatrace activegate (shared-services INT)
        # Ship logs to cloudwatch
        # Health checks
        # Test health Checks
        # ----------------------------------------------------------------------------------------------------------
        # FUTURE IDEAS
        # aws_cdk.aws_autoscaling.UpdatePolicy
        # .static replacingUpdate()	- Create a new AutoScalingGroup and switch over to it.
        # .static rollingUpdate(options?) - Replace the instances in the AutoScalingGroup one by one, or in batches.
