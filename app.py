import os

from flask import Flask, g
from flask_wtf.csrf import CSRFProtect

from db_conf import mongo_engine
from login_app import login_app, login_manager
from pigeon_api import pigeon_api
from pigeon_app import pigeon_app

# app definition
app = Flask(__name__)

container_id = 'localhost' # 'cf558ed5c392'
app.config['MONGODB_HOST'] = f'mongodb://{container_id}:27019/credentials'
mongo_engine.init_app(app)
login_manager.init_app(app)
csrf = CSRFProtect(app)
#app.login_manager = login_manager

@app.teardown_appcontext
def teardown_db(exception):
    neo4j_db = g.pop('neo4j_db', None)

    if neo4j_db is not None:
        neo4j_db.close()


app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
)

app.register_blueprint(pigeon_app)
app.register_blueprint(pigeon_api)
app.register_blueprint(login_app)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
