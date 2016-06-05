"""
	Sample Controller File

	A Controller should be in charge of responding to a request.
	Load models to interact with the database and load views to render them to the client.

	Create a controller using this template
"""
from system.core.controller import *

class users(Controller):
	def __init__(self, action):
		super(users, self).__init__(action)
		"""
			This is an example of loading a model.
			Every controller has access to the load_model method.
		"""
		self.load_model('user')
		self.load_model('friend')
		self.db = self._app.db

		"""
		
		This is an example of a controller method that will load a view for the client 

		"""
	def index(self):

		return self.load_view('index.html')

	def register(self):
		registration_info = {
			'name': request.form['name'],
			'email': request.form['email'],
			'password': request.form['password'],
			'pw_confirmation': request.form['pw_confirmation'],
			'datebirth': request.form['datebirth']
			}

		create_user = self.models['user'].register(registration_info)
		if create_user['status'] == True:
			if 'id' not in session:
				session['id'] = create_user['user']['id']
			if 'name' not in session:
				session['name'] = create_user['user']['name']

			return redirect('/dashboard')

		else:
			for message in create_user['regis_errors']:
				flash(message, 'regis_errors')
			# redirect to the method that renders the form
			return redirect('/')

	def login(self):
		login_info = {
			'emailcheck': request.form['emailcheck'], 
			'passwordcheck': request.form['passwordcheck']
			}
		login_user = self.models['user'].login(login_info)
		
		if login_user['status'] == True:
				session['id'] = login_user['id'] 
				session['name'] = login_user['name']
				
				return redirect('/dashboard')

		else:
			if login_user['status'] == False:
				for message in login_user['login_errors']:
					flash(message, 'login_errors')
				return redirect('/')

	def logout(self):
		session.clear()
		return redirect('/')


