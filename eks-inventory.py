#!/usr/bin/env python3
import boto3
import csv
from botocore.exceptions import ClientError
import json
import time

timestr = time.strftime("%Y%m%d-%H%M%S")
regions = ['us-east-2','us-east-1']
for region in regions:  
    client = boto3.client("eks", region_name=region)
response = client.list_clusters()
clusterid = response.get("clusters")
header = ["AccountId","ClusterName", "InstanceID", "InstanceTypes", "Region"]
with open(f"eks-node-{timestr}.csv", "w", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for cluster in clusterid:
        ClusterName = cluster

        client = boto3.client('sts')
        response = client.get_caller_identity()
        AccountId= response.get('Account')
        for Accounts in AccountId:
            Account = Accounts

    # print(json_dump)
        client = boto3.client("ec2", region_name=region)
        custom_filter = [
            {"Name": "tag-key", "Values": [f"kubernetes.io/cluster/{ClusterName}"]},
            {"Name": "instance-state-name", "Values": ["pending", "running"]},
    ]

        response = client.describe_instances(Filters=custom_filter)
    # print(response)
        for reservation in response.get("Reservations"):
            for instances in reservation.get("Instances"):
                InstanceID = instances.get("InstanceId")
                InstanceTypes = instances.get("InstanceType")
                (ClusterName, instances.get("InstanceId"), (instances.get("InstanceType")))
                data = [AccountId,ClusterName, InstanceID, InstanceTypes, region]
                writer.writerow(data)