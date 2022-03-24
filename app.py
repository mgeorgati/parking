import psycopg2
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('map.html')

@app.route('/parking')
def hello_park():
    lat = float(request.args.get("lat", 54))
    lng = float(request.args.get("lng", 10))
    
    # Connect to an existing database
    conn = psycopg2.connect(dbname = "parking",
        user = "postgres",
        host = "localhost",
        port = '5432',
        password = "postgres",
        sslmode="disable")
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Query the database and obtain data as Python objects
    cur.execute("""SELECT id, streetname, bemaerkning, ST_AsGeoJSON(geometry)
                            FROM phus
                            ORDER BY geometry <-> 'SRID=4326;POINT(%s %s)'::geometry
                            LIMIT 1;""", (lng, lat))
    row = cur.fetchone()
    output = '''{
        "type": "Feature",
        "properties": {
            "id": '''+str(row[0])+''',
            "streetname": "'''+row[1]+'''",
            "firm": "'''+row[2]+'''"},
        "geometry": '''+ row[3]+ '''
    }
    '''

    cur.close()
    conn.close()

    return Response(response=output,
                    status=200,
                    mimetype="application/json")

