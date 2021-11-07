from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name , last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        User.first_name = data['first_name']
        User.email = data['email']
        return connectToMySQL('login_registration').query_db( query, data )


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_registration').query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        else:
            for fname in result:
                firstname = fname.get('first_name')
                User.first_name = firstname
        return cls(result[0])


    @classmethod
    def get_name(cls):
        print(User.first_name)
        my_email = User.email
        query = "SELECT first_name FROM users WHERE email = '" + my_email + "';"
        results = connectToMySQL('login_registration').query_db(query)
        print(results)
        for fname in results:
            firstname = fname.get('first_name')
            email =fname.get('email')
            User.email = email
            User.first_name = firstname
        return firstname


    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("first name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("last name must be at least 3 characters.")
            is_valid = False
        if len(user['email']) < 5:
            flash("email must be at least 5 characters.")
            is_valid = False
        if len(user['password']) < 6:
            flash("password must be at least 6 characters.")
            is_valid = False
        return is_valid