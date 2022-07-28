
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


"""
A simple python wrapper for Google's `Firebase Database REST API`_

.. _Firebase Database REST API: 
	https://firebase.google.com/docs/reference/rest/database
"""

import math
import json
import time
from random import randrange
from urllib.parse import urlencode
from google.auth.transport.requests import Request

from ._stream import Stream
from ._db_convert import FirebaseResponse
from firebase._exception import raise_detailed_error
from ._db_convert import convert_to_firebase, convert_list_to_firebase


class Database:
	""" Firebase Database Service


	:type credentials: :class:`~google.oauth2.service_account.Credentials`
	:param credentials: Service Account Credentials.

	:type database_url: str
	:param database_url: ``databaseURL`` from Firebase configuration.

	:type requests: :class:`~requests.Session`
	:param requests: Session to make HTTP requests.
	"""

	def __init__(self, credentials, database_url, requests):
		""" Constructor """

		if not database_url.endswith('/'):
			url = ''.join([database_url, '/'])
		else:
			url = database_url

		self.credentials = credentials
		self.database_url = url
		self.requests = requests

		self.path = ""
		self.build_query = {}
		self.last_push_time = 0
		self.last_rand_chars = []

	def order_by_key(self):
		""" Filter data by their keys.

		| For more details:
		| |filtering_by_key|_

		.. |filtering_by_key| replace:: 
			Firebase Documentation | Retrieve Data | Filtering
			Data | filtering_by_key

		.. _filtering_by_key: 
			https://firebase.google.com/docs/database/rest/retrieve-data#filtering-by-key


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["orderBy"] = "$key"

		return self

	def order_by_value(self):
		""" Filter data by the value of their child keys.

		| For more details:
		| |filtering-by-value|_
		
		.. |filtering-by-value| replace::
			Firebase Documentation | Retrieve Data | Filtering
			Data | filtering-by-value

		.. _filtering-by-value: 
			https://firebase.google.com/docs/database/rest/retrieve-data#filtering-by-value


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["orderBy"] = "$value"

		return self

	def order_by_child(self, order):
		""" Filter data by a common child key.

		| For more details:
		| |filtering-by-a-specified-child-key|_

		.. |filtering-by-a-specified-child-key| replace::
			Firebase Documentation | Retrieve Data | Filtering
			Data | filtering-by-a-specified-child-key

		.. _filtering-by-a-specified-child-key: 
			https://firebase.google.com/docs/database/rest/retrieve-data#filtering-by-a-specified-child-key


		:type order: str
		:param order: Child key name.


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["orderBy"] = order

		return self

	def start_at(self, start):
		""" Filter data where child key value starts from specified
		value.

		| For more details:
		| |range-queries|_

		.. |range-queries| replace::
			Firebase Documentation | Retrieve Data | Complex
			Filtering | range-queries

		.. _range-queries: 
			https://firebase.google.com/docs/database/rest/retrieve-data#range-queries


		:type start: int or float or str
		:param start: Arbitrary starting points for queries.


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["startAt"] = start

		return self

	def end_at(self, end):
		""" Filter data where child key value ends at specified
		value.

		| For more details:
		| |range-queries|_


		:type end: int or float or str
		:param end: Arbitrary ending points for queries.


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["endAt"] = end

		return self

	def equal_to(self, equal):
		""" Filter data where child key value is equal to specified
		value.

		| For more details:
		| |range-queries|_


		:type equal: int or float or str
		:param equal: Arbitrary point for queries.


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["equalTo"] = equal

		return self

	def limit_to_first(self, limit_first):
		""" Filter the number of data to receive from top.

		| For more details:
		| |limit-queries|_

		.. |limit-queries| replace::
			Firebase Documentation | Retrieve Data | Complex
			Filtering | limit-queries

		.. _limit-queries: 
			https://firebase.google.com/docs/database/rest/retrieve-data#limit-queries


		:type limit_first: int
		:param limit_first: Maximum number of children to select
			from top.


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["limitToFirst"] = limit_first

		return self

	def limit_to_last(self, limit_last):
		""" Filter the number of data to receive from bottom.

		| For more details:
		| |limit-queries|_


		:type limit_last: int
		:param limit_last: Maximum number of children to select
			from bottom.


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["limitToLast"] = limit_last

		return self

	def shallow(self):
		""" Limit the depth of the response.

		| For more details:
		| |section-param-shallow|_

		.. |section-param-shallow| replace::
			Firebase Database REST API | Query Parameters |
			section-param-shallow |

		.. _section-param-shallow:
			https://firebase.google.com/docs/reference/rest/database#section-param-shallow


		:return: A reference to the instance object.
		:rtype: Database
		"""

		self.build_query["shallow"] = True

		return self

	def child(self, *args):
		""" Build paths to your data.


		:type args: str
		:param args: Positional arguments to build path to database.


		:return: A reference to the instance object.
		:rtype: Database
		"""

		new_path = "/".join([str(arg) for arg in args])

		if self.path:
			self.path += "/{}".format(new_path)

		else:
			if new_path.startswith("/"):
				new_path = new_path[1:]

			self.path = new_path

		return self

	def build_request_url(self, token):
		""" Builds Request URL for query.


		:type token: str
		:param token: Firebase Auth User ID Token


		:return: Request URL
		:rtype: str
		"""

		parameters = {}

		if token:
			parameters['auth'] = token

		for param in list(self.build_query):
			if type(self.build_query[param]) is str:
				parameters[param] = '"' + self.build_query[param] + '"'

			elif type(self.build_query[param]) is bool:
				parameters[param] = "true" if self.build_query[param] else "false"

			else:
				parameters[param] = self.build_query[param]

		# reset path and build_query for next query
		request_ref = '{0}{1}.json?{2}'.format(self.database_url, self.path, urlencode(parameters))

		self.path = ""
		self.build_query = {}

		return request_ref

	def build_headers(self, token=None):
		""" Build Request Header.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.


		:return: Request Header.
		:rtype: dict
		"""

		headers = {"content-type": "application/json; charset=UTF-8"}

		if not token and self.credentials:

			if not self.credentials.valid:
				self.credentials.refresh(Request())

			access_token = self.credentials.token
			headers['Authorization'] = 'Bearer ' + access_token

		return headers

	def get(self, token=None, json_kwargs={}):
		""" Read data from database.

		| For more details:
		| |section-get|_

		.. |section-get| replace::
			Firebase Database REST API | GET - Reading Data

		.. _section-get:
			https://firebase.google.com/docs/reference/rest/database#section-get


		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.

		:type json_kwargs: dict
		:param json_kwargs: (Optional) Keyword arguments to send to 
			:func:`json.dumps` method for deserialization of data, 
			defaults to :data:`{}` (empty :class:`dict` object).
				

		:return: The data associated with the path.
		:rtype: dict
		"""

		build_query = self.build_query
		query_key = self.path.split("/")[-1]
		request_ref = self.build_request_url(token)

		# headers
		headers = self.build_headers(token)

		# do request
		request_object = self.requests.get(request_ref, headers=headers)

		raise_detailed_error(request_object)
		request_dict = request_object.json(**json_kwargs)

		# if primitive or simple query return
		if isinstance(request_dict, list):
			return FirebaseResponse(convert_list_to_firebase(request_dict), query_key)

		if not isinstance(request_dict, dict):
			return FirebaseResponse(request_dict, query_key)

		if not build_query:
			return FirebaseResponse(convert_to_firebase(request_dict.items()), query_key)

		# return keys if shallow
		if build_query.get("shallow"):
			return FirebaseResponse(request_dict.keys(), query_key)

		# otherwise sort
		sorted_response = None

		if build_query.get("orderBy"):
			if build_query["orderBy"] == "$key":
				sorted_response = sorted(request_dict.items(), key=lambda item: item[0])
			elif build_query["orderBy"] == "$value":
				sorted_response = sorted(request_dict.items(), key=lambda item: item[1])
			else:
				sorted_response = sorted(request_dict.items(), key=lambda item: (build_query["orderBy"] in item[1], item[1].get(build_query["orderBy"], "")))

		return FirebaseResponse(convert_to_firebase(sorted_response), query_key)

	def push(self, data, token=None, json_kwargs={}):
		""" Add data to database.

		This method adds a Firebase Push ID at the end of the specified 
		path, and then adds/stores the data in database, unlike 
		:meth:`set` which does not use a Firebase Push ID.

		| For more details:
		| |section-post|_

		.. |section-post| replace::
			Firebase Database REST API | POST - Pushing Data

		.. _section-post:
			https://firebase.google.com/docs/reference/rest/database#section-post


		:type data: dict
		:param data: Data to be stored in database.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.

		:type json_kwargs: dict
		:param json_kwargs: (Optional) Keyword arguments to send to 
			:func:`json.dumps` method for serialization of data, 
			defaults to :data:`{}` (empty :class:`dict` object).


		:return: Child key (Firebase Push ID) name of the data.
		:rtype: dict
		"""

		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		request_object = self.requests.post(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))

		raise_detailed_error(request_object)

		return request_object.json()

	def set(self, data, token=None, json_kwargs={}):
		""" Add data to database.

		This method writes the data in database in the specified 
		path, unlike :meth:`push` which creates a Firebase Push ID then 
		writes the data to database.

		| For more details:
		| |section-put|_

		.. |section-put| replace::
			Firebase Database REST API | PUT - Writing Data

		.. _section-put:
			https://firebase.google.com/docs/reference/rest/database#section-put


		:type data: dict
		:param data: Data to be stored in database.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.

		:type json_kwargs: dict
		:param json_kwargs: (Optional) Keyword arguments to send to 
			:func:`json.dumps` method for serialization of data, 
			defaults to :data:`{}` (empty :class:`dict` object).


		:return: Successful attempt returns the ``data`` specified to 
			add to database.
		:rtype: dict
		"""

		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		request_object = self.requests.put(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))

		raise_detailed_error(request_object)

		return request_object.json()

	def update(self, data, token=None, json_kwargs={}):
		""" Update stored data of database.

		| For more details:
		| |section-patch|_

		.. |section-patch| replace:: 
			Firebase Database REST API | PATCH - Updating Data

		.. _section-patch: 
			https://firebase.google.com/docs/reference/rest/database#section-patch


		:type data: dict
		:param data: Data to be updated.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.

		:type json_kwargs: dict
		:param json_kwargs: (Optional) Keyword arguments to send to 
			:func:`json.dumps` method for serialization of data, 
			defaults to :data:`{}` (empty :class:`dict` object).


		:return: Successful attempt returns the data specified to 
			update.
		:rtype: dict
		"""

		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		request_object = self.requests.patch(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))

		raise_detailed_error(request_object)

		return request_object.json()

	def remove(self, token=None):
		""" Delete data from database.

		| For more details:
		| |section-delete|_

		.. |section-delete| replace::
			Firebase Database REST API | DELETE - Removing Data

		.. _section-delete: 
			https://firebase.google.com/docs/reference/rest/database#section-delete


		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.


		:return: Successful attempt returns :data:`None`.
		:rtype: :data:`None`
		"""

		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		request_object = self.requests.delete(request_ref, headers=headers)

		raise_detailed_error(request_object)

		return request_object.json()

	def stream(self, stream_handler, token=None, stream_id=None, is_async=True):
		request_ref = self.build_request_url(token)

		return Stream(request_ref, stream_handler, self.build_headers, stream_id, is_async)

	def check_token(self, database_url, path, token):
		""" Builds Request URL to write/update/remove data.


		:type database_url: str
		:param database_url: ``databaseURL`` from Firebase 
			configuration.

		:type path: str
		:param path: Path to data.

		:type token: str
		:param token: Firebase Auth User ID Token


		:return: Request URL
		:rtype: str
		"""

		if token:
			return '{0}{1}.json?auth={2}'.format(database_url, path, token)
		else:
			return '{0}{1}.json'.format(database_url, path)

	def generate_key(self):
		""" Generate Firebase's push IDs.

		| For more details:
		| |firebase-push-id|_

		.. |firebase-push-id| replace::
			Firebase Blog | The 2^120 Ways to Ensure Unique Identifiers

		.. _firebase-push-id:
			https://firebase.blog/posts/2015/02/the-2120-ways-to-ensure-unique_68


		:return: Firebase's push IDs
		:rtype: str
		"""

		push_chars = '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'

		now = int(time.time() * 1000)
		duplicate_time = now == self.last_push_time

		self.last_push_time = now
		time_stamp_chars = [0] * 8

		for i in reversed(range(0, 8)):
			time_stamp_chars[i] = push_chars[now % 64]
			now = int(math.floor(now / 64))

		new_id = "".join(time_stamp_chars)

		if not duplicate_time:
			self.last_rand_chars = [randrange(64) for _ in range(12)]
		else:
			for i in range(0, 11):

				if self.last_rand_chars[i] == 63:
					self.last_rand_chars[i] = 0

				self.last_rand_chars[i] += 1

		for i in range(0, 12):
			new_id += push_chars[self.last_rand_chars[i]]

		return new_id

	def sort(self, origin, by_key, reverse=False):
		""" Further sort data based on a child key value.


		:type origin: dict
		:param origin: Data to be sorted (generally the output from 
			:meth:`get` method).

		:type by_key: str
		:param by_key: Child key name to sort by.

		:type reverse: bool
		:param reverse: (Optional) Whether to return data in descending 
			order, defaults to :data:`False` (data is returned in 
			ascending order).


		:return: Sorted version of the data.
		:rtype: dict
		"""

		# unpack firebase objects
		firebases = origin.each()

		new_list = []

		for firebase in firebases:
			new_list.append(firebase.item)

		# sort
		data = sorted(dict(new_list).items(), key=lambda item: item[1][by_key], reverse=reverse)

		return FirebaseResponse(convert_to_firebase(data), origin.key())

	def get_etag(self, token=None):
		""" Fetches Firebase ETag at a specified location.

		| For more details:
		| |section-cond-etag|_

		.. |section-cond-etag| replace::
			Firebase Database REST API | Conditional Requests | 
			#section-cond-etag

		.. _section-cond-etag: 
			https://firebase.google.com/docs/reference/rest/database#section-cond-etag


		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.


		:return: Firebase ETag
		:rtype: str
		"""

		request_ref = self.build_request_url(token)

		headers = self.build_headers(token)
		# extra header to get ETag
		headers['X-Firebase-ETag'] = 'true'
		request_object = self.requests.get(request_ref, headers=headers)

		raise_detailed_error(request_object)

		return request_object.headers['ETag']

	def conditional_set(self, data, etag, token=None, json_kwargs={}):
		""" Conditionally add data to database.

		| For more details:
		| |section-expected-responses|_

		.. |section-expected-responses| replace::
			Firebase Database REST API | Conditional Requests | 
			section-expected-responses

		.. _section-expected-responses:
			https://firebase.google.com/docs/reference/rest/database#section-expected-responses


		:type data: dict
		:param data: Data to be stored in database.
		
		:type etag: str
		:param etag: Unique identifier for specific data at a
			specified location.
		
		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.
		
		:type json_kwargs: dict
		:param json_kwargs: (Optional) Keyword arguments to send to 
			:meth:`json.dumps` methods for serialization of data, 
			defaults to ``{}`` (empty :class:`dict` object).


		:return: Successful attempt returns the data specified to store,
			failed attempt (due to ETag mismatch) returns the current 
			``ETag`` for the specified path.
		:rtype: dict
		"""

		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		headers['if-match'] = etag

		request_object = self.requests.put(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))

		# ETag didn't match, so we should return the correct one for the user to try again
		if request_object.status_code == 412:
			return {'ETag': request_object.headers['ETag']}

		raise_detailed_error(request_object)

		return request_object.json()

	def conditional_remove(self, etag, token=None):
		""" Conditionally delete data from database.

		| For more details:
		| |section-expected-responses|_


		:type etag: str
		:param etag: Unique identifier for specific data at a
			specified location.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.


		:return: Successful attempt returns :data:`None`, in case of ETag
			mismatch an updated ETag for the specific data is
			returned in :class:`dict` object
		:rtype: :data:`None`
		"""

		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		headers['if-match'] = etag
		request_object = self.requests.delete(request_ref, headers=headers)

		# ETag didn't match, so we should return the correct one for the user to try again
		if request_object.status_code == 412:
			return {'ETag': request_object.headers['ETag']}

		raise_detailed_error(request_object)

		return request_object.json()
