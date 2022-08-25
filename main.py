# Depending on Environment variables, serve an ingress pod front end or a service pod API


import requests
import psycopg2
from flask import Flask

import os

# env section
'''
# example bash env vars
export CT_POD_TYPE=INGRESS_POD_DEMO
export CT_FE_HOST=blah
export CT_DB_HOST=blah
export CT_BE_HOST=blah
'''
# Mapping to environment variables
config_env = {
    'app':            'CT_POD_TYPE',
    'front_end_host': 'CT_FE_HOST',
    'db_host': 'CT_DB_HOST',
    'back_end_host':  'CT_BE_HOST'
    }
# Realize config
config = {}
for key in config_env:
    config[key] = os.getenv(config_env[key])
    if config[key] is None:
        raise AttributeError(f"Missing environment variables.  Please define '{key}' by setting {config_env[key]} in the environment.")

# Postgres connection info
PGHOST = "psql"
PGDATABASE = "psql"
PGUSER = "postgres"
PGPASSWORD = "psql"

# Ingress Pod
if config['app']=='INGRESS_POD_DEMO':
    app = Flask('Ingress Pod Demo')
    @app.route("/")
    def index_ing():
        return """
        <br>Ingress pod is reachable and responsive!
        <br>
        <br>Other links:
        <br><a href="service">Service connection</a>
        <br><a href="db">Database connection</a>
        <br><a href="full">Test service db connection</a>
        """

    @app.route("/service")
    def hit_service():
        try:
            result = requests.get(f"http://{config['back_end_host']}:12345/").text
        except Exception as e:
            result = f"Couldn't connect to service, got:\n{e}"
        return result

    @app.route("/db", methods=["GET"])
    def hit_db_ing():
        try:
            connection = psycopg2.connect(database=PGDATABASE, host=PGHOST, user=PGUSER, password=PGPASSWORD)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM hello_table")
            result = cursor.fetchall()
        except Exception as e:
            result = f"Couldn't connect to db, got:\n{e}"
        return result

    @app.route("/full")
    def hit_service_and_db():
        try:
            result = requests.get(f"http://{config['back_end_host']}:12345/db").text
        except Exception as e:
            result = f"Couldn't connect to service, got:\n{e}"
        if "Couldn't" in result:
            result = f"Couldn't hit db from service, got: [{result}]"
        return result
    # Serve
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=54321, debug=True)


# Service Pod
if config['app']=='SERVICE_POD_DEMO':
    app = Flask('Service Pod Demo')
    # Boring route
    @app.route("/")
    def index_svc():
        return "Service pod is reachable and responsive!"
    #db route
    @app.route("/db", methods=["GET"])
    def hit_db_svc():
        try:
            connection = psycopg2.connect(database=PGDATABASE, host=PGHOST, user=PGUSER, password=PGPASSWORD)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM hello_table")
            result = cursor.fetchall()
        except Exception as e:
            result = f"Couldn't connect to db, got:\n{e}"
        return result
    # Serve
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=12345, debug=True)

# DB info (not implemented here, just notes )
'''
While standing up psql db, run the following

create table
    hello_table
as
    select 'Database is reachable and responsive!' AS hello_column;

'''
