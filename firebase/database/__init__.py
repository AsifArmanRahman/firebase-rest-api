
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import math
import json
import time
from random import randrange
from urllib.parse import urlencode

from ._stream import Stream
from ._db_convert import FirebaseResponse
from firebase._exception import raise_detailed_error
from ._db_convert import convert_to_firebase, convert_list_to_firebase


class Database:
	""" Database Service """

	def __init__(self, api_key, credentials, database_url, requests):
		if not database_url.endswith('/'):
			url = ''.join([database_url, '/'])
		else:
			url = database_url

		self.api_key = api_key
		self.credentials = credentials
		self.database_url = url
		self.requests = requests

		self.path = ""
		self.build_query = {}
		self.last_push_time = 0
		self.last_rand_chars = []

	def order_by_key(self):
		self.build_query["orderBy"] = "$key"

		return self

	def order_by_value(self):
		self.build_query["orderBy"] = "$value"

		return self

	def order_by_child(self, order):
		self.build_query["orderBy"] = order

		return self

	def start_at(self, start):
		self.build_query["startAt"] = start

		return self

	def end_at(self, end):
		self.build_query["endAt"] = end

		return self

	def equal_to(self, equal):
		self.build_query["equalTo"] = equal

		return self

	def limit_to_first(self, limit_first):
		self.build_query["limitToFirst"] = limit_first

		return self

	def limit_to_last(self, limit_last):
		self.build_query["limitToLast"] = limit_last

		return self

	def shallow(self):
		self.build_query["shallow"] = True

		return self

	def child(self, *args):
		new_path = "/".join([str(arg) for arg in args])

		if self.path:
			self.path += "/{}".format(new_path)

		else:
			if new_path.startswith("/"):
				new_path = new_path[1:]

			self.path = new_path

		return self

	def build_request_url(self, token):
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
		headers = {"content-type": "application/json; charset=UTF-8"}

		if not token and self.credentials:
			access_token = self.credentials.get_access_token().access_token
			headers['Authorization'] = 'Bearer ' + access_token

		return headers

	def get(self, token=None, json_kwargs={}):
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
		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		request_object = self.requests.post(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))

		raise_detailed_error(request_object)

		return request_object.json()

	def set(self, data, token=None, json_kwargs={}):
		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		request_object = self.requests.put(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))

		raise_detailed_error(request_object)

		return request_object.json()

	def update(self, data, token=None, json_kwargs={}):
		request_ref = self.check_token(self.database_url, self.path, token)

		self.path = ""

		headers = self.build_headers(token)
		request_object = self.requests.patch(request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8"))

		raise_detailed_error(request_object)

		return request_object.json()

	def remove(self, token=None):
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
		if token:
			return '{0}{1}.json?auth={2}'.format(database_url, path, token)
		else:
			return '{0}{1}.json'.format(database_url, path)

	def generate_key(self):
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
		# unpack firebase objects
		firebases = origin.each()

		new_list = []

		for firebase in firebases:
			new_list.append(firebase.item)

		# sort
		data = sorted(dict(new_list).items(), key=lambda item: item[1][by_key], reverse=reverse)

		return FirebaseResponse(convert_to_firebase(data), origin.key())

	def get_etag(self, token=None, json_kwargs={}):
		request_ref = self.build_request_url(token)

		headers = self.build_headers(token)
		# extra header to get ETag
		headers['X-Firebase-ETag'] = 'true'
		request_object = self.requests.get(request_ref, headers=headers)

		raise_detailed_error(request_object)

		return request_object.headers['ETag']

	def conditional_set(self, data, etag, token=None, json_kwargs={}):
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
