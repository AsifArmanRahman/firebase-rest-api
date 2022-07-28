
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from google.oauth2.service_account import Credentials


def _service_account_creds_from_secret(service_account_secret):
	""" Service Account Credentials from Service Account Secrets.

	File path of the service account secret file
	in json format can  also be passed as the value
	of the parameter `service_account_secret`.

	:param service_account_secret: Service Account Secret Key from Firebase Console.
	:type service_account_secret: dict | str
	:return: Service Account Credentials
	:rtype: :class:`~google.oauth2.service_account.Credentials`
	"""

	credentials = None
	scopes = [
		'https://www.googleapis.com/auth/firebase.database',
		"https://www.googleapis.com/auth/datastore",
		'https://www.googleapis.com/auth/userinfo.email',
		"https://www.googleapis.com/auth/cloud-platform"
	]

	if type(service_account_secret) is str:
		credentials = Credentials.from_service_account_file(service_account_secret, scopes=scopes)
	if type(service_account_secret) is dict:
		credentials = Credentials.from_service_account_info(service_account_secret, scopes=scopes)

	return credentials
