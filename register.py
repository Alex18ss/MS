from flask import *  # подключили библиотеку flask
# from flask_login import *
from werkzeug.exceptions import BadRequestKeyError
from database import *
app = Flask(__name__) # создали фласк приложение(веб-сервер)

global session

def setcookie(userlogin):
    try:
        if db.in_db(request.form["login"]):
            res = make_response(render_template("example.html"))
            session = db.get_session(userlogin)
            res.set_cookie('session', session, 1296000)
            return res
        else:
            return redirect('/register')
    except BadRequestKeyError:
        return redirect('/register')


@app.route("/register")
def register():
    if request.cookies.get('session') and request.cookies.get('session') == session:
        return redirect("/main_page")
    return render_template('register.html')


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if request.cookies.get('session') and request.cookies.get('session') == session:
        return render_template('example.html')
    try:
        if not db.in_db(request.form["login"]):
            db.insert_user(request.form["login"], request.form["password"])
            return setcookie(request.form["login"])
        else:
            if db.check_password(request.form["login"], request.form["password"]):
                return setcookie(request.form["login"])
            else:
                return redirect('/register')
    except BadRequestKeyError:
        return redirect('/register')


if __name__ == '__main__':
    db = BerestaDatabase("databases/data_beresta.db")
    db.recreate_table()
    app.run(debug=True, port=12289, threaded=True)
