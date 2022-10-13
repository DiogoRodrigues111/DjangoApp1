from distutils.util import execute
from sys import executable
import psycopg2
from psycopg2 import errors


def insert_new_data_pg(name, email, password, is_banned: bool):
    """

    Insert into the table.

    Args:
        name:
            Data's for insert to columns Name.

        email:
            Data's for insert in columns Email.

        password:
            Data's to add in columns Password.

        is_banned:
            If user take banned. It is a number.

    Returns:
        Status Added, or data's added with success.

    """

    # Insert values to table.
    pg_insert_data_to_table = \
        F'INSERT INTO pgUserTab(name, email, password, is_banned) VALUES (%s, %s, %s, %s)'

    status_added = create_new_cmd_pg(pg_insert_data_to_table, seq=(name, email, password, is_banned))

    return status_added


def update_new_table_pg(name, password, email):
    """

    Update Postgresql for new values table.

    Note: It is HTML page that update
        See: templates/update.html.

    Args:
        name:
            This is really go changed.

        password:
            This is really go changed.

        email:
            Email the user, for check it. And then UPDATED.

    """

    # Update table with password of the user.
    pg_update_with_email = \
        R'UPDATE pgUserTab SET name = %s, password = %s WHERE email = %s'

    status_added = create_new_cmd_pg(pg_update_with_email, seq=(name, password, email))

    return status_added


def pg_delete_columns(email):
    """

    Delete datas on Databases.

    Obs:
        It is not can be recovery.

    Args:
        email:
            That routine take values of the email, and then delete if possible.

    Returns:
        Status Added to delete user.

    """

    """ That operation not can be reversible. """

    create_new_cmd_pg(query='''DELETE FROM pgUserTab WHERE email=%s;''', seq=(email,))

    return None

def pg_drop_if_exists(table_name):
    """ 
    
    Drop if exists the table in database.

    Args:
        table_name:
            Name of the Table in database registered.

    Returns:
        SQL command line working.

     """

    pg_drop_table = "DROP TABLE pgUserTab;"
    status_added = create_new_cmd_pg(pg_drop_table)

    return status_added

def pg_user_banned(is_banned, email):
    """
    
    User can be banned.

    This operation can be recovered, with update.

    Args:
        is_banned:
            If user is banned. ( It is a number. 0 or 1 ).

        email:
            Is email of the user to be Banned.

    Returns:
        Status working, User Banned.
    """

    pg_user_banned = "UPDATE pgUserTab SET is_banned = %s WHERE email = %s"
    status_added = create_new_cmd_pg(pg_user_banned, seq=(is_banned, email))

    return status_added


def create_new_cmd_pg(query, seq=None):
    """

    Create Command-Line for query and commit sequence to Postgres.

    Args:
        query:
            Is a Command-Line.

        seq:
            Is Args of the query

    See:
        DuplicateTable removed that sequence.

    Returns:
        It's returns a connection from psycopg2.connection

    """

    new_instance = psycopg2.connect(dbname='myuserdb', host='localhost', user='root', password='root', port='5432')
    if new_instance:
        print('Connection ready with Postgresql.')
    else:
        print('Failed to stables connection.')

    # Open the cursor to perform database operations.
    cursor = new_instance.cursor()
    try:
        cursor.execute(query, seq)
        print(f'Query Executed: {query}')
        new_instance.commit()
    except errors.DuplicateTable:
        pass

    return new_instance
