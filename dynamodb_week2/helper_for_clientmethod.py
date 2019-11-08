import code_using_clientmethod

REGION = "ap-south-1"
TABLE_NAME = "my-new-table"

if __name__ == "__main__":

    # dynomodb table creation and data insertion
    dynamodb_obj = code_using_clientmethod.Dynamodb(REGION, TABLE_NAME)
    dynamodb_obj.create_insert_data()

