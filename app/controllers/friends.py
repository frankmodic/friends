"""
	Sample Controller File
	A Controller should be in charge of responding to a request.
	Load models to interact with the database and load views to render them to the client.
	Create a controller using this template
"""
from system.core.controller import *

class friends(Controller):
	def __init__(self, action):
		super(friends, self).__init__(action)
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
	def dashboard(self):
		user_id = session['id']

		all_friends = self.models['friend'].display(user_id)

		displayothers = self.models['friend'].displayothers(user_id)
		displayfriendslist = self.models['friend'].displayfriendslist(user_id)

		return self.load_view('dashboard.html', all_friends = all_friends, displayothers = displayothers, displayfriendslist = displayfriendslist, user_id = user_id)


	def delete(self, id):
		friend_id = id
		delete_friend = self.models['friend'].delete(friend_id)
		return redirect ('dashboard')

	def friendslist(self, id):
		friend_id = id
		user_id = session['id']
		# user = self.models['user'].get_user(friend_id, user_id)
		# print user
		# friend_name = user['name']
		addtowishlist = self.models['friend'].addtofriendslist(friend_id, user_id)
		return redirect ('dashboard')

	def remove(self, id):
		friend_id = id
		user_id = session['id']
		remove = self.models['friend'].remove(friend_id, user_id)
		return redirect ('dashboard')

	def show(self, id):
		friend_id = id
		user_id = session['id']
		one_user = self.models['user'].get_user(friend_id, user_id)

		return self.load_view('show.html', one_user = one_user)