
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from oauth2client.service_account import ServiceAccountCredentials


def _service_account_creds_from_secret(service_account_secret):
	""" Service Account Credentials from Service Account Secrets.

	File path of the service account secret file
	in json format can  also be passed as the value
	of the parameter `service_account_secret`.

	:param service_account_secret: Service Account Secret Key from Firebase Console.
	:type service_account_secret: dict | str
	:return: Service Account Credentials
	:rtype: ServiceAccountCredentials
	"""

	credentials = None
	scopes = [
		'https://www.googleapis.com/auth/firebase.database',
		'https://www.googleapis.com/auth/userinfo.email',
		"https://www.googleapis.com/auth/cloud-platform"
	]

	if type(service_account_secret) is str:
		credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account_secret, scopes)
	if type(service_account_secret) is dict:
		credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_secret, scopes)

	return credentials
