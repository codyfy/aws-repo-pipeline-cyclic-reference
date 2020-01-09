from aws_cdk import (
    core,
    aws_codecommit as codecommit,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_autoscaling as autoscaling,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codedeploy as codedeploy,
    aws_ec2 as ec2,
    aws_s3 as s3
)


class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, repo: codecommit.Repository, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #---------- CodePipeline ----------#
        artifactBucket = s3.Bucket(self, 'PipelineBucket',
            bucket_name="bucket-name")

        pipeline = codepipeline.Pipeline(self, "CodePipeline",
            artifact_bucket=s3.Bucket.from_bucket_attributes(self, 'ImportedBucket',
            bucket_name="bucket-name")
        )
        
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="Source",
            repository=repo,
            output=source_output
        )        
        pipeline.add_stage(stage_name="Source", actions=[source_action])


        #---------- Deploy ----------#
        deploy_application = codedeploy.ServerApplication(self, "CodeDeployApplication", 
            application_name="application-name"
        )

        deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
            application=deploy_application,
        )
        
        deploy_action = codepipeline_actions.CodeDeployServerDeployAction(
            action_name="deploy",
            input=source_output,
            deployment_group=deployment_group
        )
        pipeline.add_stage(stage_name="Deploy", actions=[ deploy_action ])