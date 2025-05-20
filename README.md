# EKS Node Inventory Script

This Python script queries all EKS (Elastic Kubernetes Service) nodes in an AWS account and writes key information to a CSV file for inventory and tracking purposes.

## Overview

The script `eks-inventory.py` automates the process of gathering information about all Kubernetes nodes running in your EKS clusters across multiple AWS regions. It collects data such as:

- AWS Account ID
- Cluster Name
- EC2 Instance ID
- Instance Type
- AWS Region

## Prerequisites

- Python 3
- AWS SDK for Python (boto3)
- Appropriate AWS credentials configured
- Required permissions:
  - `eks:ListClusters`
  - `sts:GetCallerIdentity`
  - `ec2:DescribeInstances`

## How It Works

1. **Timestamp Generation**: Creates a unique timestamp to append to the output filename
2. **Region Iteration**: Queries specified AWS regions (us-east-1 and us-east-2)
3. **Cluster Identification**: Lists all EKS clusters in the account
4. **Account Detection**: Retrieves the AWS account ID
5. **Node Discovery**: For each cluster, identifies EC2 instances with the Kubernetes cluster tag
6. **Data Collection**: Extracts relevant information from each instance
7. **CSV Generation**: Writes all collected data to a timestamped CSV file

## Code Walkthrough

```python
#!/usr/bin/env python3
import boto3
import csv
from botocore.exceptions import ClientError
import json
import time

# Generate timestamp for the output file
timestr = time.strftime("%Y%m%d-%H%M%S")

# Define regions to query
regions = ['us-east-2','us-east-1']
for region in regions:  
    client = boto3.client("eks", region_name=region)
```

The script begins by importing necessary libraries and setting up a timestamp for the output file. It then defines the AWS regions to query and creates an EKS client.

```python
response = client.list_clusters()
clusterid = response.get("clusters")

# Set up CSV header and file
header = ["AccountId","ClusterName", "InstanceID", "InstanceTypes", "Region"]
with open(f"eks-node-{timestr}.csv", "w", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
```

Here, the script gets a list of all EKS clusters and prepares a CSV file with appropriate headers.

```python
    for cluster in clusterid:
        ClusterName = cluster

        # Get AWS account ID
        client = boto3.client('sts')
        response = client.get_caller_identity()
        AccountId = response.get('Account')
```

For each cluster, the script retrieves the AWS account ID using the Security Token Service (STS).

```python
        # Query EC2 instances with cluster tag
        client = boto3.client("ec2", region_name=region)
        custom_filter = [
            {"Name": "tag-key", "Values": [f"kubernetes.io/cluster/{ClusterName}"]},
            {"Name": "instance-state-name", "Values": ["pending", "running"]},
        ]

        response = client.describe_instances(Filters=custom_filter)
```

The script then creates an EC2 client and queries for instances that:
1. Have a tag key matching the cluster name pattern used by EKS
2. Are in either "pending" or "running" states

```python
        # Process instance data and write to CSV
        for reservation in response.get("Reservations"):
            for instances in reservation.get("Instances"):
                InstanceID = instances.get("InstanceId")
                InstanceTypes = instances.get("InstanceType")
                (ClusterName, instances.get("InstanceId"), (instances.get("InstanceType")))
                data = [AccountId, ClusterName, InstanceID, InstanceTypes, region]
                writer.writerow(data)
```

Finally, the script extracts the relevant information from each instance and writes it to the CSV file.

## Output

The script generates a CSV file named `eks-node-YYYYMMDD-HHMMSS.csv` with the following columns:
- AccountId: The AWS account number
- ClusterName: Name of the EKS cluster
- InstanceID: EC2 instance ID of the node
- InstanceTypes: EC2 instance type (e.g., t3.medium, m5.large)
- Region: AWS region where the node is deployed
