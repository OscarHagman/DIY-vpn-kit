import json
import boto3
from botocore.config import Config
import time


def create_instance(access_key: str, secret_key: str, instance_location: str, security_group: str):
    my_config = Config(
        region_name=instance_location,
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    ec2_client = boto3.client(
        'ec2',
        config=my_config,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    instance = ec2_client.run_instances(
        ImageId="ami-0ff338189efb7ed37",
        MinCount=1,
        MaxCount=1,
        InstanceType="t3.micro",
        SecurityGroups=[security_group],
        KeyName="Simple-DevOps"
    )

    print("sleeping for 30 seconds to give instance time to boot up")
    time.sleep(25)
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)

    instance_id = instance["Instances"][0]["InstanceId"]
    instance_description = ec2_client.describe_instances(InstanceIds=[instance_id])
    return instance_description


def create_keys_config(access_key, secret_key, ssh_key_name):
    keys = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
        "ssh_key_name": ssh_key_name
    }
    with open("keys_config.json", "w") as keys_config:
        json.dump(keys, keys_config)


def load_keys_config(file_path: str):
    try:
        with open(file_path, "r") as json_keys:
            keys = json.load(json_keys)
            return keys
    except FileNotFoundError:
        print("Configuration file not found")
        return False
    except Exception as e:
        print("Unexpected error:\n\n", e)
        exit()


def setup_user():
    while True:
        access_key = input("Aws access key: ")
        secret_key = input("Aws secret key: ")
        ssh_key_name = input("SSH key name: ")

        print("\nIs this correct? (y/n)\n" +
              "Aws access key:", access_key +
              "\nAws secret key:", secret_key +
              "\nSSH key name:", ssh_key_name)

        user_input = input()
        if user_input.upper() == "Y":
            break

    create_keys_config(access_key, secret_key, ssh_key_name)


def main():
    while True:
        keys = load_keys_config("keys_config.json")
        if keys:
            keys = load_keys_config("keys_config.json")
            instance_description = create_instance(
                keys["aws_access_key_id"],
                keys["aws_secret_access_key"],
                "eu-north-1",
                "launch-wizard-1"
            )
            public_ip = instance_description["Reservations"][0]["Instances"][0]["NetworkInterfaces"][0][
                "PrivateIpAddresses"][0]["Association"]["PublicIp"]
            print("PUBLIC IP:", public_ip)
            break
        else:
            print("Starting configuration file setup\n")
            setup_user()


if __name__ == "__main__":
    main()
