from flask import *  # подключили библиотеку flask
# from flask_login import *
from werkzeug.exceptions import BadRequestKeyError
from database import *
app = Flask(__name__)
# создали фласк приложение(веб-сервер)


def remain():
    if request.cookies.get('logged'):
        return redirect("/main_page")
    print("To setcookie -->>")
    return setcookie()


def setcookie():
    try:
        if db.in_db(request.form["login"]):
            res = make_response()
            res.set_cookie('logged', 'yes', 1296000)
            print("To main_page -->>")
            redirect("/main_page")
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
    print("In main page")
    if request.cookies.get('logged'):
        print("Here 1")
        return render_template('example.html')
    try:
        if not db.in_db(request.form["login"]):
            print("Here 2")
            db.insert_user(request.form["login"], request.form["password"])
            print("To remain -->>")
            return remain()
        else:
            if db.check_password(request.form["login"], request.form["password"]):
                print("Here 3")
                return remain()
            else:
                print("Here 4")
                return redirect('/register')
    except BadRequestKeyError:
        print("Here 5")
        return redirect('/register')


if __name__ == '__main__':
    db = BerestaDatabase("databases/test.db")
    db.recreate_table()
    app.run(debug=True, port=12289, threaded=True)
