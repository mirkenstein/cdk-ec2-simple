from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as ec2
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkEc2SimpleStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #Get Default VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC",
                                  # This imports the default VPC but you can also
                                  # specify a 'vpcName' or 'tags'.
                                  is_default=True
                                  )
        my_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                              vpc=vpc,
                                              description="Allow ssh access to ec2 instances",
                                              allow_all_outbound=True
                                              )
        my_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")

        #Launch EC2
        my_ec2=ec2.Instance(self, "my_ec2",
                            vpc=vpc,
                            machine_image=ec2.MachineImage.latest_amazon_linux(),
                            instance_type=ec2.InstanceType("t2.micro"),
                            security_group=my_security_group,
        )
