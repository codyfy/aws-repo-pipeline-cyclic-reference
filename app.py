#!/usr/bin/env python3

from aws_cdk import core

from cdk_repopipe.cdk_repo_stack import RepoStack
from cdk_repopipe.cdk_pipe_stack import PipelineStack


app = core.App()
repo_stack = RepoStack(app, "cdk-repo")
pipe_stack = PipelineStack(app, "cdk-pipe", repo_stack.repo)

app.synth()
