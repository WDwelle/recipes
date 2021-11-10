from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    if not User.validate_user(request.form):
        return redirect("/")
    else:
        User.save(data)
        return redirect('/welcome')


@app.route("/check", methods = ["POST"])
def check():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return render_template("/welcome.html", one_user = User.first_name)


@app.route("/welcome")
def welcome():
    User.get_name()
    print(User.first_name)
    return render_template("welcome.html", one_user = User.first_name)


@app.route("/clear")
def clear():
    User.first_name = ''
    User.last_name = ''
    User.email = ''
    User.password = ''
    return redirect("/")