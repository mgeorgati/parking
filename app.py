import psycopg2
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('map.html')

