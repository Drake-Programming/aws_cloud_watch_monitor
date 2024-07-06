#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloud_watch_monitor.cloud_watch_monitor_stack import CloudWatchMonitorStack


app = cdk.App()
CloudWatchMonitorStack(app, "CloudWatchMonitorStack")

app.synth()
