from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkAlbAssnmtStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        #VPC
        self.vpc = ec2.Vpc(
            self, "EngineeringVpc",
            cidr="10.0.0.0/18",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ]       
        )

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkAlbAssnmtQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
