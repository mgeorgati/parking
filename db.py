# import Python's built-in JSON library
import json
# import the psycopg2 database adapter for PostgreSQL
import psycopg2
from psycopg2 import Error
try:
    # Connect to an existing database
    connection = psycopg2.connect(dbname = "parking",
        user = "postgres",
        host = "localhost",
        port = '5432',
        #### ---- YOU NEED TO CHANGE THIS!!!! ---- ####
        password = "postgres",
        sslmode="disable")
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
    
    # use Python's open() function to load the JSON data
    with open('phus.json') as json_data:
        # use load() rather than loads() for JSON files
        df = json.load(json_data)
      
    cursor.execute('DROP TABLE if exists phus;')
    connection.commit()
    cursor.execute('CREATE TABLE phus (id int, code varchar, streetname varchar, \
        bemaerkning varchar, geometry geometry);')
    # Add a commit on the connection.
    connection.commit()
    for i in range(len(df)):
        feature = df[i]['properties']
        geometry = df[i]['geometry']
        geom = json.dumps(geometry)
        
        id = feature['id']
        code = feature['vejkode']
        street_name = feature['vejnavn']
        bemaerkning = feature['bemaerkning']
        cursor.execute("""INSERT INTO phus (id, code, streetname, bemaerkning, geometry)  
                       VALUES ({0}, {1}, '{2}', '{3}', ST_AsText(ST_GeomFromGeoJSON('{4}')))"""
                       .format(id, code, street_name, bemaerkning, geom))
    connection.commit()
    print("Records Successfully Imported!")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")