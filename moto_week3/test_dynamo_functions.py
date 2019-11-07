import unittest
import boto3
from moto import mock_dynamodb2


class TestDynamo(unittest.TestCase):

    def setUp(self):
        pass

    @mock_dynamodb2
    def test_dynamo_db(self):
        table_name = 'test'
        dynamodb = boto3.resource('dynamodb', 'us-east-1')

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'key',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'key',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # add a sample item to the table to check if mocking is being done successfully

        item = {'key': 'value'}

        table.put_item(Item=item)

        table = dynamodb.Table(table_name)
        response = table.get_item(
            Key={
                'key': 'value'
            }
        )
        print(response)
        if 'Item' in response:
            item = response['Item']

        self.assertTrue("key" in item)
        self.assertEqual(item["key"], "value")
