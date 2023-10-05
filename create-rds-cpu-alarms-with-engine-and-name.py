import boto3

# Cria um cliente RDS usando as configurações padrão do CloudShell
rds_client = boto3.client('rds')

# Lista todas as instâncias RDS
response = rds_client.describe_db_instances()

# Itera sobre as instâncias
for instance in response['DBInstances']:
    # Obtém o ID da instância
    instance_id = instance['DBInstanceIdentifier']

    # Obtém a engine do banco
    instance_rds_engine = instance['Engine']

    # Obtém o nome da instância
    instance_rds_name = instance_id.split('-')[0]

    # Configura o tópico SNS (substitua 'YOUR_SNS_TOPIC_ARN' pelo ARN real)
    alarm_actions = 'YOUR_SNS_TOPIC_ARN'

    # Cria o alerta de CPU
    cloudwatch_client = boto3.client('cloudwatch')
    cloudwatch_client.put_metric_alarm(
        AlarmName=f"RDS-{instance_rds_engine}-{instance_rds_name}-CPUUtilization",
        AlarmDescription=f"RDS-{instance_rds_engine}-{instance_rds_name}-CPUUtilization",
        MetricName="CPUUtilization",
        Namespace="AWS/RDS",
        Statistic="Average",
        Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_rds_name}],
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        Period=300,
        Threshold=80,
        EvaluationPeriods=2,
        AlarmActions=[alarm_actions]
    )
