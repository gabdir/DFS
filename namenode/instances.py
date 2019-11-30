import os
import json


def get_instances():
    keys_file = open("keys", "r")
    key = keys_file.readline()
    secret_key = keys_file.readline()
    subnet = "subnet-e7d69f9d"
    file = "file.txt"
    os.system(f'aws configure set aws_access_key_id {key}')
    os.system(f'aws configure set aws_secret_access_key {secret_key}')
    os.system(f"aws configure set default.region us-east-2")
    os.system(f"rm {file}")
    os.system(f"aws ec2 describe-instances --filters 'Name=subnet-id,Values={subnet}' >> {file}")

    file = open("file.txt", "r")
    data = json.load(file)
    instances_list = []
    for reservation in data["Reservations"]:
        for instances in reservation["Instances"]:
            instances_list.append(instances["NetworkInterfaces"][0]["Association"]["PublicDnsName"])
    print(instances_list)
    return instances_list


if __name__ == "__main__":
    get_instances()
