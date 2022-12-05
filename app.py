from flask import Flask, render_template, request, g
from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import json

app = Flask(__name__)

driver = GraphDatabase.driver("bolt://127.0.0.1:7689", auth=basic_auth("neo4j", "knock-cape-reserve"))

def get_db():
    if 'db' not in g:
        g.neo4j_db = driver.session()

    return g.neo4j_db

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-pigeon', methods=['GET', 'POST'])
def add_pigeon():
    if request.method == "GET":
        return render_template("add_pigeon.html")
    else:
        cislo_krouzku_full = request.form.get("cislo_krouzku", "")
        if not cislo_krouzku_full:
            return render_template("add_pigeon.html", add_pigeon_success=False, error="Nebylo zadáno číslo kroužku! Data nebyla uložena")

        cislo_krouzku, rocnik = cislo_krouzku_full.split("/")

        holub_data = {
            "id" : str(cislo_krouzku) + "-" + str(rocnik),
            "cislo_krouzku": cislo_krouzku,
            "rocnik": rocnik,
            "pohlavi": request.form.get("pohlavi", ""),
            "plemeno": request.form.get("plemeno", ""),
            "barva": request.form.get("barva", ""),
            "kresba": request.form.get("kresba", ""),
            "chovatel": request.form.get("chovatel", ""),
            "bydliste": request.form.get("bydliste", ""),
            "exterierove_vady": request.form.get("exterierove_vady", ""),
            "exterierove_prednosti": request.form.get("exterierove_prednosti", ""),
            "cil_slechteni": request.form.get("cil_slechteni", ""),
            "povahove_vlastnosti": request.form.get("povahove_vlastnosti", ""),
        }

        try:
            db = get_db()
            db.run("CREATE (p:Pigeon $data )", data=holub_data)

            # check of matka
            # check if otec
            # check if matka in db
            # if not matka in db -> create matka
            # match holub, matka matka:Pigeon-[:MATKA]->holub:Pigeon
        except Neo4jError:
            return render_template("add_pigeon.html", add_pigeon_success=False, error="Data nebyla uložena.")

        return  render_template("add_pigeon.html", add_pigeon_success=True)


@app.route('/edit-pigeon')
def edit_pigeon():
    ...


@app.route('/pigeon-detail/<pigeonID>')
def pigeon_detail(pigeonID):
    db= get_db()
    q = "MATCH (a:Pigeon) "\
        "WHERE a.id = $id "\
        "RETURN a AS pigeon"
    result = db.run(q, id=pigeonID)
    data = result.data()[0]["pigeon"]
    return render_template("pigeon_detail.html", data=data)


@app.route("/my-pigeons")
def my_pigeons():
    db = get_db()
    q = "MATCH (a:Pigeon) " \
        "RETURN a AS pigeon"
    result = db.run(q)
    data = result.data()
    return render_template("pigeon_list.html", data=data)

@app.route('/pigeon-pedigree')
def pigeon_pedigree():
    ...


@app.route('/pigeon-pedigree-download')
def pigeon_pedigree_download():
    ...


if __name__ == '__main__':
    app.run()
