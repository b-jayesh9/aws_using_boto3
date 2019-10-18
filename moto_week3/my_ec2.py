import boto3


def get_client():
    """
    Returns the ec2 boto3 client
    """
    return boto3.client('ec2')


def list_ec2_instances():
    """
    List EC2 InstanceId
    """
    ec2 = get_client()

    response = ec2.describe_instances()
    if response:
        for res in response.get('Reservations', []):
            for instance in res.get('Instances', []):
                yield instance['InstanceId']


def main():
    """
    Main entry
    """

    for instance in list_ec2_instances():
        print(instance)


if __name__ == '__main__':
    main()
