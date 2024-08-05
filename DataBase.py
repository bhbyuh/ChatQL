import psycopg2

def session_creation(databasename,Dbpassword):
    conn=psycopg2.connect(
        dbname=databasename,
        user="postgres",
        password=Dbpassword,
        port=5432
    )

    cur=conn.cursor()

    return [conn,cur]

def table_creation(conn,cur,query):
    cur.execute(query)
        
    conn.commit()

def insert_data(cursor,conn,df,insert_query,table_name):
    # Generate SQL insert query
    columns = df.columns.tolist()
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"

    for index, row in df.iterrows():
        values = tuple(row)
        cursor.execute(insert_query, values)

    conn.commit()

def get_data(cursor,query):
    
    cursor.execute(query)
    
    rows=cursor.fetchall()
    return rows