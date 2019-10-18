import boto3

def list_tables():
    dynamodb = boto3.resource('dynamodb')
    tables = [table.name for table in dynamodb.tables.all()]
    yield tables


def main():
    for x in list_tables():
        print('{}'.format(x))

