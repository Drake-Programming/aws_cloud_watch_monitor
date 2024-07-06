from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as sns_sub,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    Duration,
)
from constructs import Construct


class CloudWatchMonitorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        web_hook_lambda = _lambda.Function(
            self,
            "webHookLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("services"),
            handler="hook.handler",
        )

        alarm_topic = sns.Topic(
            self,
            "ValueAlarmTopic",
            display_name="ValueAlarmTopic",
            topic_name="ValueAlarmTopic",
        )

        alarm_topic.add_subscription(sns_sub.LambdaSubscription(web_hook_lambda))

        test_alarm = cloudwatch.Alarm(
            self,
            "TestApiAlarm",
            metric=cloudwatch.Metric(
                metric_name="custom-error",
                namespace="Custom",
                period=Duration.minutes(1),
                statistic="Sum",
            ),
            evaluation_periods=1,
            threshold=100,
        )

        topic_action = cloudwatch_actions.SnsAction(alarm_topic)
        test_alarm.add_alarm_action(topic_action)
        test_alarm.add_ok_action(topic_action)

        apiAlarm = cloudwatch.Alarm(
            self,
            "Api4xxAlarm",
            metric=cloudwatch.Metric(
                metric_name="4XXError",
                namespace="AWS/ApiGateway",
                period=Duration.minutes(1),
                statistic="Sum",
                dimensions_map={"ApiName": "Employee-Api"},
            ),
            evaluation_periods=1,
            threshold=1,
        )

        apiAlarm.add_alarm_action(topic_action)
        apiAlarm.add_ok_action(topic_action)
