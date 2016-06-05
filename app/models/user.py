""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class user(Model):
    def __init__(self):
        super(user, self).__init__()

    def register(self, registration_info):
            regis_errors = []
            if not registration_info['name']:
                regis_errors.append('Name cannot be blank')
            elif len(registration_info['name']) < 2:
                regis_errors.append('Name must be at least 2 characters long')
            if not registration_info['email']:
                regis_errors.append('Email cannot be blank')
            if not registration_info['password']:
                regis_errors.append('Password cannot be blank')
            if not registration_info['pw_confirmation']:
                regis_errors.append('Password confirmation cannot be blank')
            elif len(registration_info['password'])< 8:
                regis_errors.append('Password must be at least 8 characters')
            elif registration_info['password'] != registration_info['pw_confirmation']:
                regis_errors.append('Passwords do not match!')
            if not registration_info['datebirth']:
                regis_errors.append('Date of Birth cannot be blank')

            if regis_errors:
                return{'status': False, 'regis_errors': regis_errors}

            else:

                password = registration_info['password']
                pw_hash = self.bcrypt.generate_password_hash(password)
                query = "INSERT INTO users (name, email, password, datebirth) VALUES (:name, :email, :password, :datebirth)"
                data = {
                    'name': registration_info['name'], 
                    'email': registration_info['email'], 
                    'password' : pw_hash,
                    'datebirth': registration_info['datebirth']
                }

                self.db.query_db(query, data)
                get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
                users = self.db.query_db(get_user_query)
                return{'status': True, 'user':users[0]}

    def login(self, login_info):
        login_errors = []
        if not login_info['emailcheck']:
            login_errors.append('username cannot be blank')
        if not login_info['passwordcheck']:
            login_errors.append('password cannot be blank')
        if login_errors:
            return {'status': False, 'login_errors': login_errors}

        else:
            password = login_info['passwordcheck']
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = {'email': login_info['emailcheck']}
            user = self.db.query_db(query, data)
            if user and self.bcrypt.check_password_hash(user[0]['password'], password):
                id = user[0]['id']
                name = user[0]['name']
                return{'status': True, 'name': name, 'id': id}
            else:
                login_errors.append("Invalid login. Username or password doesnt match our database")
                return {"status": False, "login_errors": login_errors}

    def get_user(self, friend_id, user_id):
        print id
        query = "SELECT name, email FROM users where id = :friend_id"
        data = {'friend_id': friend_id }
        return self.db.get_one(query, data)