import boto3


def get_client():
    """
    get the client endpoint for the service
    """
    return boto3.client("s3")


def list_s3_buckets():
    """
    lists all the bucket names and stores them, to be used in the main function
    """
    s3 = get_client()
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        yield(bucket['Name'])


def list_s3_objects(bucket):
    """
    lists all the objects of a particular bucket and stores them, to be used in the main function
    """
    s3 = get_client()
    response = s3.list_objects_v2(Bucket=bucket)
    if response:
        try:
            for _object in response['Contents']:
                yield(_object['Key'])
        except KeyError:
            return "KeyError. No such key exists in the specified bucket"


def read_s3_object(bucket, key):
    """
    reads the data of a particular object of a object and stores them, to be used in the main function
    """
    s3 = get_client()

    response = s3.get_object(Bucket=bucket, Key=key)
    if response:

        yield(response['Body'].read())


def main():
    """
    main function to print data obtained through various functions 
    """
    for buckets in list_s3_buckets():
        print('{}'.format(buckets))

        for key in list_s3_objects(buckets):
            print("{}".format(key))

            for body in read_s3_object(buckets, key):
                print("{}".format(body))
