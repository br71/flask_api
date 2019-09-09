import os
import yaml
from flask import Flask, jsonify, escape, render_template, request, abort
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)

with open("db.yaml", 'r') as s:
    db = yaml.safe_load(s)

app.config['MYSQL_DATABASE_HOST'] = db['mysql_host']
app.config['MYSQL_DATABASE_USER'] = db['mysql_user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DATABASE_DB'] = db['mysql_db']

app.config['SECRET_KEY'] = os.urandom(24)


mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)


@app.route('/')
def hello():
    cursor = mysql.get_db().cursor()
    sql = "select * from actor"
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


@app.route('/actors/')
def actors():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "select * from actor"
        cursor.execute(sql)
        rows = cursor.fetchmany(50)
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/actor/<int:id_>', methods=["GET"])
def actor(id_):
    id_ = escape(id_)
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM actor WHERE actor_id={}".format(id_))
        row = cursor.fetchmany(50)
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/add_actor', methods=['POST'])
def addactor():

    try:
        d = request.get_json()
        fn = d["first_name"]
        ln = d["last_name"]

        sql = "INSERT INTO actor (`first_name`, `last_name`) VALUES('{}','{}')".format(fn, ln)
        print(sql)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update_actor/<int:_id>', methods=['PUT'])
def update_actor(_id):
    _id = escape(_id)

    d = request.get_json()
    ln = d["last_name"]

    try:
        sql = "UPDATE actor SET last_name = '{}' WHERE actor_id={}".format(ln, _id)
        print(sql)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        resp = jsonify('User modified successfully!')
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete_actor/<int:_id>', methods=['DELETE'])
def delete_actor(_id):

    _id = escape(_id)

    try:
        sql = "DELETE FROM actor WHERE actor_id={}".format(_id)
        print(sql)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/bootstrap')
def bootstrap():
    return render_template('bootstrap.html')


@app.route('/form')
def form():
    return render_template('form.html')


if __name__ == '__main__':
    app.run()

