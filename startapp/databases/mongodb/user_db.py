import pymongo


def create_instance_new_database(name_db, conn_host='mongodb://127.0.0.1:27017/'):
    """
    Create an new instance of the databases for MongoDB.

    And create too an database with without table.

    Args:
        name_db
            Name of Database for creating.

        conn_host
            Default Host and Port of the MongoDB.
    """

    chk_database = f'{name_db}'

    client = pymongo.MongoClient(conn_host)
    create_db = client[name_db]

    if chk_database in client.list_databases():
        print(f'API: Database created with success with name {create_db}')
        print(' ')
        print(f'API: List of The databases founds: {client.list_databases()}')
