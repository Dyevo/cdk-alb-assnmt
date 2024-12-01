import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_alb_assnmt.network_stack import CdkAlbAssnmtStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_alb_assnmt/cdk_alb_assnmt_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkAlbAssnmtStack(app, "cdk-alb-assnmt")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
