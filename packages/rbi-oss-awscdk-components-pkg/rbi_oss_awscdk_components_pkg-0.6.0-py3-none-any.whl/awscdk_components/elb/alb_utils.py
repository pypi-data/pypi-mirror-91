from aws_cdk import (
    core,
    aws_lambda,
    aws_ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elvb2_targets,
    aws_cognito,
    aws_s3
)


def register_lambda_target_group_with_cognito_auth_rule(
        scope: core.Construct,
        fn: aws_lambda.IFunction,
        vpc: aws_ec2.IVpc,
        listener: elbv2.ApplicationListener,
        user_pool: aws_cognito.CfnUserPool,
        user_pool_app_client: aws_cognito.CfnUserPoolClient,
        user_pool_domain: aws_cognito.CfnUserPoolDomain,
        path_pattern_values: [str],
        target_group_id: str = 'lambdatg',
        listener_rule_id: str = 'lambdaalblrule'
) -> None:
    """
        Registers the lambda function as target group in the ALB listener and adds authentication
        rule before access through the provided AWS cognito user pool.

        The security group of the lambda function is configured to allow connections from the ALB listener on port 443.

        The path_pattern_values provide the paths for the forwarding rule in the listener, ie. /mylambda, /mylambda/*
        target_group_id and listener_rule_id can be customized if the uniqueness of the ids in the stack is violated.
    """
    target = elvb2_targets.LambdaTarget(fn)
    target_group = elbv2.ApplicationTargetGroup(
        scope=scope,
        id=target_group_id,
        targets=[target],
        vpc=vpc,
        target_type=elbv2.TargetType.LAMBDA
    )

    # this is necessary due to a bug in the CDK - TODO: add reference to the issue
    target_group.node.default_child.node.add_dependency(fn)

    elbv2.CfnListenerRule(
        scope=scope,
        id=listener_rule_id,
        actions=[
            {
                'type': 'authenticate-cognito',
                'authenticateCognitoConfig': elbv2.CfnListenerRule.AuthenticateCognitoConfigProperty(
                    user_pool_arn=user_pool.attr_arn,
                    user_pool_client_id=user_pool_app_client.ref,
                    user_pool_domain=user_pool_domain.ref,
                    scope='openid',
                    session_timeout=3600,
                    on_unauthenticated_request='authenticate'
                ),
                'order': 10
            },
            {
                'type': 'forward',
                'order': 20,
                'targetGroupArn': target_group.target_group_arn
            }
        ],
        conditions=[
            {
                'field': 'path-pattern',
                'values': path_pattern_values
            }
        ],
        listener_arn=listener.listener_arn,
        priority=1000
    )
    fn.connections.allow_from(listener, aws_ec2.Port.tcp(443))


def register_ec2_as_alb_target(
        scope: core.Construct,
        ec2: aws_ec2.Instance,
        listener: elbv2.ApplicationListener,
        vpc: aws_ec2.IVpc,
        path_pattern_values: [str],
        port: int,
        protocol: elbv2.ApplicationProtocol = elbv2.ApplicationProtocol.HTTPS,
        listener_rule_id: str = 'ec2alblrule',
        target_group_id: str = 'ec2tg',
):
    """
        Registers a given EC2 instance as an ALB listener target.

        The security group of the EC2 is configured to allow connections from the ALB listener on the provided port.

        The path_pattern_values provide the paths for the forwarding rule in the listener, ie. /myec2, /myec2/*
        target_group_id and listener_rule_id can be customized if the uniqueness of the ids in the stack is violated.

        :param scope: the construct
        :param ec2: the EC2 instance
        :param listener: ALB listener
        :param vpc: the VPC
        :param path_pattern_values: for the forwarding rule, see above
        :param port: the port on the EC2 where the ALB can connect to
        :param protocol: defaults to elbv2.ApplicationProtocol.HTTPS
        :param listener_rule_id: see above
        :param target_group_id: see above
    """
    __register_ec2_as_alb_target_int(
        scope=scope,
        ec2=ec2,
        listener=listener,
        vpc=vpc,
        path_pattern_values=path_pattern_values,
        port=port,
        protocol=protocol,
        listener_rule_id=listener_rule_id,
        target_group_id=target_group_id
    )


def register_ec2_as_alb_target_with_authentication_rule(
        scope: core.Construct,
        ec2: aws_ec2.Instance,
        listener: elbv2.ApplicationListener,
        vpc: aws_ec2.IVpc,
        path_pattern_values: [str],
        port: int,
        user_pool: aws_cognito.CfnUserPool,
        user_pool_app_client: aws_cognito.CfnUserPoolClient,
        user_pool_domain: aws_cognito.CfnUserPoolDomain,
        protocol: elbv2.ApplicationProtocol = elbv2.ApplicationProtocol.HTTPS,
        listener_rule_id: str = 'ec2alblrule',
        target_group_id: str = 'ec2tg',
):
    """
        Registers a given EC2 instance as an ALB listener target. The access to the instance is protected by
        authentication rule for authentication with AWS Cognito

        The security group of the EC2 is configured to allow connections from the ALB listener on the provided port.

        The path_pattern_values provide the paths for the forwarding rule in the listener, ie. /myec2, /myec2/*
        target_group_id and listener_rule_id can be customized if the uniqueness of the ids in the stack is violated.
        :param scope: the construct
        :param ec2: the EC2 instance
        :param listener: ALB listener
        :param vpc: the VPC
        :param path_pattern_values: for the forwarding rule, see above
        :param port: the port on the EC2 where the ALB can connect to
        :param user_pool: see aws_cognito.CfnUserPool
        :param user_pool_app_client: see aws_cognito.CfnUserPoolClient
        :param user_pool_domain: see aws_cognito.CfnUserPoolDomain
        :param protocol: defaults to elbv2.ApplicationProtocol.HTTPS
        :param listener_rule_id: see above
        :param target_group_id: see above
    """
    __register_ec2_as_alb_target_int(
        scope=scope,
        ec2=ec2,
        listener=listener,
        vpc=vpc,
        path_pattern_values=path_pattern_values,
        port=port,
        user_pool=user_pool,
        user_pool_app_client=user_pool_app_client,
        user_pool_domain=user_pool_domain,
        protocol=protocol,
        listener_rule_id=listener_rule_id,
        target_group_id=target_group_id
    )


def __register_ec2_as_alb_target_int(
        scope: core.Construct,
        ec2: aws_ec2.Instance,
        listener: elbv2.ApplicationListener,
        vpc: aws_ec2.IVpc,
        path_pattern_values: [str],
        port: int,
        user_pool: aws_cognito.CfnUserPool = None,
        user_pool_app_client: aws_cognito.CfnUserPoolClient = None,
        user_pool_domain: aws_cognito.CfnUserPoolDomain = None,
        protocol: elbv2.ApplicationProtocol = elbv2.ApplicationProtocol.HTTPS,
        listener_rule_id: str = 'ec2alblrule',
        target_group_id: str = 'ec2tg',
):
    """
        Registers a given EC2 instance as an ALB listener target.

        The security group of the EC2 is configured to allow connections from the ALB listener on the provided port.

        The path_pattern_values provide the paths for the forwarding rule in the listener, ie. /myec2, /myec2/*
        target_group_id and listener_rule_id can be customized if the uniqueness of the ids in the stack is violated.
    """
    target = elvb2_targets.InstanceTarget(ec2)
    target_group = elbv2.ApplicationTargetGroup(
        scope=scope,
        id=target_group_id,
        vpc=vpc,
        port=port,
        targets=[target],
        target_type=elbv2.TargetType.INSTANCE,
        protocol=protocol
    )

    actions = []

    if user_pool and user_pool_app_client and user_pool_domain:
        auth_rule = {
            'type': 'authenticate-cognito',
            'authenticateCognitoConfig': elbv2.CfnListenerRule.AuthenticateCognitoConfigProperty(
                user_pool_arn=user_pool.attr_arn,
                user_pool_client_id=user_pool_app_client.ref,
                user_pool_domain=user_pool_domain.ref,
                scope='openid',
                session_timeout=3600,
                on_unauthenticated_request='authenticate'
            ),
            'order': 10
        }
        actions.append(auth_rule)

    actions.append(
        {
            'type': 'forward',
            'order': 20,
            'targetGroupArn': target_group.target_group_arn
        }
    )

    elbv2.CfnListenerRule(
        scope=scope,
        id=listener_rule_id,
        actions=actions,
        conditions=[
            {
                'field': 'path-pattern',
                'values': path_pattern_values
            }
        ],
        listener_arn=listener.listener_arn,
        priority=2000
    )
    ec2.connections.allow_from(listener, aws_ec2.Port.tcp(port))


def enable_logging(
        load_balancer: elbv2.BaseLoadBalancer,
        logging_s3_bucket: aws_s3.IBucket,
        logging_prefix: str = None
) -> None:
    """
        Enables the logs of the LB to be written to the provided S3 bucket.

        Please note that the S3 bucket must be properly configured to be able to write to it!
    """
    load_balancer.log_access_logs(
        bucket=logging_s3_bucket,
        prefix=logging_prefix
    )
