from pigeon_app import pigeon_app
from pigeon_api import pigeon_api
from login_app import login_app
from flask import Flask, g
from db_conf import mongo_engine
import os


app = Flask(__name__)
mongo_engine.init_app(app)

@app.teardown_appcontext
def teardown_db(exception):
    neo4j_db = g.pop('neo4j_db', None)

    if neo4j_db is not None:
        neo4j_db.close()


app.config.update(
    TESTING=True,
    SECRET_KEY=os.environ.get("SECRET_KEY")
)

app.register_blueprint(pigeon_app)
app.register_blueprint(pigeon_api)
app.register_blueprint(login_app)
app.run(debug=True)
