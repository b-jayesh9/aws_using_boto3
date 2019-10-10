import boto3

dynamodb = boto3.resource('dynamodb')

existing_tables = [table.name for table in dynamodb.tables.all()]


# sample list to insert

accounts_list = [['abc@ab.co', 'asdas', 'eirj'], ['q4esf@fds.co', 'fsdsfsd', 'a3r3f'], ['h4w4@ab.co', 'gw4g4', 'hwhw'],
                 ['whww@ab.co', 'wwgs', 'h4wh4']]

# we can add a file/other source to add data to the table.


def create_table(tbl, attr1, attr2):

    '''

    :param tbl:  name of the table to be created
    :param attr1: name of 1st attribute in key schema
    :param attr2: name of 2nd attribute in key schema
    :return: returns if table is successfully created or not by using inbuilt function table.table_status
    '''

    table = dynamodb.create_table(
        TableName=tbl,
        KeySchema=[
            {
                'AttributeName': attr1,
                'KeyType': 'HASH'
            },
            {
                'AttributeName': attr2,
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': attr1,
                'AttributeType': 'S'
            },
            {
                'AttributeName': attr2,
                'AttributeType': 'S'
            },

         ],

        ProvisionedThroughput={
             'ReadCapacityUnits': 50,
             'WriteCapacityUnits': 50
         }
    )

    return table.table_status


def put_data(tbl, user, pwd, name):
    table = dynamodb.Table(tbl)
    response = table.put_item(
        Item={
            'username': user,
            'password': pwd,
            'name': name
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def get_data(tbl, user, pwd):
    table = dynamodb.Table(tbl)
    response = table.get_item(
        AttributesToGet=[
            'username',
            'password'],
        Key={'username': user, 'password': pwd}

    )
    if 'Item' in response:
        print(response['Item'])
        return response['Item']
    else:
        return None


def write_batch(tbl):
    with dynamodb.Table(tbl).batch_writer() as batch:
        
        for i in range(len(accounts_list)):
            batch.put_item(
                Item={
                    'username': accounts_list[i][0],
                    'password': accounts_list[i][1],
                    'name': accounts_list[i][2]
                }
            )
    return dynamodb.Table(tbl).item_count


def delete_table(tbl):
    if tbl in existing_tables:
        table = dynamodb.Table(tbl)
        table.delete()
        dynamodb.Table(tbl).wait_until_not_exists()
        return "table deleted successfully" if tbl not in existing_tables else "Error in deleting table"
    else:
        return "No such table exists"


def update_item(tbl, user, pwd, key_to_insert, value_to_insert):
    table = dynamodb.Table(tbl)
    table.update_item(
        Key={
            'username': user,
            'password': pwd
        },
        UpdateExpression='SET {} = :val1'.format(key_to_insert),
        ExpressionAttributeValues={
            ':val1': value_to_insert
        }
    )

    return 0


def delete_item(tbl, key_val_pair):
    response = tbl.delete_item(
        Key={key_val_pair['key']: key_val_pair['value']}
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False
    return 0


def delete_all_items(tbl_to_delete_items):
    if tbl_to_delete_items in existing_tables:
        table = dynamodb.Table(tbl_to_delete_items)
        table.delete()
        try:
            dynamodb.Table(tbl_to_delete_items).wait_until_not_exists()
            table = create_table(tbl_to_delete_items)
        except Exception:
            print("Error occurred while deleting items in {} table".format(tbl_to_delete_items))
    else:
        print("No such table exists")
    return 0

