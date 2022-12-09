from flask import Blueprint, render_template, request, g, send_file, redirect, url_for
from db_conf import  driver, mongo_engine


login_app = Blueprint('login_app', __name__, template_folder='templates/login')


def get_neo4j_db():
    if 'db' not in g:
        g.neo4j_db = driver.session()

    return g.neo4j_db

def get_mongo_db():
    if 'mongodb' not in g:
        g.mongo_db = driver.session()

    return g.mongo_db


@login_app.route('/login', methods=['GET', 'POST'])
def login():
    get_mongo_db()
    return render_template('login_page.html')

@login_app.route('/logout')
def logout():
    return "Zatím neimplementováno"

@login_app.route('/register')
def register():
    return "Zatím neimplementováno"
