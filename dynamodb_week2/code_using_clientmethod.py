import boto3
import time


class Dynamodb:
    def __init__(self, region, table_name):
        self.client_dynamodb = boto3.client('dynamodb', region_name=region)
        self.table_name = table_name

    def create_table(self):
        self.client_dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': "name",
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': "name",
                    'AttributeType': 'S'
                }
            ],

            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        while self.table_status() != 'ACTIVE':
            time.sleep(2)

    def put_data(self):
        self.client_dynamodb.put_item(
            TableName=self.table_name,
            Item={
                'name': {'S': 'csv'},
                'phone': {'N': '100'},
            }
        )

    def get_data(self):
        response = self.client_dynamodb.get_item(
            TableName=self.table_name,
            Key={
                'name': {'S': 'csv'}
            }
        )
        print(response)

    def table_status(self):
        response = self.client_dynamodb.describe_table(
            TableName=self.table_name
        )
        return response['Table']['TableStatus']

    def create_insert_data(self):
        response = self.client_dynamodb.list_tables()
        existing_tables = response['TableNames']
        if self.table_name not in existing_tables:
            self.create_table()
        # self.put_data()
        self.get_data()
        print("table created and data inserted")