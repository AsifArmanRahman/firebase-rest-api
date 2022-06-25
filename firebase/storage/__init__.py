
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import requests
from gcloud import storage

try:
	from urllib.parse import quote
except:
	from urllib import quote

from firebase._exception import raise_detailed_error


class Storage:
	""" Storage Service """

	def __init__(self, credentials, requests, storage_bucket):
		self.credentials = credentials
		self.requests = requests
		self.storage_bucket = "https://firebasestorage.googleapis.com/v0/b/" + storage_bucket

		self.path = ""

		if credentials:
			client = storage.Client(credentials=credentials, project=storage_bucket)
			self.bucket = client.get_bucket(storage_bucket)

	def child(self, *args):
		new_path = "/".join(args)

		if self.path:
			self.path += "/{}".format(new_path)
		else:
			if new_path.startswith("/"):
				new_path = new_path[1:]

			self.path = new_path

		return self

	def put(self, file, token=None):
		# reset path
		path = self.path
		self.path = None

		if isinstance(file, str):
			file_object = open(file, 'rb')
		else:
			file_object = file

		request_ref = self.storage_bucket + "/o?name={0}".format(path)

		if token:
			headers = {"Authorization": "Firebase " + token}
			request_object = self.requests.post(request_ref, headers=headers, data=file_object)

			raise_detailed_error(request_object)

			return request_object.json()

		elif self.credentials:
			blob = self.bucket.blob(path)

			if isinstance(file, str):
				return blob.upload_from_filename(filename=file)
			else:
				return blob.upload_from_file(file_obj=file)

		else:
			request_object = self.requests.post(request_ref, data=file_object)

			raise_detailed_error(request_object)

			return request_object.json()

	def delete(self, name, token):
		if self.credentials:
			self.bucket.delete_blob(name)
		else:
			request_ref = self.storage_bucket + "/o?name={0}".format(name)

			if token:
				headers = {"Authorization": "Firebase " + token}
				request_object = self.requests.delete(request_ref, headers=headers)
			else:
				request_object = self.requests.delete(request_ref)

			raise_detailed_error(request_object)

	def download(self, path, filename, token=None):
		# remove leading backlash
		url = self.get_url(token)

		if path.startswith('/'):
			path = path[1:]

		if self.credentials:
			blob = self.bucket.get_blob(path)
			if not blob is None:
				blob.download_to_filename(filename)

		elif token:
			headers = {"Authorization": "Firebase " + token}
			r = requests.get(url, stream=True, headers=headers)

			if r.status_code == 200:
				with open(filename, 'wb') as f:
					for chunk in r:
						f.write(chunk)

		else:
			r = requests.get(url, stream=True)

			if r.status_code == 200:
				with open(filename, 'wb') as f:
					for chunk in r:
						f.write(chunk)

	def get_url(self, token):
		path = self.path
		self.path = None

		if path.startswith('/'):
			path = path[1:]

		if token:
			return "{0}/o/{1}?alt=media&token={2}".format(self.storage_bucket, quote(path, safe=''), token)

		return "{0}/o/{1}?alt=media".format(self.storage_bucket, quote(path, safe=''))

	def list_files(self):
		return self.bucket.list_blobs()
