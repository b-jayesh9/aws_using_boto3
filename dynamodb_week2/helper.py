import code as c

if __name__ == '__main__':
    if c.table_name not in c.existing_tables:
        c.create_table()
        c.write_batch()
        c.get_data()
    elif c.table_name in c.existing_tables:
        try:
            c.write_batch()
            c.get_data()
        except Exception:
            c.get_data()
