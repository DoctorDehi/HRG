from app import app as main_app
from  pigeon_api import pigeon_api
from flask import Flask, g


app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    neo4j_db = g.pop('neo4j_db', None)

    if neo4j_db is not None:
        neo4j_db.close()

app.register_blueprint(main_app)
app.register_blueprint(pigeon_api)
app.run(debug=True)