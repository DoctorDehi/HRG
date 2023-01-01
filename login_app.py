from flask import Blueprint, render_template, request, g, redirect, jsonify
from db_conf import  neo_driver, mongo_engine, User
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


login_app = Blueprint('login_app', __name__, template_folder='templates/login')

# setting up login manager and specifying login view page
login_manager = LoginManager()

def get_neo4j_db():
    if 'db' not in g:
        g.neo4j_db = neo_driver.session()

    return g.neo4j_db

def get_mongo_db():
    if 'mongodb' not in g:
        g.mongo_db = mongo_engine.session()

    return g.mongo_db

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


@login_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        # get credentials
        email = request.form["email"]
        password = request.form["password"]

        # find corresponding user
        user_trying_to_log_in = User.objects(email=email).first()

        if user_trying_to_log_in is None:
            return render_template('login_page.html', login_error="Uživatel s touto emailovou adresou není registrován")

        password_hash = user_trying_to_log_in.get_password_hash()

        # check credentials
        if user_trying_to_log_in.is_active and check_password_hash(pwhash=password_hash, password=password):
            login_user(user_trying_to_log_in)
            return redirect('/')
        else:
            return render_template('login_page.html', login_error="Nesprávné přihlašovací údaje")
    else:
        return render_template('login_page.html')

@login_app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect('/login')

@login_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        email = request.form["email"]
        
        user_uniqueness_check = User.objects(email=email).first()
        if user_uniqueness_check:
            return render_template('registration_page.html', login_error="Uživatel s touto emailovou adresou je již zaregistrovaný")
        
        password = request.form["password"]
        password_again = request.form["password_again"]

        if password == password_again:

            password_hash = generate_password_hash(password=password, method="pbkdf2:sha512")
            new_user = User(email=email, password=password_hash)
            new_user.save()
            login_user(new_user)
            return redirect('/my-pigeons')

        else:
            return render_template('registration_page.html', login_error="Zadaná hesla se neshodují")

    else:
        return render_template('registration_page.html')

@login_app.route("/ltest")
def test():
    return jsonify(User.objects.all())
