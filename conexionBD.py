import psycopg2
import os

def conexionBD():
    conexion = ''    
    try:
        host     = os.environ.get('POSTGRESQL_HOST')
        username = os.environ.get('POSTGRESQL_USER')
        password = os.environ.get('POSTGRESQL_PASSWORD')
        database = os.environ.get('POSTGRESQL_DB')

        conexion = psycopg2.connect(host = host,database = database,user = username,password = password)
        
        conexion.autocommit = True

    except Exception as e:
        print("Error", e)        

    return conexion

    # host = os.environ.get('POSTGRESQL_HOST')
    # user = os.environ.get('POSTGRESQL_USER')
    # password = os.environ.get('POSTGRESQL_PASSWORD')
    # database = os.environ.get('POSTGRESQL_DB')
    # puerto = 5432

    # conn_engine = ''

    # try:
    #     conn_engine = f'''postgresql://{user}:{password}@{host}:{puerto}/{database}'''
    #     conn_engine = create_engine(conn_engine)
    # except Exception as e:
    #     print(e)

    # return conn_engine

