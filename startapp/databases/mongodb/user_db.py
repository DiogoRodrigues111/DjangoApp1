import pymongo


def create_instance_new_database(name_db: str, conn_host='mongodb://127.0.0.1:27017/'):
    """
    Create an new instance of the databases for MongoDB.

    And create too an database with without table.

    Args:
        name_db
            Name of Database for creating.

        conn_host
            Default Host and Port of the MongoDB.
    """

    client = pymongo.MongoClient(conn_host)

    create_db = client[name_db if name_db in client.list_database_names() is not None else None]
    if create_db.list_collection_names():
        print(f'MongoDB Database Founds: {create_db.list_collection_names()}')
