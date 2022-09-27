import psycopg2
from psycopg2 import errors


def create_new_cmd_pg(query):
    new_instance = psycopg2.connect(dbname='myuserdb', host='localhost', user='root', password='root', port='5432')
    if new_instance:
        print('Connection ready with Postgresql.')
    else:
        print('Failed to stables connection.')

    # Open the cursor to perform database operations.
    cursor = new_instance.cursor()
    try:
        cursor.execute(query)
        print(f'Query Executed: {query}')
        new_instance.commit()
    except errors.DuplicateTable:
        pass

    return new_instance
