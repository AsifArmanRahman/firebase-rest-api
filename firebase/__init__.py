
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import requests
from oauth2client.service_account import ServiceAccountCredentials

from .auth import Auth
from .storage import Storage
from .database import Database


def initialize_app(config):
	return Firebase(config)


class Firebase:
	""" Firebase Interface """

	def __init__(self, config):
		self.api_key = config["apiKey"]
		self.auth_domain = config["authDomain"]
		self.database_url = config["databaseURL"]
		self.storage_bucket = config["storageBucket"]

		self.credentials = None
		self.requests = requests.Session()

		if config.get("serviceAccount"):
			scopes = [
				'https://www.googleapis.com/auth/firebase.database',
				'https://www.googleapis.com/auth/userinfo.email',
				"https://www.googleapis.com/auth/cloud-platform"
			]
			service_account_type = type(config["serviceAccount"])

			if service_account_type is str:
				self.credentials = ServiceAccountCredentials.from_json_keyfile_name(config["serviceAccount"], scopes)
			if service_account_type is dict:
				self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(config["serviceAccount"], scopes)

		adapter = requests.adapters.HTTPAdapter(max_retries=3)

		for scheme in ('http://', 'https://'):
			self.requests.mount(scheme, adapter)

	def auth(self):
		return Auth(self.api_key, self.credentials, self.requests)

	def database(self):
		return Database(self.api_key, self.credentials, self.database_url, self.requests)

	def storage(self):
		return Storage(self.credentials, self.requests, self.storage_bucket)
