import boto3


def get_client():
    return boto3.client("s3")


def list_s3_buckets():
    s3 = get_client()
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        yield(bucket['Name'])


def list_s3_objects(bucket):
    s3 = get_client()
    response = s3.list_objects_v2(Bucket=bucket)
    if response:
        try:
            for _object in response['Contents']:
                yield(_object['Key'])
        except KeyError:
            pass


def read_s3_object(bucket, key):
    s3 = get_client()

    response = s3.get_object(Bucket=bucket, Key=key)
    if response:

        yield(response['Body'].read())


def main():
    for buckets in list_s3_buckets():
        print('[{}]'.format(buckets))

        for key in list_s3_objects(buckets):
            print("[{}]".format(key))

            for body in read_s3_object(buckets, key):
                print("{}".format(body)[1:])
