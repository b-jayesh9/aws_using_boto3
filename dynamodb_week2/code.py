import boto3

dynamodb = boto3.resource('dynamodb')

table_name = 'mynewtable'
existing_tables = [table.name for table in dynamodb.tables.all()]

#sample list to insert

accounts_list = [['abc@ab.co','asdas','eirj'], ['q4esf@fds.co','fsdsfsd','a3r3f'], ['h4w4@ab.co','gw4g4','hwhw'],
                 ['whww@ab.co', 'wwgs', 'h4wh4']]

#we can add a file/other source to add data to the table.


def create_table():
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'password',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'password',
                'AttributeType': 'S'
            },

         ],

        ProvisionedThroughput={
             'ReadCapacityUnits': 50,
             'WriteCapacityUnits': 50
         }
    )
    print(table.item_count)
    return table.table_status


def put_data():
    table = dynamodb.Table(table_name)
    response = table.put_item(
        Item={
            'username': 'eranahaata@gmail.com',
            'password': 'qazxsw',
            'name': 'Era Nsaha'
        }

    )
    return response


def get_data():
    table = dynamodb.Table(table_name)
    response = table.get_item(
        AttributesToGet=[
            'username',
            'password'],
        Key={'username': "eranahaata@gmail.com", 'password': "qazxsw"}

    )
    print(response)
    return response


def write_batch():
    with dynamodb.Table(table_name).batch_writer() as batch:
        for i in range(len(accounts_list)):
            batch.put_item(
                Item={
                    'username': accounts_list[i][0],
                    'password': accounts_list[i][1],
                    'name': accounts_list[i][2]
                }
            )


