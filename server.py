from flask_app.controllers import users
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app import __init__


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=80, debug=True)