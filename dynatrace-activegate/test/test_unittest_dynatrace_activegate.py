from aws_cdk import core as cdk
import unittest

from dynatrace_activegate.dynatrace_activegate_stack import DynatraceActivegateStack


class TagsTestCase(unittest.TestCase):

    # Initialise objects for testing
    @classmethod
    def setUpClass(cls):

        app = cdk.App()

        DynatraceActivegateStack(
            app,
            "Stack",
            vpc_id="vpc-0ed78d1d0d9b9015e",
            env={"account": "063411552818", "region": "eu-west-2"},
        )

        # Synthesize templates
        cls._template = app.synth().get_stack_by_name("Stack").template

        # Parse template for Resources
        cls._resources = [resource for resource in cls._template["Resources"].values()]

    @classmethod
    def tearDownClass(cls):
        cls._template
        cls._resources

    # Test all required tags have been included
    def test_for_required_tags(self):
        required_tags = [
            "Product",
            "Environment",
            "Support-Level",
            "Cost-Centre",
            "Sub-Project-Code",
            "Name",
        ]
        for r in self._resources:
            if r["Properties"].get("Tags"):
                tags = r["Properties"]["Tags"]
                for t in tags:
                    for q in required_tags:
                        if t["Key"] == q:
                            print(f'Resource {r["Type"]} has tag {t["Key"]}')
                            break
        self.assertEqual(t["Key"], q)

    # Test all tags have values
    def test_tag_values_not_empty(self):
        for r in self._resources:
            if r["Properties"].get("Tags"):
                tags = r["Properties"]["Tags"]
                for t in tags:
                    self.assertIsNot(t["Value"], "")


if __name__ == "__main__":
    unittest.main()

# _______________
# TASK LIST     |__________________________________________________________________________________
#
# TESTS TO ADD:
# assert count (resources created) == 3
# assert resources == resource type: Security Group
# assert resources == resource type: IAM Role
# assert resources == resource type: AutoScaling Group
# assert vpcid == "vpc-0ed78d1d0d9b9015e"
# assert ingress_rule peer == "172.30.0.0/24" on port 9999
# assert ingress_rule peer == "172.30.0.0/24" on port 443
# assert iam role == "iam_activegate"
# assert iam.managedPolicy == "AmazonSSMManagedInstanceCore"
# assert autoscalinggroup subnet_type == "public"
# assert autoscalinggroup security_group == "sg_activegate"
# assert autoscalinggroup role == "iam_activegate"
# assert autoscalinggroup keyname == "dynatraace_activegate"
# assert autoscalinggroup userdata == ???????
# assert autoscalinggroup min capacity == "1"
# assert autoscalinggroup max capacity == "2"
# assert autoscalinggroup machine_name == ("eu-west-2": "ami-00f7450c16148a7f2")
# assert autoscalinggroup instancetype == ("BURSTABLE2", "MEDIUM")
# assert autoscalinggroup block-device volume_size == 24
# assert autoscalinggroup block-device delete_onm_termination == "TRUE"
