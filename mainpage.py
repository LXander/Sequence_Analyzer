
import os
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
import example_builder,search_region,name_load
import json,requests,forms,random

from flask_wtf.csrf import  CsrfProtect

csrf = CsrfProtect()

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE = os.path.join(app.root_path,'Sequence_Analyzer.db'),
    SECRET_KEY = 'test key',
    USERNAME = 'lxander',
    PASSWORD = 'password'
))
app.config.from_envvar('FDA_SETTINGS',silent = True)
csrf.init_app(app)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql',mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def data_load():
    db = get_db()
    builder = example_builder.builder()
    for _ in range(100):
        example = builder.build_example()

        db.execute('insert into resource(json) values(?)',
                   [example])
    db.commit()

def gene_data_creater(geneDict):
    db = get_db()
    builder = example_builder.builder(geneDict)
    for _ in range(random.randint(3,15)):
        example = builder.build_example()
        db.execute('insert into genedata(json) values(?)',
                   [example])
    db.commit()

def gene_db_creater():
    db = get_db()
    db.execute('drop table if exists genedata;')
    db.execute("create table genedata(id integer primary key autoincrement,'json' varchar not null);")
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    name_load()
    print ("Initialized the database")



@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/db_test')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html',entries = entries)


@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title,text) values (?,?)',
               [request.form['title'],request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/resource',methods=['GET','POST'])
def resource_list():
    db = get_db()
    cur = db.execute('select id from resource')
    ids = cur.fetchall()
    return render_template('resource_list.html', ids=ids)

@app.route('/resource/<int:id>',methods=['GET','POST'])
def resource_page(id):
    form = forms.CompareFoem()
    if form.validate_on_submit():

        print ("validate")
        print (form.MultipleSequence.data)
        warp = {}
        warp['method'] = form.methods.data
        warp['standard_sequence'] = form.MultipleSequence.data
        db = get_db()
        cur = db.execute('select * from resource where id = (?)',[id])
        resource = cur.fetchone()
        if resource:
            res =  json.loads(resource['json'])
            warp['variant'] = res['variant']
            warp['referenceSeq'] = res['referenceSeq']
            quality = requests.post('http://127.0.0.1:8388/get_quality', json=warp)
            print (quality.text)
            return render_template('resource_quality.html',quality = quality)


    print ("invalidate")
    db = get_db()
    cur = db.execute('select * from resource where id = (?)',[id])
    resource = cur.fetchone()
    if resource:
        return render_template('resource_detail.html',resource = resource,form=form,dumps = json.dumps,loads = json.loads)
    return abort(404)

@app.route('/request_quality/<int:id>',methods=['GET','POST'])
def quality(id):
    db = get_db()
    cur = db.execute('select * from resource where id = (?)',[id])
    resource = cur.fetchone()
    if resource:

        print (resource['json'])


        quality = requests.post('http://127.0.0.1:8388/get_quality',json = resource['json'])
        return render_template('resource_quality.html',quality = quality)
    return 'hello world'

@app.route('/sequence/<int:id>',methods=['GET','POST'])
def sequence_page(id):
    form = forms.CompareFoem()
    if form.validate_on_submit():

        print("validate")
        print(form.MultipleSequence.data)
        warp = {}
        warp['method'] = form.methods.data
        warp['standard_sequence'] = form.MultipleSequence.data
        db = get_db()
        cur = db.execute('select * from genedata where id = (?)', [id])
        resource = cur.fetchone()
        if resource:
            res = json.loads(resource['json'])
            warp['variant'] = res['variant']
            warp['referenceSeq'] = res['referenceSeq']
            quality = requests.post('http://127.0.0.1:8388/get_quality', json=warp)
            return render_template('resource_quality.html', quality=quality)

    print("invalidate")
    db = get_db()
    cur = db.execute('select * from genedata where id = (?)', [id])
    resource = cur.fetchone()
    if resource:
        return render_template('resource_detail.html', resource=resource, form=form, dumps=json.dumps, loads=json.loads)
    return abort(404)

@app.route('/search',methods=['GET','POST'])
def search():
    geneName = name_load.get_gene_name()
    form = forms.SearchForm()
    if form.validate_on_submit():

        gene_db_creater()
        geneDicts = search_region.get_geneDicts(form.GeneName.data)
        gene_data_creater(geneDicts[0])

        db = get_db()
        cur = db.execute('select * from genedata;')
        genes = cur.fetchall()
        geneData = {}
        for gene in genes:
            geneData[gene['id']] = json.loads(gene['json'])
        ids = [gene['id'] for gene in genes]
        print (ids)
        return render_template('gene_resource_list.html',ids=ids)



    return render_template('search.html',form=form,geneName = geneName)


@app.route('/comparision/<int:id>',methods=['GET','POST'])
def compare(id):
    db = get_db()
    cur = db.execute('select * from resource where id = (?)',[id])
    resource = cur.fetchone()



@app.route('/uitest',methods=['GET','POST'])
def ui_test():
    return render_template('banner.html')


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash("You are logged in")
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    app.run(debug=True,port=8288)
