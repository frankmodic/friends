
from system.core.model import Model
from time import strftime

class friend(Model):
	def __init__(self):
		super(friend, self).__init__()


	def addfriend(self, friend_info, user_id):

		add_errors = []

		if not friend_info['name']:
			add_errors.append('Please give the friend a name')
		if len(friend_info['name']) < 4:
			add_errors.append('Must be at least 3 characters long')

		if add_errors:
			return {'status': False, 'add_errors': add_errors}

		else:
			time = strftime('%B %d, %Y, %T')
			query = "INSERT INTO friends (name, dateadded, user_id) VALUES (:name, NOW(), :user_id)"
			data = {
				'name': friend_info['name'], 
				'dateadded': time,
				'user_id': user_id
				}
			self.db.query_db(query, data)

			return {'status': True}

	def display(self, user_id):
		query = "SELECT friends.id, friends.user_id, friends.name as friend_name, users.name as user_name, friends.dateadded as friend_date FROM friends JOIN users ON friends.user_id = users.id WHERE user_id = :user_id OR friends.id IN (SELECT friend_id FROM friendslist WHERE user_id = :user_id)"
		data = { 'user_id': user_id}
		return self.db.query_db(query, data)

	def displayothers(self, user_id):
		query = "SELECT id, users.name as friend_name FROM users"
		# query = "SELECT friends.id as id, friends.user_id as user_id, friends.name as friend_name, users.name as user_name FROM friends JOIN users ON friends.user_id = users.id WHERE user_id != :user_id AND friends.id not in (SELECT friend_id from friendslist WHERE user_id = :user_id)"
		data = { 'user_id': user_id}
		return self.db.query_db(query, data)

	def delete(self, friend_id):
		query = "DELETE FROM friends WHERE friend_id = :friend_id"
		data = {'friend_id': friend_id}
		return self.db.query_db(query, data)

	def addtofriendslist(self, friend_id, user_id):
		query = "INSERT INTO friendslist (user_id, friend_id) VALUES (:user_id, :friend_id)"
		data = {
				'user_id': user_id,
				'friend_id': friend_id
			}
		return self.db.query_db(query, data)

	def displayfriendslist(self, user_id):
		query = "SELECT friends.name as friend_name, users.name as user_name, friends.dateadded as friend_date FROM friends JOIN users ON friends.user_id = users.id"
		data = {'user_id': user_id}

		return self.db.query_db(query, data)

	def remove(self, friend_id, user_id):
		query = "DELETE FROM friendslist WHERE friend_id = :friend_id AND user_id = :user_id"
		data = {'user_id': user_id, 'friend_id': friend_id}

		return self.db.query_db(query, data)

	def show(self, friend_id, user_id):
		query = "SELECT users.name as name, friends.name as friend_name FROM users JOIN friends ON users.id = friends.user_id WHERE friends.id = :friend_id"
		data = {'friend_id': friend_id}

		return self.db.query_db(query, data)

	def show2(self, friend_id, user_id):
		query = "SELECT friendslist.user_id, users.name FROM friendslist LEFT JOIN users ON friendslist.user_id=users.id WHERE friend_id = :friend_id"
		data = {'friend_id': friend_id}

		return self.db.query_db(query, data)