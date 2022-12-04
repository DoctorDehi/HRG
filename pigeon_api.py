import json
from neo4j import GraphDatabase, basic_auth
from app import app
from flask import g, request, jsonify


driver = GraphDatabase.driver("bolt://127.0.0.1:7689", auth=basic_auth("neo4j", "knock-cape-reserve"))


def get_db():
    if 'db' not in g:
        g.neo4j_db = driver.session()

    return g.neo4j_db

@app.teardown_appcontext
def teardown_db(exception):
    neo4j_db = g.pop('neo4j_db', None)

    if neo4j_db is not None:
        neo4j_db.close()


@app.route('/api/pigeon', methods=['GET'])
def query_pigeons():
    id = request.args.get('id')
    db = get_db()
    q = "MATCH (a:Pigeon) "
    if id:
        q = q + "WHERE a.id = $id "
    q = q + "RETURN a AS pigeon"
    result = db.run(q, id=id)
    return jsonify(result.data())


@app.route('/api/pigeon', methods=['PUT'])
def create_pigeon():
    pigeon = json.loads(request.data)
    id = str(pigeon["cislo_krouzku"]) + "-" + str(pigeon["rocnik"])
    db = get_db()
    db.run("CREATE (p:Pigeon {  id: $id,"
                                "cislo_krouzku: $cislo_krouzku,"
                                "rocnik: $rocnik"
           "}) ", id=id, cislo_krouzku=pigeon["cislo_krouzku"], rocnik=pigeon["rocnik"])

    return jsonify(pigeon)


@app.route('/api/pigeon', methods=['POST'])
def update_pigeon():
    pigeon = json.loads(request.data)
    if pigeon.get("id"):
        db = get_db()
        q = "MATCH (p:Pigeon) " \
            "WHERE p.id = $id " \
            "SET "
        for key, value in dict(pigeon).items():
            q = q + f"p.{key} = '{value}', "
        q = q[:-2]

        db.run(q, id=pigeon["id"])
    return jsonify(pigeon)


@app.route('/api/pigeon', methods=['DELETE'])
def delete_pigeon():
    pigeon = json.loads(request.data)
    if pigeon.get("id"):
        db = get_db()

        db.run("MATCH (a:Pigeon)"
               "WHERE a.id = $id "
               "DELETE a", id=pigeon["id"])

    return jsonify(pigeon)