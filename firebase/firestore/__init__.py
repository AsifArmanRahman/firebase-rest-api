
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


"""
A simple python wrapper for Google's `Firebase Cloud Firestore REST API`_

.. _Firebase Cloud Firestore REST API:
	https://firebase.google.com/docs/firestore/reference/rest
"""

from math import ceil
from proto.message import Message
from google.cloud.firestore import Client
from google.cloud.firestore_v1._helpers import *
from google.cloud.firestore_v1.query import Query
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.base_query import _enum_from_direction

from ._utils import _from_datastore, _to_datastore
from firebase._exception import raise_detailed_error


class Firestore:
	""" Firebase Firestore Service

	:type api_key: str
	:param api_key: ``apiKey`` from Firebase configuration

	:type credentials: :class:`~google.oauth2.service_account.Credentials`
	:param credentials: Service Account Credentials

	:type project_id: str
	:param project_id: ``projectId`` from Firebase configuration

	:type requests: :class:`~requests.Session`
	:param requests: Session to make HTTP requests
	"""

	def __init__(self, api_key, credentials, project_id, requests):
		""" Constructor method """

		self._api_key = api_key
		self._credentials = credentials
		self._project_id = project_id
		self._requests = requests

	def collection(self, collection_id):
		""" Get reference to a collection in a Firestore database.


		:type collection_id: str
		:param collection_id: An ID of collection in firestore.


		:return: Reference to a collection.
		:rtype: Collection
		"""

		return Collection([collection_id], api_key=self._api_key, credentials=self._credentials, project_id=self._project_id, requests=self._requests)


class Collection:
	""" A reference to a collection in a Firestore database.

	:type collection_path: list
	:param collection_path: Collective form of strings to create a
		Collection.

	:type api_key: str
	:param api_key: ``apiKey`` from Firebase configuration

	:type credentials: :class:`~google.oauth2.service_account.Credentials`
	:param credentials: Service Account Credentials

	:type project_id: str
	:param project_id: ``projectId`` from Firebase configuration

	:type requests: :class:`~requests.Session`
	:param requests: Session to make HTTP requests
	"""

	def __init__(self, collection_path, api_key, credentials, project_id, requests):
		""" Constructor method """

		self._path = collection_path

		self._api_key = api_key
		self._credentials = credentials
		self._project_id = project_id
		self._requests = requests

		self._base_path = f"projects/{self._project_id}/databases/(default)/documents"
		self._base_url = f"https://firestore.googleapis.com/v1/{self._base_path}"

		if self._credentials:
			self.__datastore = Client(credentials=self._credentials, project=self._project_id)

		self._query = {}
		self._is_limited_to_last = False

	def _build_query(self):
		""" Builds query for firestore to execute.


		:return: An query.
		:rtype: :class:`~google.cloud.firestore_v1.query.Query`
		"""

		if self._credentials:
			_query = _build_db(self.__datastore, self._path)
		else:
			_query = Query(CollectionReference(self._path.pop()))

		for key, val in self._query.items():
			if key == 'endAt':
				_query = _query.end_at(val)
			elif key == 'endBefore':
				_query = _query.end_before(val)
			elif key == 'limit':
				_query = _query.limit(val)
			elif key == 'limitToLast':
				_query = _query.limit_to_last(val)
			elif key == 'offset':
				_query = _query.offset(val)
			elif key == 'orderBy':
				for q in val:
					_query = _query.order_by(q[0], **q[1])
			elif key == 'select':
				_query = _query.select(val)
			elif key == 'startAfter':
				_query = _query.start_after(val)
			elif key == 'startAt':
				_query = _query.start_at(val)
			elif key == 'where':
				for q in val:
					_query = _query.where(q[0], q[1], q[2])

		if not self._credentials and _query._limit_to_last:

			self._is_limited_to_last = _query._limit_to_last

			for order in _query._orders:
				order.direction = _enum_from_direction(
					_query.DESCENDING
					if order.direction == _query.ASCENDING
					else _query.ASCENDING
				)

			_query._limit_to_last = False

		self._path.clear()
		self._query.clear()

		return _query

	def add(self, data, token=None):
		""" Create a document in the Firestore database with the
		provided data using an auto generated ID for the document.


		:type data: dict
		:param data: Data to be stored in firestore.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults
			to :data:`None`.


		:return: returns the auto generated document ID, used to store
			the data.
		:rtype: str
		"""

		path = self._path.copy()
		self._path.clear()

		if self._credentials:
			db_ref = _build_db(self.__datastore, path)

			response = db_ref.add(data)

			return response[1].id

		else:
			req_ref = f"{self._base_url}/{'/'.join(path)}?key={self._api_key}"

			if token:
				headers = {"Authorization": "Firebase " + token}
				response = self._requests.post(req_ref, headers=headers, json=_to_datastore(data))

			else:
				response = self._requests.post(req_ref, json=_to_datastore(data))

			raise_detailed_error(response)

			doc_id = response.json()['name'].split('/')

			return doc_id.pop()

	def document(self, document_id):
		""" A reference to a document in a collection.


		:type document_id: str
		:param document_id: An ID of document inside a collection.


		:return: Reference to a document.
		:rtype: Document
		"""

		self._path.append(document_id)
		return Document(self._path, api_key=self._api_key, credentials=self._credentials, project_id=self._project_id, requests=self._requests)

	def end_at(self, document_fields):
		""" End query at a cursor with this collection as parent.


		:type document_fields: dict
		:param document_fields: A dictionary of fields representing a
			query results cursor. A cursor is a collection of values
			that represent a position in a query result set.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		self._query['endAt'] = document_fields

		return self

	def end_before(self, document_fields):
		""" End query before a cursor with this collection as parent.


		:type document_fields: dict
		:param document_fields: A dictionary of fields representing a
			query results cursor. A cursor is a collection of values
			that represent a position in a query result set.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		self._query['endBefore'] = document_fields

		return self

	def get(self, token=None):
		""" Returns a list of dict's containing document ID and the
		data stored within them.


		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults
			to :data:`None`.


		:return: A list of document ID's with the data they possess.
		:rtype: list
		"""

		docs = []

		if self._credentials:
			db_ref = self._build_query()

			results = db_ref.get()

			for result in results:
				docs.append({result.id: result.to_dict()})

		else:

			body = None

			if len(self._query) > 0:
				req_ref = f"{self._base_url}/{'/'.join(self._path[:-1])}:runQuery?key={self._api_key}"

				body = {
					"structuredQuery": json.loads(Message.to_json(self._build_query()._to_protobuf()))
				}

			else:
				req_ref = f"{self._base_url}/{'/'.join(self._path)}?key={self._api_key}"

			if token:
				headers = {"Authorization": "Firebase " + token}

				if body:
					response = self._requests.post(req_ref, headers=headers, json=body)
				else:
					response = self._requests.get(req_ref, headers=headers)

			else:

				if body:
					response = self._requests.post(req_ref, json=body)
				else:
					response = self._requests.get(req_ref)

			raise_detailed_error(response)

			if isinstance(response.json(), dict):
				for doc in response.json()['documents']:
					doc_id = doc['name'].split('/')
					docs.append({doc_id.pop(): _from_datastore({'fields': doc['fields']})})

			elif isinstance(response.json(), list):
				for doc in response.json():
					fields = {}

					if doc.get('document'):

						if doc.get('document').get('fields'):
							fields = doc['document']['fields']

						doc_id = doc['document']['name'].split('/')
						docs.append({doc_id.pop(): _from_datastore({'fields': fields})})

			if self._is_limited_to_last:
				docs = list(reversed(list(docs)))

		return docs

	def list_of_documents(self, token=None):
		""" List all sub-documents of the current collection.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults
			to :data:`None`.


		:return: A list of document ID's.
		:rtype: list
		"""

		docs = []

		path = self._path.copy()
		self._path.clear()

		if self._credentials:
			db_ref = _build_db(self.__datastore, path)

			list_doc = list(db_ref.list_documents())

			for doc in list_doc:
				docs.append(doc.id)

		else:

			req_ref = f"{self._base_url}/{'/'.join(path)}?key={self._api_key}"

			if token:
				headers = {"Authorization": "Firebase " + token}
				response = self._requests.get(req_ref, headers=headers)

			else:
				response = self._requests.get(req_ref)

			raise_detailed_error(response)

			if response.json().get('documents'):
				for doc in response.json()['documents']:
					doc_id = doc['name'].split('/')
					docs.append(doc_id.pop())

		return docs

	def limit_to_first(self, count):
		""" Create a limited query with this collection as parent.

			.. note::
				`limit_to_first` and `limit_to_last` are mutually
				exclusive. Setting `limit_to_first` will drop
				previously set `limit_to_last`.


		:type count: int
		:param count: Maximum number of documents to return that match
			the query.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		self._query['limit'] = count

		return self

	def limit_to_last(self, count):
		""" Create a limited to last query with this collection as
		parent.

			.. note::
				`limit_to_first` and `limit_to_last` are mutually
				exclusive. Setting `limit_to_first` will drop
				previously set `limit_to_last`.


		:type count: int
		:param count: Maximum number of documents to return that
			match the query.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		self._query['limitToLast'] = count

		return self

	def offset(self, num_to_skip):
		""" Skip to an offset in a query with this collection as parent.


		:type num_to_skip: int
		:param num_to_skip: The number of results to skip at the
			beginning of query results. (Must be non-negative.)


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		self._query['offset'] = num_to_skip

		return self

	def order_by(self, field_path, **kwargs):
		""" Create an "order by" query with this collection as parent.


		:type field_path: str
		:param field_path: A field path (``.``-delimited list of field
			names) on which to order the query results.

		:Keyword Arguments:
			* *direction* ( :class:`str` ) --
				Sort query results in ascending/descending order on a field.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		arr = []

		if self._query.get('orderBy'):
			arr = self._query['orderBy']

		arr.append([field_path, kwargs])

		self._query['orderBy'] = arr

		return self

	def select(self, field_paths):
		""" Create a "select" query with this collection as parent.

		:type field_paths: list
		:param field_paths: A list of field paths (``.``-delimited list
			of field names) to use as a projection of document fields
			in the query results.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		self._query['select'] = field_paths

		return self

	def start_after(self, document_fields):
		""" Start query after a cursor with this collection as parent.


		:type document_fields: dict
		:param document_fields: A dictionary of fields representing
			a query results cursor. A cursor is a collection of values
			that represent a position in a query result set.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		self._query['startAfter'] = document_fields

		return self

	def start_at(self, document_fields):
		""" Start query at a cursor with this collection as parent.


		:type document_fields: dict
		:param document_fields: A dictionary of fields representing a
			query results cursor. A cursor is a collection of values
			that represent a position in a query result set.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		self._query['startAt'] = document_fields

		return self

	def where(self, field_path, op_string, value):
		""" Create a "where" query with this collection as parent.


		:type field_path: str
		:param field_path: A field path (``.``-delimited list of field
			names) for the field to filter on.

		:type op_string: str
		:param op_string: A comparison operation in the form of a
			string. Acceptable values are ``<``, ``<=``, ``==``, ``!=``
			, ``>=``, ``>``, ``in``, ``not-in``, ``array_contains`` and
			``array_contains_any``.

		:type value: Any
		:param value: The value to compare the field against in the
			filter. If ``value`` is :data:`None` or a NaN, then ``==``
			is the only allowed operation.  If ``op_string`` is ``in``,
			``value`` must be a sequence of values.


		:return: A reference to the instance object.
		:rtype: Collection
		"""

		arr = []

		if self._query.get('where'):
			arr = self._query['where']

		arr.append([field_path, op_string, value])

		self._query['where'] = arr

		return self


class Document:
	""" A reference to a document in a Firestore database.

	:type document_path: list
	:param document_path: Collective form of strings to create a
		Document.

	:type api_key: str
	:param api_key: ``apiKey`` from Firebase configuration

	:type credentials: :class:`~google.oauth2.service_account.Credentials`
	:param credentials: Service Account Credentials

	:type project_id: str
	:param project_id: ``projectId`` from Firebase configuration

	:type requests: :class:`~requests.Session`
	:param requests: Session to make HTTP requests
	"""

	def __init__(self, document_path, api_key, credentials, project_id, requests):
		""" Constructor method """

		self._path = document_path

		self._api_key = api_key
		self._credentials = credentials
		self._project_id = project_id
		self._requests = requests

		self._base_path = f"projects/{self._project_id}/databases/(default)/documents"
		self._base_url = f"https://firestore.googleapis.com/v1/{self._base_path}"

		if self._credentials:
			self.__datastore = Client(credentials=self._credentials, project=self._project_id)

	def collection(self, collection_id):
		""" A reference to a collection in a Firestore database.


		:type collection_id: str
		:param collection_id: An ID of collection in firestore.


		:return: Reference to a collection.
		:rtype: Collection
		"""

		self._path.append(collection_id)
		return Collection(self._path, api_key=self._api_key, credentials=self._credentials, project_id=self._project_id, requests=self._requests)

	def delete(self, token=None):
		""" Deletes the current document from firestore.

		| For more details:
		| |delete_documents|_

		.. |delete_documents| replace::
			Firebase Documentation | Delete data from Cloud
			Firestore | Delete documents

		.. _delete_documents:
			https://firebase.google.com/docs/firestore/manage-data/delete-data#delete_documents

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults
			to :data:`None`.
		"""

		path = self._path.copy()
		self._path.clear()

		if self._credentials:
			db_ref = _build_db(self.__datastore, path)

			db_ref.delete()

		else:
			req_ref = f"{self._base_url}/{'/'.join(path)}?key={self._api_key}"

			if token:
				headers = {"Authorization": "Firebase " + token}
				response = self._requests.delete(req_ref, headers=headers)

			else:
				response = self._requests.delete(req_ref)

			raise_detailed_error(response)

	def get(self, field_paths=None, token=None):
		""" Read data from a document in firestore.


		:type field_paths: list
		:param field_paths: (Optional) A list of field paths
			(``.``-delimited list of field names) to filter data, and
			return the filtered values only, defaults
			to :data:`None`.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults
			to :data:`None`.


		:return: The whole data stored in the document unless filtered
			to retrieve specific fields.
		:rtype: dict
		"""

		path = self._path.copy()
		self._path.clear()

		if self._credentials:
			db_ref = _build_db(self.__datastore, path)

			result = db_ref.get(field_paths=field_paths)

			return result.to_dict()

		else:

			mask = ''

			if field_paths:
				for field_path in field_paths:
					mask = f"{mask}mask.fieldPaths={field_path}&"

			req_ref = f"{self._base_url}/{'/'.join(path)}?{mask}key={self._api_key}"

			if token:
				headers = {"Authorization": "Firebase " + token}
				response = self._requests.get(req_ref, headers=headers)

			else:
				response = self._requests.get(req_ref)

			raise_detailed_error(response)

			return _from_datastore(response.json())

	def set(self, data, token=None):
		""" Add data to a document in firestore.

		| For more details:
		| |set_a_document|_

		.. |set_a_document| replace::
			Firebase Documentation | Add data to Cloud Firestore | Set
			a document

		.. _set_a_document:
			https://firebase.google.com/docs/firestore/manage-data/add-data#set_a_document


		:type data: dict
		:param data: Data to be stored in firestore.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults
			to :data:`None`.
		"""

		path = self._path.copy()
		self._path.clear()

		if self._credentials:
			db_ref = _build_db(self.__datastore, path)

			db_ref.set(data)

		else:

			req_ref = f"{self._base_url}:commit?key={self._api_key}"

			body = {
				"writes": [
					Message.to_dict(pbs_for_set_no_merge(f"{self._base_path}/{'/'.join(path)}", data)[0])
					]
			}

			if token:
				headers = {"Authorization": "Firebase " + token}
				response = self._requests.post(req_ref, headers=headers, json=body)

			else:
				response = self._requests.post(req_ref, json=body)

			raise_detailed_error(response)

	def update(self, data, token=None):
		""" Update stored data inside a document in firestore.


		:type data: dict
		:param data: Data to be stored in firestore.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults
			to :data:`None`.
		"""

		path = self._path.copy()
		self._path.clear()

		if self._credentials:
			db_ref = _build_db(self.__datastore, path)

			db_ref.update(data)

		else:
			req_ref = f"{self._base_url}:commit?key={self._api_key}"

			body = {
				"writes": [
					Message.to_dict(pbs_for_update(f"{self._base_path}/{'/'.join(path)}", data, None)[0])
				]
			}

			if token:
				headers = {"Authorization": "Firebase " + token}
				response = self._requests.post(req_ref, headers=headers, json=body)

			else:
				response = self._requests.post(req_ref, json=body)

			raise_detailed_error(response)


def _build_db(db, path):
	""" Returns a reference to Collection/Document with admin
	credentials.


	:type db: :class:`~google.cloud.firestore.Client`
	:param db: Reference to Firestore Client.

	:type path: list
	:param path: Collective form of strings to create a document.


	:return: Reference to collection/document to perform CRUD 
		operations.
	:rtype: :class:`~google.cloud.firestore_v1.document.CollectionReference`
		or :class:`~google.cloud.firestore_v1.document.DocumentReference`
	"""

	n = ceil(len(path) / 2)

	for _ in range(n):
		db = db.collection(path.pop(0))

		if len(path) > 0:
			db = db.document(path.pop(0))

	return db
