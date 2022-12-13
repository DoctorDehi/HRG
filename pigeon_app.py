from enum import Enum

from flask import Blueprint, render_template, request, g, send_file, redirect, url_for
from neo4j.exceptions import Neo4jError
from db_conf import driver
import tempfile
from exceptions import *

pigeon_app = Blueprint('pigeon_app', __name__, template_folder='templates')


def get_db():
    if 'db' not in g:
        g.neo4j_db = driver.session()

    return g.neo4j_db


class PigeonGender:
    HOLUB = {
        "marking": "1.0",
        "assoc_relationship": "OTEC"
    }
    HOLUBICE = {
        "marking": "0.1",
        "assoc_relationship": "MATKA"
    }

def cislo_krouzku_full_from_id(pigeonID):
    parts = pigeonID.split("-")
    if len(parts)!=3:
        raise WrongPigeonIdFormat(pigeonID)
    return parts[1] + "/" + parts[2]

def split_pigeon_id(pigeonID):
    parts = pigeonID.split('-')
    if len(parts)!=3:
        raise WrongPigeonIdFormat(pigeonID)
    return parts

def add_parent(parent_id, pigeon_id, gender):
    db = get_db()
    result = db.run('MATCH (a:Pigeon) WHERE a.id = $id RETURN a AS pigeon', id=parent_id)
    parent_data = result.data()
    if len(parent_data) == 1:
        if parent_data[0].get('pigeon').get("pohlavi") != gender["marking"]:
            raise WrongPigeonGenderExcetion(gender["assoc_relationship"], parent_data[0].get('pigeon').get("pohlavi"))
    # parent isnt in db yet
    else:
        user_id, cislo_krouzku, rocnik = split_pigeon_id(parent_id)
        data = {
            'id': parent_id,
            'pohlavi': gender["marking"],
            'cislo_krouzku': cislo_krouzku,
            'rocnik': rocnik
        }
        db.run('CREATE (p:Pigeon $data )', data=data)


    relationship = gender["assoc_relationship"]
    q = f"""MATCH
            (a:Pigeon),
            (b:Pigeon)
            WHERE a.id = $parent_id AND b.id = $pigeon_id
            CREATE (a)-[r:{relationship}]->(b)
        """
    db.run(q, parent_id=parent_id, pigeon_id=pigeon_id)

# def add_matka(matka_id, holub_id):
#     db = get_db()
#     result = db.run('MATCH (a:Pigeon) WHERE a.id = $id RETURN a AS pigeon', id=matka_id)
#     data = result.data()
#     if len(data) == 1:
#         if data[0].get('pigeon').get("pohlavi") == '1.0':
#             raise WrongPigeonGenderExcetion('matky', '1.0')
#     else:
#         a = matka_id.split('-')
#         data = {
#             'id': matka_id,
#             'pohlavi': '0.1',
#             'cislo_krouzku': a[1],
#             'rocnik': a[2]
#         }
#         db.run('CREATE (p:Pigeon $data )', data=data)
#
#     q = """MATCH
#             (a:Pigeon),
#             (b:Pigeon)
#             WHERE a.id = $matka_id AND b.id = $holub_id
#             CREATE (a)-[r:MATKA]->(b)
#         """
#     db.run(q, matka_id=matka_id, holub_id=holub_id)
#
# def add_otec(otec_id, holub_id):
#     db = get_db()
#     result = db.run('MATCH (a:Pigeon) WHERE a.id = $id RETURN a AS pigeon', id=otec_id)
#     data = result.data()
#     if len(data) == 1:
#         if data[0].get("pigeon").get('pohlavi') == '0.1':
#             raise WrongPigeonGenderExcetion('otce', '0.1')
#     else:
#         a = otec_id.split('-')
#         data = {
#             'id': otec_id,
#             'pohlavi': '1.0',
#             'cislo_krouzku': a[1],
#             'rocnik': a[2]
#         }
#         db.run('CREATE (p:Pigeon $data )', data=data)
#
#     q = """MATCH
#             (a:Pigeon),
#             (b:Pigeon)
#             WHERE a.id = $otec_id AND b.id = $holub_id
#             CREATE (a)-[r:OTEC]->(b)
#         """
#     db.run(q, otec_id=otec_id, holub_id=holub_id)
#

def get_holub_data_from_form(form):
    data = {
        "pohlavi": form.get("pohlavi", ""),
        "plemeno": form.get("plemeno", ""),
        "barva": form.get("barva", ""),
        "kresba": form.get("kresba", ""),
        "chovatel": form.get("chovatel", ""),
        "bydliste": form.get("bydliste", ""),
        "exterierove_vady": form.get("exterierove_vady", ""),
        "exterierove_prednosti": form.get("exterierove_prednosti", ""),
        "cil_slechteni": form.get("cil_slechteni", ""),
        "povahove_vlastnosti": form.get("povahove_vlastnosti", ""),
    }
    return data


@pigeon_app.route('/')
def index():
    return render_template('index.html')


@pigeon_app.route('/add-pigeon', methods=['GET', 'POST'])
def add_pigeon():
    if request.method == "GET":
        return render_template("add_pigeon.html")
    else:
        cislo_krouzku_full = request.form.get("cislo_krouzku", "")
        if not cislo_krouzku_full:
            return render_template("add_pigeon.html", add_pigeon_success=False, error="Nebylo zadáno číslo kroužku! Data nebyla uložena")

        cislo_krouzku, rocnik = cislo_krouzku_full.split("/")
        user_id = 1

        holub_id = str(user_id) + "-" + str(cislo_krouzku) + "-" + str(rocnik)

        # zkountrolovat zda holub id není v db
        db = get_db()
        result = db.run('MATCH (a:Pigeon) WHERE a.id = $id RETURN a AS pigeon', id=holub_id)
        # holub je v db, neukladej
        if len(result.data()) > 0:
            return render_template("add_pigeon.html", add_pigeon_success=False,
                                   error="Holub s tímto kroužkem již v databázi je! Data nebyla uložena.")

        holub_data = {
        "id": holub_id,
        "cislo_krouzku": cislo_krouzku,
        "rocnik": rocnik,
        }
        holub_data.update(get_holub_data_from_form(request.form))

        try:
            db.run("CREATE (p:Pigeon $data )", data=holub_data)

        except Neo4jError:
            return render_template("add_pigeon.html", add_pigeon_success=False, error="Data nebyla uložena.")

        error = ""
        # add matka
        cislo_krouzku_matka_full = request.form.get("matka", "")
        if cislo_krouzku_matka_full:
            cislo_krouzku_matka, rocnik_matka = cislo_krouzku_matka_full.split('/')
            matka_id = str(user_id) + "-" + str(cislo_krouzku_matka) + "-" + str(rocnik_matka)
            try:
                add_parent(parent_id=matka_id, pigeon_id=holub_id, gender=PigeonGender.HOLUBICE)
            except WrongPigeonGenderExcetion as e:
                error = error + e.message + " "
            except Neo4jError as e:
                error = error + "Informace o matce nebyla uložena. "
                error = error + e.message

        # add otec
        cislo_krouzku_otec_full = request.form.get("otec", "")
        if cislo_krouzku_otec_full:
            cislo_krouzku_otec, rocnik_otec = cislo_krouzku_otec_full.split('/')
            otec_id = str(user_id) + "-" + str(cislo_krouzku_otec) + "-" + str(rocnik_otec)
            try:
                add_parent(parent_id=otec_id, pigeon_id=holub_id, gender=PigeonGender.HOLUB)
            except WrongPigeonGenderExcetion as e:
                error = error + e.message + " "
            except Neo4jError as e:
                error = error + "Informace o otci nebyla uložena. "


        return  render_template("add_pigeon.html", add_pigeon_success=True, error=error)


@pigeon_app.route('/edit-pigeon/<pigeonID>', methods=['GET', 'POST'])
def edit_pigeon(pigeonID):
    db = get_db()
    q = "MATCH (a:Pigeon) " \
        "WHERE a.id = $id " \
        "RETURN a AS pigeon"
    result = db.run(q, id=pigeonID)
    pigeon = result.data()[0]["pigeon"]

    if request.method == "POST":
        holub_data = get_holub_data_from_form(request.form)
        # pokud se změní pohlaví, rozvázat vztah s případnými potomky
        if holub_data['pohlavi'] != pigeon['pohlavi']:
            ...
        # pokud se změní matka či otec, rozvázat vztah s původním a přidat nový
        return "Zatím neimplementováno, změny nebyly uloženy.."
    else:
        # pridat do dat krouzky matky a otce
        return render_template("edit_pigeon.html", data=pigeon)

@pigeon_app.route('/delete-pigeon/<pigeonID>', methods=['GET', 'POST'])
def delete_pigeon(pigeonID):
    if request.method == "POST":
        # mazání z db
        return redirect(url_for("pigeon_app.my_pigeons"))
    else:
        krouzek = pigeonID.split('-')[1:].join('/')
        return render_template("delete_pigeon.html", pigeon_krouzek=krouzek, pigeonID = pigeonID)


@pigeon_app.route('/pigeon-detail/<pigeonID>')
def pigeon_detail(pigeonID):
    db= get_db()
    q = "MATCH (a:Pigeon) "\
        "WHERE a.id = $id "\
        "RETURN a AS pigeon"
    result = db.run(q, id=pigeonID)
    data = result.data()[0]["pigeon"]
    return render_template("pigeon_detail.html", data=data)


@pigeon_app.route("/my-pigeons")
def my_pigeons():
    db = get_db()
    q = "MATCH (a:Pigeon) " \
        "RETURN a AS pigeon"
    result = db.run(q)
    data = result.data()
    return render_template("pigeon_list.html", data=data)


# noinspection PyPep8Naming
@pigeon_app.route('/pigeon-pedigree-visualizastion/<pigeonID>')
def pigeon_visualise_pedigree(pigeonID):
    cislo_krouzku = cislo_krouzku_full_from_id(pigeonID)
    return render_template("visualize_pedigree.html", cislo_krouzku=cislo_krouzku)


@pigeon_app.route('/pigeon-pedigree-download')
def pigeon_pedigree_download():
    # asi redirect
    return "Zatím neimplementováno"

@pigeon_app.route('/test/rodokmen.pdf')
def test():
    tmp = tempfile.TemporaryFile()
    # tmp.write(b'some content')
    # tmp.seek(0)
    from pdf_gen import pdf_gen_test
    output = pdf_gen_test.gen_test()
    output.write_stream(tmp)
    output.write(tmp)
    tmp.seek(0)
    return send_file(tmp, download_name="rodokmen.pdf")

@pigeon_app.route('/test')
def test2():
    add_parent(parent_id='1-AT514-20', pigeon_id="1-TE234-13", gender=PigeonGender.HOLUBICE)
    return 'ok'


