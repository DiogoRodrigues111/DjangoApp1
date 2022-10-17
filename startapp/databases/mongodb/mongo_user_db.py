import pymongo
from pymongo.errors import CollectionInvalid


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
    try:
        client = pymongo.MongoClient(conn_host)
        print('MongoDB: Database created with successful.')
        create_db = client[name_db].create_collection(name_db)
    except CollectionInvalid:
        pass


def create_new_table_mongo(name, name_of_database):
    """
    
    Create a table in MongoDB

    Args:
        name:
            Name of the databases.

        name_of_databse:
            Name connections where the databases is instancing.

    """

    pass