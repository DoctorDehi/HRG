import tempfile
from urllib.parse import unquote

from flask import Blueprint, render_template, request, g, send_file, redirect, url_for, jsonify
from neo4j.exceptions import Neo4jError

from db_conf import driver
from exceptions import *
from neo_interface import NeoInterface
from utils import pigeon_id_from_cislo_krouzku_full, cislo_krouzku_full_from_id, split_pigeon_id, PigeonGender
from pdf_gen.pdf_generator import PedigreePDFGenerator

pigeon_app = Blueprint('pigeon_app', __name__, template_folder='templates')


def get_db():
    if 'db' not in g:
        g.neo4j_db = driver.session()

    return g.neo4j_db


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

        user_id = 1
        pigeon_id = pigeon_id_from_cislo_krouzku_full(cislo_krouzku_full, user_id)
        cislo_krouzku, rocnik = cislo_krouzku_full.split('/')

        # zkountrolovat zda holub id není v db
        db = get_db()
        existing_pigeon = NeoInterface.get_pigeon_by_id(db, pigeon_id)
        # holub je v db, neukladej
        if existing_pigeon:
            return render_template("add_pigeon.html", add_pigeon_success=False,
                                   error="Holub s tímto kroužkem již v databázi je! Data nebyla uložena.")

        holub_data = {
        "id": pigeon_id,
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
        if request.form.get("matka", ""):
            mother_id = pigeon_id_from_cislo_krouzku_full(request.form.get("matka", ""), user_id)
            try:
                NeoInterface.add_parent(db, pigeon_id=pigeon_id, parent_id=mother_id,
                                        parent_gender=PigeonGender.HOLUBICE)
            except WrongPigeonGenderExcetion as e:
                error = error + e.message + " "
            except Neo4jError:
                error = error + "Informace o matce nebyla uložena. "

        # add otec
        if request.form.get("otec", ""):
            father_id = pigeon_id_from_cislo_krouzku_full(request.form.get("otec", ""), user_id)
            try:
                NeoInterface.add_parent(db, pigeon_id=pigeon_id, parent_id=father_id, parent_gender=PigeonGender.HOLUB)
            except WrongPigeonGenderExcetion as e:
                error = error + e.message + " "
            except Neo4jError:
                error = error + "Informace o otci nebyla uložena. "

        return  render_template("add_pigeon.html", add_pigeon_success=True, error=error)


@pigeon_app.route('/edit-pigeon/<pigeonID>', methods=['GET', 'POST'])
def edit_pigeon(pigeonID):
    db = get_db()
    old_pigeon = NeoInterface.get_pigeon_by_id(db, pigeon_id=pigeonID)
    mother = NeoInterface.get_mother_of_pigeon(db ,pigeon_id=pigeonID)
    father = NeoInterface.get_father_of_pigeon(db ,pigeon_id=pigeonID)

    if request.method == "POST":
        new_pigeon_data = get_holub_data_from_form(request.form)
        # pokud se změní pohlaví, rozvázat vztah s případnými potomky
        if new_pigeon_data['pohlavi'] != old_pigeon['pohlavi']:
            r_label = PigeonGender.get_gender_from_marking(old_pigeon['pohlavi'])["assoc_relationship"]
            db.run(f"MATCH (p:Pigeon {{id: '{pigeonID}' }}), (p)-[r:{r_label}]->(:Pigeon) DELETE r")

        new_father_ckf = request.form.get('otec')
        new_mother_ckf = request.form.get('matka')
        NeoInterface.update_parent(db, 1, pigeon_id=pigeonID,
                                   db_parent=father,
                                   form_parent_ckf=new_father_ckf,
                                   parent_gender=PigeonGender.HOLUB)
        NeoInterface.update_parent(db, 1, pigeon_id=pigeonID,
                                   db_parent=mother,
                                   form_parent_ckf=new_mother_ckf,
                                   parent_gender=PigeonGender.HOLUBICE)

        NeoInterface.update_pigeon_data(db ,pigeon_id=pigeonID, pigeon_data=new_pigeon_data)

        data = new_pigeon_data.copy()
        data['cislo_krouzku'] = old_pigeon.get('cislo_krouzku')
        data['rocnik'] = old_pigeon.get('rocnik')
        data["otec"] = new_father_ckf
        data["matka"] = new_mother_ckf


        return render_template("edit_pigeon.html", data=data, edit_pigeon_success=True)

    # method == GET
    else:
        # pridat do dat krouzky matky a otce
        data = old_pigeon.copy()
        if father:
            data["otec"] = cislo_krouzku_full_from_id(father["id"])
        if mother:
            data["matka"] = cislo_krouzku_full_from_id(mother["id"])
        return render_template("edit_pigeon.html", data=data)

@pigeon_app.route('/delete-pigeon/<pigeonID>', methods=['GET', 'POST'])
def delete_pigeon(pigeonID):
    if request.method == "POST":
        # mazání z db
        db = get_db()
        db.run("MATCH (p:Pigeon {id: $pigeonID}) DELETE p", pigeonID=pigeonID)
        return redirect(url_for("pigeon_app.my_pigeons"))
    else:
        krouzek = cislo_krouzku_full_from_id(pigeonID)
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


@pigeon_app.route('/pigeon-pedigree-download/<pigeonID>')
def pigeon_pedigree_download(pigeonID):
    # asi redirect
    parts = split_pigeon_id(pigeonID)
    filename = f"Rodokmen_{parts[1]}%2F{parts[2]}.pdf"
    return redirect(url_for("pigeon_app.generate_pedigree", pigeonID=pigeonID, filename=filename))

@pigeon_app.route("/pigeon-pedigree-download/<pigeonID>/<filename>")
def generate_pedigree(pigeonID, filename):
    filename = unquote(filename)
    pdf_gen = PedigreePDFGenerator()
    tmp = tempfile.TemporaryFile()
    db = get_db()
    paths = NeoInterface.get_ancestor_paths(db, pigeonID)
    pdf =  pdf_gen.generate_pedigree_from_paths(paths, tmp)
    return send_file(pdf, download_name=filename)
    # return f"Test: {pigeonID, filename}"


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
    db = get_db()
    a = NeoInterface.get_ancestor_paths(db, pigeon_id="1-TE254-21")
    # a = NeoInterface.remove_parent(db, parent_id='1-TE254-21', pigeon_id='1-AY424-21',  parent_gender=PigeonGender.HOLUB)
    # return jsonify(a)
    return jsonify(a)
