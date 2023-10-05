#!/bin/bash
# Importa as bibliotecas necessárias
# aws=$(which aws)

# Setando a região
#region=$(read -p "Informe a região: ")

# Setando topico SNS 
alarm_actions=$(read -p "Informe o ARN do topico SNS:")

# Lista todas as instâncias RDS
instances= (aws rds describe-db-instances)

# Itera sobre as instâncias
for instance in $instances; do

  # Obtém o ID da instância
  instance_id=$(echo $instance | jq -r .DBInstances[].DBInstanceIdentifier)

  # Obtém a engine do banco
  instance_rds_engine=$(echo $instance | jq -r .DBInstances[].Engine)

  # Obtém o nome da instância
  instance_rds_name=$(echo $instance | jq -r .DBInstances[].DBInstanceIdentifier | cut -d "-" -f 1)

  # Cria o alerta de CPU
  aws cloudwatch put-metric-alarm \
    --region us-east-1 \
    --alarm-name "RDS-${instance_rds_engine}-${instance_rds_name}-CPUUtilization" \
    --alarm-description "RDS-${instance_rds_engine}-${instance_rds_name}-CPUUtilization" \
    --metric-name "CPUUtilization" \
    --namespace "AWS/RDS" \
    --statistic "Average" \
    --dimensions Name=DBInstanceIdentifier,Value=${instance_rds_name} \
    --comparison-operator "GreaterThanOrEqualToThreshold" \
    --period 300 \
    --threshold 80 \
    --evaluation-periods 2 \
    --alarm-actions $alarm_actions

done
