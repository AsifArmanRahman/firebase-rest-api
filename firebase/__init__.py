
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from .auth import Auth
from .storage import Storage
from .database import Database
from ._custom_requests import _custom_request
from ._service_account_credentials import _service_account_creds_from_secret


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
		self.requests = _custom_request()

		if config.get("serviceAccount"):
			self.credentials = _service_account_creds_from_secret(config['serviceAccount'])

	def auth(self):
		return Auth(self.api_key, self.credentials, self.requests)

	def database(self):
		return Database(self.api_key, self.credentials, self.database_url, self.requests)

	def storage(self):
		return Storage(self.credentials, self.requests, self.storage_bucket)
