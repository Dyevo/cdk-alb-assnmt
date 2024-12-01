from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_iam as iam
)

import aws_cdk
from constructs import Construct

class ServerStack(stack):
    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Security Groups
        webserver_sg = ec2.SecurityGroup(
            self, "WebserverSG",
            vpc=vpc,
            description="Security group for web servers",
            allow_all_outbound=True
        )
        webserver_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP traffic"
        )

        webserver_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH traffic"
        )

        # Instances
        ami = ec2.MachineImage.latest_amazon_linux()

        for i in range(1, 3):
            ec2.Instance(
                self, f"WebServer{i}",
                instance_type=ec2.InstanceType("t2.micro"),
                machine_image=ami,
                vpc=vpc,
                security_group=webserver_sg,
                vpc_subnets=ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                key_name="YourKeyPair"
            )

        # Load Balancer
        lb = elbv2.ApplicationLoadBalancer(
            self, "EngineeringLB",
            vpc=vpc,
            internet_facing=True
        )

        listener = lb.add_listener(
            "Listener",
            port=80,
            open=True
        )

        listener.add_targets(
            "WebServerTarget",
            port=80,
            targets=[
                elbv2.InstanceTarget(
                    instance_id=instance.instance_id,
                    port=80
                ) for instance in ec2.Instance.all_instances(self)
            ]
        )

        core.CfnOutput(
            self, "LoadBalancerDNS",
            value=lb.load_balancer_dns_name
        )