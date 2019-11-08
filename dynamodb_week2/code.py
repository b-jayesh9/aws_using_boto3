import boto3
import json

from boto.dynamodb2.exceptions import ResourceInUseException
from botocore.exceptions import ClientError

dynamo_db = boto3.resource('dynamodb')
existing_tables = [table.name for table in dynamo_db.tables.all()]


def create_table(tbl, key_attr1, key_attr2):
    """
    :param tbl:  name of the table to be created
    :param key_attr1: name of 1st attribute in key schema
    :param key_attr2: name of 2nd attribute in key schema
    :return: returns if table is successfully created or not by using inbuilt function table.table_status
    """

    table = dynamo_db.create_table(
        TableName=tbl,
        KeySchema=[
            {
                'AttributeName': key_attr1,
                'KeyType': 'HASH'
            },
            {
                'AttributeName': key_attr2,
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': key_attr1,
                'AttributeType': 'S'
            },
            {
                'AttributeName': key_attr2,
                'AttributeType': 'S'
            },

        ],

        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    return table.table_status


def put_data(tbl, user, pwd, name):
    table = dynamo_db.Table(tbl)
    try:
        response = table.put_item(
            Item={
                'username': user,
                'password': pwd,
                'name': name
            },
            ConditionExpression='attribute_not_exists(username) AND attribute_not_exists(password)'

        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return 'successfully put data'
        else:
            return 'Failure in putting data'
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return "username and password already exists"


def get_data(tbl, user, pwd):
    table = dynamo_db.Table(tbl)
    response = table.get_item(
        AttributesToGet=[
            'username',
            'password'],
        Key={'username': user, 'password': pwd}

    )

    if 'Item' in response:
        return response['Item']
    else:
        return None


def write_batch(tbl):
    count = 0
    with open("dynamodb_week2\generated.json") as json_data:
        items = json.load(json_data)
        table = dynamo_db.Table(tbl)
        with table.batch_writer() as batch:
            # Loop through the JSON objects
            for item in items:
                try:
                    batch.put_item(Item=item)
                    count = count+1
                except Exception as e:
                    pass

    return count


def update_item(tbl, user, pwd, key_to_insert, value_to_insert):
    table = dynamo_db.Table(tbl)
    response = table.update_item(
        Key={
            'username': user,
            'password': pwd
        },
        UpdateExpression='SET {} = :val1'.format(key_to_insert),
        ExpressionAttributeValues={
            ':val1': value_to_insert
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return 'successfully updated data'
    else:
        return 'Failure in updating data'


def delete_item(tbl, key_val_pair):
    print(key_val_pair)
    table_to_delete_item = dynamo_db.Table(tbl)
    response = table_to_delete_item.delete_item(
        Key=key_val_pair
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 400:
        return False
    else:
        return True


def delete_table(tbl):
    if tbl in existing_tables:
        table = dynamo_db.Table(tbl)
        table.delete()
        dynamo_db.Table(tbl).wait_until_not_exists()
        all_tables_after_deletion = [table.name for table in dynamo_db.tables.all()]
        return "table deleted successfully" if tbl not in all_tables_after_deletion else "Error in deleting table"
    else:
        return "No such table exists"


def delete_all_items(tbl_to_delete_items):
    if tbl_to_delete_items in existing_tables:
        table = dynamo_db.Table(tbl_to_delete_items)
        try:
            table.delete()
            # will only get deleted if the table is in active state.
            dynamo_db.Table(tbl_to_delete_items).wait_until_not_exists()
            create_table(tbl_to_delete_items, key_attr1='username', key_attr2='password')
            return "All items deleted from table"
        except ResourceInUseException:
            return "Error occurred while deleting items in {} table".format(tbl_to_delete_items)
    else:
        return "No such table exists"
