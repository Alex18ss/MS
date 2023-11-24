from flask import Flask, request, redirect, render_template, make_response
from werkzeug.exceptions import BadRequestKeyError
from databases.database import db

app = Flask(__name__)


def setcookie():
    try:
        if db.in_db(request.form["login"]):
            res = make_response(render_template("example.html"))
            res.set_cookie('logged', 'yes', 1296000)
            return res
        else:
            return redirect('/register')
    except BadRequestKeyError:
        return redirect('/register')


@app.route("/register")
def register():
    if request.cookies.get('logged'):
        return redirect("/main_page")
    return render_template('register.html')


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if request.cookies.get('logged'):
        return render_template('example.html')
    try:
        if not db.in_db(request.form["login"]):
            db.insert_user(request.form["login"], request.form["password"])
            return setcookie()
        else:
            if db.check_password(request.form["login"], request.form["password"]):
                return setcookie()
            else:
                return redirect('/register')
    except BadRequestKeyError:
        return redirect('/register')
