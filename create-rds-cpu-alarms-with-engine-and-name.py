import boto3

# Pergunta ao usuário qual é o ARN do tópico SNS
sns_topic_arn = input("Informe o ARN do tópico SNS: ")

# Pergunta ao usuário qual é a região
region = input("Informe a região: ")

# Cria um cliente RDS usando a região informada
rds_client = boto3.client('rds', region_name=region)

# Lista todas as instâncias RDS
response = rds_client.describe_db_instances()

# Itera sobre as instâncias
for instance in response['DBInstances']:
    # Obtém o ID da instância
    instance_id = instance['DBInstanceIdentifier']

    # Obtém a engine do banco
    rds_engine = instance['Engine']

    # Obtém o nome da instância
    rds_name = instance_id.split('-')[0]

    # Cria o alerta de CPU com o nome composto
    alarm_name = f"RDS-{rds_engine}-{rds_name}-CPUUtilization"

    # Cria o alerta de CPU
    cloudwatch_client = boto3.client('cloudwatch', region_name=region)
    cloudwatch_client.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription=alarm_name,
        MetricName="CPUUtilization",
        Namespace="AWS/RDS",
        Statistic="Average",
        Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': rds_name}],
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        Period=300,
        Threshold=80,
        EvaluationPeriods=2,
        AlarmActions=[sns_topic_arn]
    )
