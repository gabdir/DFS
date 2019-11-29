import os
import json


def get_instances():
    key = "AKIAID4V7PGM4U7YIFOA"
    secret_key = "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"
    subnet = "subnet-e7d69f9d"
    file = "file.txt"
    os.system(f'aws configure set aws_access_key_id {key}')
    os.system(f'aws configure set aws_secret_access_key {secret_key}')
    os.system(f"aws configure set default.region us-east-2")
    os.system(f"rm {file}")
    os.system(f"aws ec2 describe-instances --filters 'Name=subnet-id,Values={subnet}' >> {file}")

    file = open("file.txt", "r")
    data = json.load(file)
    instance_ids = []
    for reservation in data["Reservations"]:
        for instances in reservation["Instances"]:
            instance_ids.append(instances["InstanceId"])
    print(instance_ids)
    return instance_ids
