
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


"""
A simple python wrapper for Google's `Firebase Cloud Storage REST API`_

.. _Firebase Cloud Storage REST API:
	https://firebase.google.com/docs/reference/rest/storage/rest
"""

import datetime
from google.cloud import storage
from urllib.parse import quote

from firebase._exception import raise_detailed_error


class Storage:
	""" Firebase Cloud Storage Service 

	:type credentials:
		:class:`~google.oauth2.service_account.Credentials`
	:param credentials: Service Account Credentials.

	:type requests: :class:`~requests.Session`
	:param requests: Session to make HTTP requests.

	:type storage_bucket: str
	:param storage_bucket: ``storageBucket`` from Firebase 
		configuration.
	"""

	def __init__(self, credentials, requests, storage_bucket):
		""" Constructor """

		self.credentials = credentials
		self.requests = requests
		self.storage_bucket = "https://firebasestorage.googleapis.com/v0/b/" + storage_bucket

		self.path = ""

		if credentials:
			client = storage.Client(credentials=credentials, project=storage_bucket)
			self.bucket = client.get_bucket(storage_bucket)

	def child(self, *args):
		""" Build paths to your storage.


		:type args: str
		:param args: Positional arguments to build path to storage.


		:return: A reference to the instance object.
		:rtype: Storage
		"""

		new_path = "/".join(args)

		if self.path:
			self.path += "/{}".format(new_path)
		else:
			if new_path.startswith("/"):
				new_path = new_path[1:]

			self.path = new_path

		return self

	def put(self, file, token=None):
		""" Upload file to storage.

		| For more details:
		| |upload_files|_

		.. |upload_files| replace::
			Firebase Documentation | Upload files with Cloud Storage on 
			Web

		.. _upload_files:
			https://firebase.google.com/docs/storage/web/upload-files#upload_files


		:type file: str
		:param file: Local path to file to upload.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.


		:return: Successful attempt returns :data:`None`.
		:rtype: :data:`None`
		"""

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

	def delete(self, token=None):
		""" Delete file from storage.

		| For more details:
		| |delete_a_file|_

		.. |delete_a_file| replace::
			Firebase Documentation | Delete files with Cloud Storage on 
			Web

		.. _delete_a_file:
			https://firebase.google.com/docs/storage/web/delete-files#delete_a_file


		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.
		"""

		# reset path
		path = self.path
		self.path = None

		# remove leading backlash
		if path.startswith('/'):
			path = path[1:]

		if self.credentials:
			self.bucket.delete_blob(path)
		else:
			request_ref = self.storage_bucket + "/o?name={0}".format(path)

			if token:
				headers = {"Authorization": "Firebase " + token}
				request_object = self.requests.delete(request_ref, headers=headers)
			else:
				request_object = self.requests.delete(request_ref)

			raise_detailed_error(request_object)

	def download(self, filename, token=None):
		""" Download file from storage.

		| For more details:
		| |download_data_via_url|_

		.. |download_data_via_url| replace::
			Firebase Documentation | Download files with Cloud Storage 
			on Web

		.. _download_data_via_url:
			https://firebase.google.com/docs/storage/web/download-files#download_data_via_url


		:type filename:  str
		:param filename: File name to be downloaded as.

		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults 
			to :data:`None`.
		"""

		if self.credentials:

			# reset path
			path = self.path
			self.path = None

			# remove leading backlash
			if path.startswith('/'):
				path = path[1:]

			blob = self.bucket.get_blob(path)
			if blob is not None:
				blob.download_to_filename(filename)

		elif token:
			headers = {"Authorization": "Firebase " + token}
			r = self.requests.get(self.get_url(token), stream=True, headers=headers)

			if r.status_code == 200:
				with open(filename, 'wb') as f:
					for chunk in r:
						f.write(chunk)

		else:
			r = self.requests.get(self.get_url(token), stream=True)

			if r.status_code == 200:
				with open(filename, 'wb') as f:
					for chunk in r:
						f.write(chunk)

	def get_url(self, token=None, expiration_hour=24):
		""" Fetches URL for file.


		:type token: str
		:param token: (Optional) Firebase Auth User ID Token, defaults
			to :data:`None`.

		:type expiration_hour: int
		:param expiration_hour: (Optional) time in ``hour`` for URL to
			expire after, defaults to 24 hours. Works only for links
			generated with admin credentials.

		:return: URL for the file.
		:rtype: str
		"""

		# reset path
		path = self.path
		self.path = None

		# remove leading backlash
		if path.startswith('/'):
			path = path[1:]

		if self.credentials:
			blob = self.bucket.get_blob(path)
			if blob:
				return blob.generate_signed_url(datetime.timedelta(hours=expiration_hour), method='GET')

		elif token:

			# retrieve download tokens first
			headers = {"Authorization": "Firebase " + token}
			request_ref = "{0}/o/{1}".format(self.storage_bucket, quote(path, safe=''))
			request_object = self.requests.get(request_ref, headers=headers)

			raise_detailed_error(request_object)

			return "{0}/o/{1}?alt=media&token={2}".format(self.storage_bucket, quote(path, safe=''), request_object.json()['downloadTokens'])

		return "{0}/o/{1}?alt=media".format(self.storage_bucket, quote(path, safe=''))

	def list_files(self):
		""" List of all files in storage.

		| for more details:
		| |list_all_files|_

		.. |list_all_files| replace::
			Firebase Documentation | List files with Cloud Storage on 
			Web

		.. _list_all_files:
			https://firebase.google.com/docs/storage/web/list-files#list_all_files


		:return: list of :class:`~gcloud.storage.blob.Blob`
		:rtype: :class:`~gcloud.storage.bucket._BlobIterator`
		"""

		return self.bucket.list_blobs()
