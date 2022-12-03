from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-pigeon')
def add_pigeon():
    ...


@app.route('/edit-pigeon')
def edit_pigeon():
    ...


@app.route('/pigeon-detail')
def pigeon_detail():
    ...


@app.route('/pigeon-pedigree')
def pigeon_pedigree():
    ...


@app.route('/pigeon-pedigree-download')
def pigeon_pedigree_download():
    ...


if __name__ == '__main__':
    app.run()
