from boto.dynamodb2.exceptions import ConditionalCheckFailedException
import code as c
import time
table_name = 'my_new_table'

if __name__ == '__main__':
    if table_name not in c.existing_tables:

        print(c.create_table('my_new_table', 'username', 'password'))
        # takes 3 parameters: table_name, key attribute 1 and key attribute 2

        c.dynamo_db.Table(table_name).wait_until_exists()

        print("table created") if table_name in [table.name for table in c.dynamo_db.tables.all()] \
            else print("table creation failed")

        print("***Putting Data***")
        print(c.put_data('my_new_table', 'abc@xyz.com', 'qazxsw', 'jay'))
        # takes 4 parameters: table_name, key attribute 1, key attribute 2 and some other attribute

        print("***Getting Data***")
        print(c.get_data('my_new_table', 'abc@xyz.com', 'qazxsw'))
        # takes 3 parameters: table_name, key attr1, key attr2

        c.write_batch('my_new_table')
        # takes 1 parameter: table_name

        c.update_item('my_new_table', 'abc@xyz.com', 'qazxsw', 'age', 21)
        # takes 5 parameters: table_name, key attr1, key attr2, key of key value pair, value of key value pair

    else:
        print("putting")
        c.put_data('my_new_table', 'abc@xyz.com', 'qazxsw', 'jay')
        # takes 4 parameters: table_name, key attribute 1, key attribute 2 and some other attribute

        c.write_batch(table_name)
        # takes 1 parameter: table_name

        c.get_data(table_name, 'abc@xyz.com', 'qazxsw')
        # takes 3 parameters: table_name, key attr1, key attr2

    time.sleep(5)
    c.delete_item(table_name, {'username': 'abc@xyz.com', 'password': 'qazxsw'})
    # takes 2 parameters: table_name and key-value pair
    
    c.delete_all_items(table_name)
    # takes 1 parameter: table_name
    
    time.sleep(5)
    c.delete_table(table_name)
    # takes 1 parameter: table_name

