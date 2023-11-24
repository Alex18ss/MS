from flask import *  # подключили библиотеку flask
# from flask_login import *
from werkzeug.exceptions import BadRequestKeyError
from database import *
app = Flask(__name__)
# создали фласк приложение(веб-сервер)


@app.route("/register")
def register():
    if request.cookies.get('logged'):
        return redirect("/main_page")
    return render_template('register.html')


@app.route('/cookie', methods=['GET', 'POST'])
def setcookie():
    try:
        if db.in_db(request.form["login"]):
            resp = make_response()
            resp.set_cookie('logged', 'yes', 1296000)
            redirect("/main_page")
            return resp
        else:
            return redirect('/register')
    except BadRequestKeyError:
        return redirect('/register')


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if request.cookies.get('logged'):
        return render_template('example.html')
    try:
        if request.form["login"] is None:
            return redirect('/register')
        elif not db.in_db(request.form["login"]):
            db.insert_user(request.form["login"], request.form["password"])
            return setcookie()
        else:
            if db.check_password(request.form["login"], request.form["password"]):
                return setcookie()
            else:
                return redirect('/register')
    except BadRequestKeyError:
        return redirect('/register')


if __name__ == '__main__':
    db = BerestaDatabase("databases/beresta_data.db")
    db.recreate_table()
    app.run(debug=True, port=12289)
