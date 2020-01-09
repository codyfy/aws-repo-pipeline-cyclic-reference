#!/usr/bin/env python3

from aws_cdk import core

from cdk_repopipe.cdk_repopipe_stack import CdkRepopipeStack


app = core.App()
CdkRepopipeStack(app, "cdk-repopipe")

app.synth()
