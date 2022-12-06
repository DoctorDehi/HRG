import json
from flask import Blueprint, g, request, jsonify
from db_conf import driver


pigeon_api = Blueprint('app', __name__)


def get_db():
    if 'db' not in g:
        g.neo4j_db = driver.session()

    return g.neo4j_db


@pigeon_api.route('/api/pigeon', methods=['GET'])
def query_pigeons():
    pg_id = request.args.get('id')
    db = get_db()
    q = "MATCH (a:Pigeon) "
    if pg_id:
        q = q + "WHERE a.id = $id "
    q = q + "RETURN a AS pigeon"
    result = db.run(q, id=pg_id)
    return jsonify(result.data())


@pigeon_api.route('/api/pigeon', methods=['PUT'])
def create_pigeon():
    pigeon = json.loads(request.data)
    pg_id = str(pigeon["cislo_krouzku"]) + "-" + str(pigeon["rocnik"])
    db = get_db()
    db.run("CREATE (p:Pigeon {  id: $id,"
                                "cislo_krouzku: $cislo_krouzku,"
                                "rocnik: $rocnik"
           "}) ", id=pg_id, cislo_krouzku=pigeon["cislo_krouzku"], rocnik=pigeon["rocnik"])

    return jsonify(pigeon)


@pigeon_api.route('/api/pigeon', methods=['POST'])
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


@pigeon_api.route('/api/pigeon', methods=['DELETE'])
def delete_pigeon():
    pigeon = json.loads(request.data)
    if pigeon.get("id"):
        db = get_db()

        db.run("MATCH (a:Pigeon)"
               "WHERE a.id = $id "
               "DELETE a", id=pigeon["id"])

    return jsonify(pigeon)