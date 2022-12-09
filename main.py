from pigeon_app import pigeon_app
from pigeon_api import pigeon_api
from login_app import login_app
from flask import Flask, g
from users import connect_user_db

connect_user_db()

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    neo4j_db = g.pop('neo4j_db', None)

    if neo4j_db is not None:
        neo4j_db.close()

app.register_blueprint(pigeon_app)
app.register_blueprint(pigeon_api)
app.register_blueprint(login_app)
app.run(debug=True)