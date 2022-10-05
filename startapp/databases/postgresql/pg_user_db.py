import psycopg2
from django.shortcuts import redirect
from psycopg2 import errors


""" GLOBALS """

""" Postgres constant variables. """
# That variable is GET in the Forms, and not POST.
global usr_name, usr_email, usr_password


""" CONSTANTS """

# Update table with password of the user.
PG_UPDATE_WITH_PASSWORD = \
    'UPDATE pgUserTab' \
    F'SET name = {usr_name}, password = {usr_password} WHERE email = {usr_email};'

# Insert values to table.
PG_INSERT_DATA_TO_TABLE = \
    F'INSERT INTO pgUserTab(name, email, password) VALUES ({usr_name}, {usr_email}, {usr_password});'


def insert_new_data_pg(name, email, password):
    """ Insert into the table. """

    # Pg SQL Iterations
    global usr_name, usr_email, usr_password

    # Set values the user to global variable.
    usr_name = name
    usr_email = email
    usr_password = password

    return PG_INSERT_DATA_TO_TABLE


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

    # if check_email is find in database
    # ... update new values with global.
    if usr_email:

        # Get new values of the globals variables.

        name = usr_name
        password = usr_password

        redirect('/')

    else:
        # Failed to access user email on database.
        redirect('/update')

        # Debug.
        print('CHECK_EMAIL is not equal to Email registered in Database.')
        # Launching an Exception RuntimeError.
        raise RuntimeError('CHECK_EMAIL is not equal to Email registered in Database.')

    return PG_UPDATE_WITH_PASSWORD


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
