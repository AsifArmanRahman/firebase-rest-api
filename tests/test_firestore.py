
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


class TestFirestoreAdmin:
	movies1 = {
		'name': 'Iron Man',
		'lead': {'name': 'Robert Downey Jr.'},
		'director': '',
		'released': False,
		'year': 2008,
		'rating': 7.9,
		'prequel': None,
		'cast': ['Jon Favreau', 'Gwyneth Paltrow', 'Jeff Bridges', b'J.A.R.V.I.S', 'Terrence Howard']
	}

	movies2 = {
		'name': 'Thor',
		'lead': {'name': 'Chris Hemsworth'},
		'released': False,
		'year': 2011,
		'rating': 7.0,
		'cast': ['Tom Hiddleston', 'Natalie Portman', 'Anthony Hopkins', 'Jeremy Renner', 'Stellan Skarsgård', 'Idris Elba', 'Kat Dennings']
	}

	auto_doc_id = None

	def test_manual_doc_set(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document('001').set(self.__class__.movies1) is None

	def test_auto_doc_add(self, ds_admin):
		doc_id = ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').add(self.__class__.movies2)
		assert doc_id

		self.__class__.auto_doc_id = doc_id

	def test_manual_doc_get(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document('001').get() == self.__class__.movies1
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document(self.__class__.auto_doc_id).get() == self.__class__.movies2

	def test_collection_get(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').get() == [{'001': self.__class__.movies1}, {self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_collection_list_document(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').list_of_documents() == ['001', self.__class__.auto_doc_id]

	def test_collection_get_start_after(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('rating').start_after({'rating': 7.4}).get() == [{'001': self.__class__.movies1}]
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('rating').start_after({'rating': 6.9}).get() == [{self.__class__.auto_doc_id: self.__class__.movies2}, {'001': self.__class__.movies1}]
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('rating').start_after({'rating': 8.5}).get() == []

	def test_collection_get_start_at(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('rating').start_at({'rating': 7.4}).get() == [{'001': self.__class__.movies1}]
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('rating').start_at({'rating': 8.0}).get() == []
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('rating').start_at({'rating': 7.0}).get() == [{self.__class__.auto_doc_id: self.__class__.movies2}, {'001': self.__class__.movies1}]		

	def test_collection_get_select(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').select(['lead.name', 'released']).get() == [{'001': {'lead': self.__class__.movies1['lead'], 'released': self.__class__.movies1['released']}}, {self.__class__.auto_doc_id: {'lead': self.__class__.movies2['lead'], 'released': self.__class__.movies2['released']}}]

	def test_collection_get_offset(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('year').offset(1).get() == [{self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_collection_get_limit_to_first(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('year').limit_to_first(1).get() == [{'001': self.__class__.movies1}]

	def test_collection_get_limit_to_last(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('year', direction='DESCENDING').limit_to_last(1).get() == [{'001': self.__class__.movies1}]

	def test_collection_get_end_at(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('year').end_at({'year': 2010}).get() == [{'001': self.__class__.movies1}]
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('year').end_at({'year': 2021}).get() == [{'001': self.__class__.movies1}, {self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_collection_get_end_before(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').order_by('year').end_before({'year': 2023}).get() == [{'001': self.__class__.movies1}, {self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_collection_get_where(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').where('lead.name', 'in',  ['Benedict Cumberbatch', 'Robert Downey Jr.']).get() == [{'001': self.__class__.movies1}]
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').where('rating', '<=', 8.0).order_by('rating', direction='DESCENDING').get() == [{'001': self.__class__.movies1}, {self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_manual_doc_update(self, ds_admin):
		update_data = {'released': True}

		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document('001').update(update_data) is None
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document('001').get(field_paths=['released']) == update_data

		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document(self.__class__.auto_doc_id).update(update_data) is None
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document(self.__class__.auto_doc_id).get(field_paths=['released']) == update_data

	def test_manual_doc_get_filtered(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document('001').get(field_paths=['name']) == {'name': self.__class__.movies1['name']}
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document(self.__class__.auto_doc_id).get(field_paths=['name']) == {'name': self.__class__.movies2['name']}

	def test_manual_doc_delete(self, ds_admin):
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document('001').delete() is None
		assert ds_admin.collection('Marvels').document('Movies').collection('PhaseOne').document(self.__class__.auto_doc_id).delete() is None


class TestFirestoreAuth:
	movies1 = {
		'name': 'Dr. Strange',
		'lead': {'name': 'Benedict Cumberbatch'},
		'director': {},
		'released': False,
		'year': 2016,
		'rating': 7.5,
		'prequel': None,
		'cast': ['Tilda Swinton', 'Rachel McAdams', 'Mads Mikkelsen', 'Chiwetel Ejiofor', 'Benedict Wong'],
		'producers': []
	}

	movies2 = {
		'name': 'Black Panther',
		'lead': {'name': 'Chadwick Boseman'},
		'released': False,
		'year': 2018,
		'rating': 7.3,
		'prequel': None,
		'cast': ['Michael B. Jordan', 'Sebastian Stan', 'Letitia Wright', 'Martin Freeman', 'Winston Duke']
	}

	user = None
	auto_doc_id = None

	def test_create_test_user(self, auth):
		user = auth.sign_in_anonymous()
		self.__class__.user = user
		assert user
		assert user.get('idToken')

	def test_manual_doc_set(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document('014').set(self.__class__.movies1, token=self.__class__.user.get('idToken')) is None

	def test_auto_doc_add(self, ds):
		doc_id = ds.collection('Marvels').document('Movies').collection('PhaseThree').add(self.__class__.movies2, token=self.__class__.user.get('idToken'))
		assert doc_id

		self.__class__.auto_doc_id = doc_id

	def test_manual_doc_get(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document('014').get(token=self.__class__.user.get('idToken')) == self.__class__.movies1
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document(self.__class__.auto_doc_id).get(token=self.__class__.user.get('idToken')) == self.__class__.movies2

	def test_collection_get(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}, {self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_collection_list_documents(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').list_of_documents(token=self.__class__.user.get('idToken')) == ['014', self.__class__.auto_doc_id]

	def test_manual_doc_get_filtered(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document('014').get(field_paths=['name'], token=self.__class__.user.get('idToken')) == {'name': self.__class__.movies1['name']}
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document(self.__class__.auto_doc_id).get(field_paths=['name'], token=self.__class__.user.get('idToken')) == {'name': self.__class__.movies2['name']}

	def test_collection_get_start_after(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('rating').start_after({'rating': 7.4}).get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}]
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('rating').start_after({'rating': 7.2}).get(token=self.__class__.user.get('idToken')) == [{self.__class__.auto_doc_id: self.__class__.movies2}, {'014': self.__class__.movies1}]
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('rating').start_after({'rating': 8.5}).get(token=self.__class__.user.get('idToken')) == []

	def test_collection_get_start_at(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('rating').start_at({'rating': 7.4}).get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}]
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('rating').start_at({'rating': 8.0}).get(token=self.__class__.user.get('idToken')) == []
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('rating').start_at({'rating': 7.0}).get(token=self.__class__.user.get('idToken')) == [{self.__class__.auto_doc_id: self.__class__.movies2}, {'014': self.__class__.movies1}]		

	def test_collection_get_select(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').select(['lead.name', 'released']).get(token=self.__class__.user.get('idToken')) == [{'014': {'lead': self.__class__.movies1['lead'], 'released': self.__class__.movies1['released']}}, {self.__class__.auto_doc_id: {'lead': self.__class__.movies2['lead'], 'released': self.__class__.movies2['released']}}]

	def test_collection_get_offset(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('year').offset(1).get(token=self.__class__.user.get('idToken')) == [{self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_collection_get_limit_to_first(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('year').limit_to_first(1).get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}]

	def test_collection_get_limit_to_last(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('year').limit_to_last(1).get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}]

	def test_collection_get_end_at(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('year').end_at({'year': 2010}).get(token=self.__class__.user.get('idToken')) == []
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('year').end_at({'year': 2021}).get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}, {self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_collection_get_end_before(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').order_by('year').end_before({'year': 2023}).get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}, {self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_collection_get_where(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').where('lead.name', 'in',  ['Benedict Cumberbatch', 'Robert Downey Jr.']).get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}]
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').where('rating', '<=', 8.0).order_by('rating', direction='DESCENDING').get(token=self.__class__.user.get('idToken')) == [{'014': self.__class__.movies1}, {self.__class__.auto_doc_id: self.__class__.movies2}]

	def test_manual_doc_update(self, ds):
		update_data = {'released': True}

		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document('014').update(update_data, token=self.__class__.user.get('idToken')) is None
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document('014').get(field_paths=['released'], token=self.__class__.user.get('idToken')) == update_data

		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document(self.__class__.auto_doc_id).update(update_data, token=self.__class__.user.get('idToken')) is None
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document(self.__class__.auto_doc_id).get(field_paths=['released'], token=self.__class__.user.get('idToken')) == update_data

	def test_manual_doc_delete(self, ds):
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document('014').delete(self.__class__.user.get('idToken')) is None
		assert ds.collection('Marvels').document('Movies').collection('PhaseThree').document(self.__class__.auto_doc_id).delete(self.__class__.user.get('idToken')) is None

	def test_delete_test_user(self, auth):
		assert auth.delete_user_account(self.__class__.user.get('idToken'))


class TestFirestore:
	series1 = {
		'name': 'Loki',
		'lead': {'name': 'Tom Hiddleston'},
		'released': False,
		'year': 2021,
		'rating': 8.2,
		'prequel': None,
		'cast': ['Sophia Di Martino', 'Owen Wilson', 'Jonathan Majors', 'Wunmi Mosaku', 'Gugu Mbatha-Raw']
	}
	
	series2 = {
		'name': 'Moon Knight',
		'lead': {'name': 'Oscar Issac'},
		'released': False,
		'year': 2022,
		'rating': 7.4,
		'prequel': None,
		'cast': ['Ethan Hawke', 'May Calamawy', 'F. Murray Abraham']
	}

	auto_doc_id = None

	def test_manual_doc_set(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document('003').set(self.__class__.series1) is None

	def test_auto_doc_add(self, ds):
		doc_id = ds.collection('Marvels').document('Series').collection('PhaseFour').add(self.__class__.series2)
		assert doc_id

		self.__class__.auto_doc_id = doc_id

	def test_manual_doc_get(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document('003').get() == self.__class__.series1
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document(self.__class__.auto_doc_id).get() == self.__class__.series2

	def test_collection_get(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').get() == [{'003': self.__class__.series1}, {self.__class__.auto_doc_id: self.__class__.series2}]

	def test_collection_list_documents(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').list_of_documents() == ['003', self.__class__.auto_doc_id]

	def test_manual_doc_get_filtered(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document('003').get(field_paths=['name']) == {'name': self.__class__.series1['name']}
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document(self.__class__.auto_doc_id).get(field_paths=['name']) == {'name': self.__class__.series2['name']}

	def test_collection_get_start_after(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('rating').start_after({'rating': 7.4}).get() == [{'003': self.__class__.series1}]
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('rating').start_after({'rating': 7.3}).get() == [{self.__class__.auto_doc_id: self.__class__.series2}, {'003': self.__class__.series1}]
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('rating').start_after({'rating': 8.5}).get() == []

	def test_collection_get_start_at(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('rating').start_at({'rating': 7.4}).get() == [{self.__class__.auto_doc_id: self.__class__.series2}, {'003': self.__class__.series1}]
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('rating').start_at({'rating': 8.0}).get() == [{'003': self.__class__.series1}]
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('rating').start_at({'rating': 8.5}).get() == []		

	def test_collection_get_select(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').select(['lead.name', 'released']).get() == [{'003': {'lead': self.__class__.series1['lead'], 'released': self.__class__.series1['released']}}, {self.__class__.auto_doc_id: {'lead': self.__class__.series2['lead'], 'released': self.__class__.series2['released']}}]

	def test_collection_get_offset(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('year').offset(1).get() == [{self.__class__.auto_doc_id: self.__class__.series2}]

	def test_collection_get_limit_to_first(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('year').limit_to_first(1).get() == [{'003': self.__class__.series1}]

	def test_collection_get_limit_to_last(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('year').limit_to_last(1).get() == [{'003': self.__class__.series1}]

	def test_collection_get_end_at(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('year').end_at({'year': 2010}).get() == []
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('year').end_at({'year': 2021}).get() == [{'003': self.__class__.series1}]

	def test_collection_get_end_before(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').order_by('year').end_before({'year': 2023}).get() == [{'003': self.__class__.series1}, {self.__class__.auto_doc_id: self.__class__.series2}]

	def test_collection_get_where(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').where('lead.name', 'in',  ['Benedict Cumberbatch', 'Robert Downey Jr.']).get() == []
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').where('rating', '<=', 8.0).get() == [{self.__class__.auto_doc_id: self.__class__.series2}]

	def test_manual_doc_update(self, ds):
		update_data = {'released': True}

		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document('003').update(update_data) is None
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document('003').get(field_paths=['released']) == update_data

		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document(self.__class__.auto_doc_id).update(update_data) is None
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document(self.__class__.auto_doc_id).get(field_paths=['released']) == update_data

	def test_manual_doc_delete(self, ds):
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document('003').delete() is None
		assert ds.collection('Marvels').document('Series').collection('PhaseFour').document(self.__class__.auto_doc_id).delete() is None
