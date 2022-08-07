
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


class TestFirestoreAdmin:
	movies = {
		'name': 'Iron Man',
		'lead': {'name': 'Robert Downey Jr.'},
		'released': False,
		'year': 2008,
		'rating': 7.9,
		'prequel': None,
		'cast': ['Jon Favreau', 'Gwyneth Paltrow', 'Jeff Bridges', b'J.A.R.V.I.S', 'Terrence Howard']
	}

	def test_manual_doc_set(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').set(self.__class__.movies) is None


class TestFirestoreAuth:
	movies = {
		'name': 'Dr. Strange',
		'lead': {'name': 'Benedict Cumberbatch'},
		'released': False,
		'year': 2016,
		'rating': 7.5,
		'prequel': None,
		'cast': ['Tilda Swinton', 'Rachel McAdams', 'Mads Mikkelsen', 'Chiwetel Ejiofor', 'Benedict Wong']
	}
	user = None

	def test_create_test_user(self, auth):
		user = auth.sign_in_anonymous()
		self.__class__.user = user
		assert user
		assert user.get('idToken')

	def test_manual_doc_set(self, ds):
		assert ds.collection('Marvels').document('Movies').set(self.__class__.movies, token=self.__class__.user.get('idToken')) is None

	def test_delete_test_user(self, auth):
		assert auth.delete_user_account(self.__class__.user.get('idToken'))


class TestFirestore:
	series = {
		'name': 'Moon Knight',
		'lead': {'name': 'Oscar Issac'},
		'released': False,
		'year': 2022,
		'rating': 7.4,
		'prequel': None,
		'cast': ['Ethan Hawke', 'May Calamawy', 'F. Murray Abraham']
	}

	def test_manual_doc_set(self, ds):
		assert ds.collection('Marvels').document('Series').set(self.__class__.series) is None
