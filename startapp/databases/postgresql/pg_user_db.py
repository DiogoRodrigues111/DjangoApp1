import psycopg2
from django.shortcuts import redirect
from psycopg2 import errors


""" GLOBALS """

""" Postgres constant variables. """
# That variable is GET in the Forms, and not POST.
global usr_name, usr_email, usr_password


""" CONSTANTS """


class PgVariables:
    """ Get and Set, properties """

    PG_INSERT_DATA_TO_TABLE: str
    PG_UPDATE_WITH_PASSWORD: str


def insert_new_data_pg(name, email, password):
    """ Insert into the table. """

    # Pg SQL Iterations
    global usr_name, usr_email, usr_password

    # Set values the user to global variable.
    usr_name = name
    usr_email = email
    usr_password = password

    # Insert values to table.
    PgVariables.PG_INSERT_DATA_TO_TABLE = \
        F'INSERT INTO pgUserTab(name, email, password) VALUES ({usr_name}, {usr_email}, {usr_password});'

    return PgVariables.PG_INSERT_DATA_TO_TABLE


def update_new_table_pg(name, password):
    """

    Update Postgresql for new values table.

    Note: It is HTML page that update
        See: templates/update.html.

    Args:
        name:
            This is really go changed.

        password:
            This is really go changed.

    """

    # Pg SQL Iterations
    global usr_name, usr_email, usr_password

    # TODO:
    #   Get iteration with globals variables, before insert datas.
    #   Find in Database name values,
    #   Find and check if email is correspond with Database values inserts.
    #   Check if password really exists for others datas inserted.

    # Update table with password of the user.
    PgVariables.PG_UPDATE_WITH_PASSWORD = \
        F'UPDATE pgUserTab SET name = {name}, password = {password} WHERE email = {usr_email};'

    if PgVariables.PG_UPDATE_WITH_PASSWORD:

        # Get new values of the globals variables.
        # This is Get properties

        usr_name = name
        usr_password = password

        redirect('/')

    else:
        # Failed to access user email on database.
        redirect('/update')

        # Debug.
        print('CHECK_EMAIL is not equal to Email registered in Database.')
        # Launching an Exception RuntimeError.
        raise RuntimeError('CHECK_EMAIL is not equal to Email registered in Database.')

    return PgVariables.PG_UPDATE_WITH_PASSWORD


def pg_delete_columns(email):
    """
    Delete datas on Databases.

    Args:
        email:
            That routine take values of the email, and then delete if possible.

    """

    """ That operation not can be reversible. """

    global usr_name, usr_email, usr_password

    if email is usr_email:
        usr_name = ''
        usr_email = ''
        usr_password = ''
    else:
        raise RuntimeError('Not can be DELETE values on Database. Something Wrong occur.')


def create_new_cmd_pg(query):
    """
    Create Command-Line for query and commit sequence to Postgres.

    Args:
        query: Is a Command-Line.

    See:
        DuplicateTable removed that sequence.

    Returns:
        It's returns an connection from psycopg2.connection
    """

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
