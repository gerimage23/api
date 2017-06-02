import psycopg2


def execute_sql_statement(sql_statement, values=list()):
    try:
        # setup connection string
        with open('static/conn_str.txt', 'r') as file:
            conn_str = file.readline()
        dbname = conn_str.split(',')[0]
        user = conn_str.split(',')[1]
        host = conn_str.split(',')[2]
        password = conn_str.split(',')[3]

        connect_str = "dbname="+dbname+" user="+user+" host="+host+" password="+password
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # set autocommit option, to do every query when we call it
        conn.autocommit = True

    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

    cursor = conn.cursor()
    cursor.execute(sql_statement, values)
    if sql_statement[:6] == 'SELECT':
        rows = list(cursor.fetchall())
        return rows
