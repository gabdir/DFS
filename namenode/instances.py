import os
import json


def get_instances(key, secret_key, subnet):
    print(key, secret_key, subnet)
    file = "instancesfile.txt"
    os.system(f'aws configure set aws_access_key_id {key}')
    os.system(f'aws configure set aws_secret_access_key {secret_key}')
    os.system(f"aws configure set default.region us-east-2")
    os.system(f"rm {file}")
    os.system(f"aws ec2 describe-instances --filters 'Name=subnet-id,Values={subnet}' >> {file}")

    file = open(file, "r")
    data = json.load(file)
    instances_list = []
    for reservation in data["Reservations"]:
        for instances in reservation["Instances"]:
            instances_list.append(instances["NetworkInterfaces"][0]["Association"]["PublicDnsName"])
    print(instances_list)
    return instances_list


if __name__ == "__main__":
    #get_instances()
    get_instances("AKIAJ7DAXD66HEIENCEA", "ln9uWqZHPf4y59vuUuThfNdCwGR8k8hCfnC956C+", "subnet-e7d69f9d")
