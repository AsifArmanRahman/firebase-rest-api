
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


"""
A simple python wrapper for Google's
`Firebase Authentication REST API`_

.. _Firebase Authentication REST API: https://firebase.google.com/docs/reference/rest/auth
"""

import json
import math
import pkce
import random
import datetime
import python_jwt as jwt
from hashlib import sha256
from jwcrypto.jwk import JWK
from urllib.parse import parse_qs
from google.auth.transport.requests import Request
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat

from firebase._exception import raise_detailed_error


class Auth:
	""" Firebase Authentication Service

	:type api_key: str
	:param api_key: ``apiKey`` from Firebase configuration

	:type credentials: :class:`~google.oauth2.service_account.Credentials`
	:param credentials: Service Account Credentials

	:type requests: :class:`~requests.Session`
	:param requests: Session to make HTTP requests

	:type client_secret: str or dict
	:param client_secret: (Optional) File path to or the dict object
		from social client secret file, defaults to :data:`None`.

	"""

	def __init__(self, api_key, credentials, requests, client_secret=None):
		""" Constructor method """

		self.api_key = api_key
		self.credentials = credentials
		self.requests = requests

		self.provider_id = None
		self.session_id = None
		self.__code_verifier = None
		self.__nonce = None

		if client_secret:
			self.client_secret = _load_client_secret(client_secret)

	def authenticate_login_with_google(self):
		""" Redirect the user to Google's OAuth 2.0 server to initiate 
		the authentication and authorization process.

		:return: Google Sign In URL
		:rtype: str
		"""
		return self.create_authentication_uri('google.com')

	def authenticate_login_with_facebook(self):
		""" Redirect the user to Facebook's OAuth 2.0 server to
		initiate the authentication and authorization process.

		:return: Facebook Sign In URL
		:rtype: str
		"""
		return self.create_authentication_uri('facebook.com')

	def create_authentication_uri(self, provider_id):
		""" Creates an authentication URI for the given social
		provider.

		| For more details:
		| |section-fetch-providers-for-email|_

		.. |section-fetch-providers-for-email| replace::
			Firebase Auth REST API | Fetch providers for email

		.. _section-fetch-providers-for-email:
			https://firebase.google.com/docs/reference/rest/auth#section-fetch-providers-for-email


		:type provider_id: str
		:param provider_id: The IdP ID. For white listed IdPs it's a
			short domain name e.g. 'google.com', 'aol.com', 'live.net'
			and 'yahoo.com'. For other OpenID IdPs it's the OP
			identifier.


		:return: The URI used by the IDP to authenticate the user.
		:rtype: str
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/createAuthUri?key={0}".format(self.api_key)

		data = {
			"clientId": self.client_secret['client_id'],
			"providerId": provider_id,
			"continueUri": self.client_secret['redirect_uris'][0],
		}

		self.__nonce = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(20))

		if provider_id == 'google.com':
			data['authFlowType'] = 'CODE_FLOW'
			data['customParameter'] = {"access_type": 'offline', "prompt": 'select_account', "include_granted_scopes": 'true', "nonce": self.__nonce}

		if provider_id == 'facebook.com':
			self.__code_verifier, code_challenge = pkce.generate_pkce_pair()
			data['oauthScope'] = 'openid'
			data['customParameter'] = {"code_challenge": code_challenge, "code_challenge_method": 'S256', "nonce": sha256(self.__nonce.encode('utf')).hexdigest()}

		headers = {"content-type": "application/json; charset=UTF-8"}
		request_object = self.requests.post(request_ref, headers=headers, json=data)

		raise_detailed_error(request_object)

		self.provider_id = provider_id
		self.session_id = request_object.json()['sessionId']

		return request_object.json()['authUri']

	def sign_in_with_email_and_password(self, email, password):
		""" Sign in a user with an email and password.

		| For more details:
		| `Firebase Auth REST API | section-sign-in-email-password`_

		.. _Firebase Auth REST API | section-sign-in-email-password: https://firebase.google.com/docs/reference/rest/auth#section-sign-in-email-password

		:type email: str
		:param email: The email the user is signing in with.

		:type password: str
		:param password: The password for the account.

		:return: UserInfo and Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return _token_expire_time(request_object.json())

	def sign_in_anonymous(self):
		""" Sign In Anonymously.

		| For more details:
		| `Firebase Auth REST API | section-sign-in-anonymously`_

		.. _Firebase Auth REST API | section-sign-in-anonymously: https://firebase.google.com/docs/reference/rest/auth#section-sign-in-anonymously

		:return: Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"returnSecureToken": True})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return _token_expire_time(request_object.json())

	def create_custom_token(self, uid, additional_claims=None, expiry_minutes=60):
		""" Create a Firebase Auth custom token.

		| For more details:
		| `Firebase Documentation | Create Custom tokens`_

		.. _Firebase Documentation | Create Custom tokens: https://firebase.google.com/docs/auth/admin/create-custom-tokens

		:type uid: str
		:param uid: The unique identifier of the user, must be a
			string, between 1-36 characters long.

		:type additional_claims:  dict or None
		:param additional_claims: Optional custom claims to include
			in the Security Rules ``auth`` / ``request.auth``
			variables.

		:type expiry_minutes:  int
		:param expiry_minutes: The time, in minutes since the UNIX
			epoch, at which the token expires.
			Default value is 60.

		:return: Firebase Auth custom token.
		:rtype: str
		"""

		service_account_email = self.credentials.service_account_email
		private_key = JWK.from_pem(self.credentials.signer._key.private_bytes(encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption()))

		payload = {
			"iss": service_account_email,
			"sub": service_account_email,
			"aud": "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit",
			"uid": uid
		}

		if additional_claims:
			payload["claims"] = additional_claims

		exp = datetime.timedelta(minutes=expiry_minutes)

		return jwt.generate_jwt(payload, private_key, "RS256", exp, other_headers={'kid': self.credentials.signer._key_id})

	def sign_in_with_custom_token(self, token):
		""" Exchange custom token for an ID and refresh token.

		| For more details:
		| `Firebase Auth REST API | section-verify-custom-token`_

		.. _Firebase Auth REST API | section-verify-custom-token : https://firebase.google.com/docs/reference/rest/auth#section-verify-custom-token

		:type token: str
		:param token: A Firebase Auth custom token from which to
			create an ID and refresh token pair.

		:return: Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={0}".format(self.api_key)  # noqa

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"returnSecureToken": True, "token": token})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return _token_expire_time(request_object.json())

	def refresh(self, refresh_token):
		""" Refresh a Firebase ID token.

		| For more details:
		| `Firebase Auth REST API | section-refresh-token`_

		.. _Firebase Auth REST API | section-refresh-token : https://firebase.google.com/docs/reference/rest/auth#section-refresh-token

		:type refresh_token: str
		:param refresh_token: A Firebase Auth refresh token.

		:return: New (Refreshed) Firebase Auth tokens for the account.
		:rtype: dict
		"""

		request_ref = "https://securetoken.googleapis.com/v1/token?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"grantType": "refresh_token", "refreshToken": refresh_token})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)
		request_object_json = request_object.json()

		# handle weirdly formatted response
		user = {
			"localId": request_object_json["user_id"],
			"idToken": request_object_json["id_token"],
			"refreshToken": request_object_json["refresh_token"],
			"expiresIn": request_object_json["expires_in"]
		}

		return _token_expire_time(user)

	def get_account_info(self, id_token):
		""" Fetch user's stored account information.

		| For more details:
		| `Firebase Auth REST API | section-get-account-info`_

		.. _Firebase Auth REST API | section-get-account-info : https://firebase.google.com/docs/reference/rest/auth#section-get-account-info

		:type id_token: str
		:param id_token: The Firebase ID token of the account.

		:return: The account info, associated with the given
			Firebase ID token.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"idToken": id_token})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

	def send_email_verification(self, id_token):
		""" Send an email verification to verify email ownership.

		| For more details:
		| `Firebase Auth REST API | section-send-email-verification`_

		.. _Firebase Auth REST API | section-send-email-verification : https://firebase.google.com/docs/reference/rest/auth#section-send-email-verification

		:type id_token: str
		:param id_token: The Firebase ID token of the user to verify.

		:return: The email of the account associated with Firebase ID
			token.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

	def send_password_reset_email(self, email):
		""" Send a password reset email.

		| For more details:
		| `Firebase Auth REST API | section-send-password-reset-email`_

		.. _Firebase Auth REST API | section-send-password-reset-email: https://firebase.google.com/docs/reference/rest/auth#section-send-password-reset-email

		:type email: str
		:param email: User's email address.

		:return: User's email address.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

	def verify_password_reset_code(self, reset_code, new_password):
		""" Reset password using code.

		| For more details:
		| `Firebase Auth REST API | #section-confirm-reset-password`_

		.. _Firebase Auth REST API | #section-confirm-reset-password: https://firebase.google.com/docs/reference/rest/auth#section-confirm-reset-password

		:type reset_code: str
		:param reset_code: The email action code sent to the user's
			email for resetting the password.

		:type new_password: str
		:param new_password: The user's new password.

		:return: User Email and Type of the email action code.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/resetPassword?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"oobCode": reset_code, "newPassword": new_password})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

	def create_user_with_email_and_password(self, email, password):
		""" Create a new user with email and password.

		| For more details:
		| `Firebase Auth REST API | section-create-email-password`_

		.. _Firebase Auth REST API | section-create-email-password: https://firebase.google.com/docs/reference/rest/auth#section-create-email-password

		:type email:  str
		:param email: The email for the user to create.

		:type password:  str
		:param password: The password for the user to create.

		:return: User Email and Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

	def delete_user_account(self, id_token):
		""" Delete an existing user.

		| For more details:
		| `Firebase Auth REST API | section-delete-account`_

		.. _Firebase Auth REST API | section-delete-account: https://firebase.google.com/docs/reference/rest/auth#section-delete-account

		:type id_token: str
		:param id_token: The Firebase ID token of the user to
			delete.
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"idToken": id_token})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

	def sign_in_with_oauth_credential(self, oauth2callback_url):
		""" Sign In With OAuth credential.

		| For more details:
		| |section-sign-in-with-oauth-credential|_

		.. |section-sign-in-with-oauth-credential| replace::
			Firebase Auth REST API | Sign in with OAuth credential

		.. _section-sign-in-with-oauth-credential:
			https://firebase.google.com/docs/reference/rest/auth#section-sign-in-with-oauth-credential


		:type oauth2callback_url: str
		:param oauth2callback_url: The URL redirected to after
			successful authorization from the provider.

		:return: User account info and Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyAssertion?key={0}".format(self.api_key)

		token = self._token_from_auth_url(oauth2callback_url)
		data = {
			'postBody': f"providerId={self.provider_id}&{token['type']}={token['value']}&nonce={self.__nonce}",
			'autoCreate': 'true',
			'requestUri': self.client_secret['redirect_uris'][0],
			'sessionId': self.session_id,
			'returnSecureToken': 'true',
			'returnRefreshToken': 'true',
			'returnIdpCredential': 'false',
		}

		headers = {"content-type": "application/json; charset=UTF-8"}
		request_object = self.requests.post(request_ref, headers=headers, json=data)

		raise_detailed_error(request_object)

		return _token_expire_time(request_object.json())

	def _token_from_auth_url(self, url):
		""" Fetch tokens using the authorization code from given URL.


		:type url: str
		:param url: The URL redirected to after successful
			authorization from the provider.


		:return: The OAuth credential (an ID token).
		:rtype: dict
		"""

		request_ref = _token_host(self.provider_id)

		auth_url_values = parse_qs(url[url.index('?') + 1:])

		data = {
			'client_id': self.client_secret['client_id'],
			'client_secret': self.client_secret['client_secret'],
			'code': auth_url_values['code'][0],
			'redirect_uri': self.client_secret['redirect_uris'][0],
		}

		if self.provider_id == 'google.com':
			data['grant_type'] = 'authorization_code'
		elif self.provider_id == 'facebook.com':
			data['code_verifier'] = self.__code_verifier

		headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return {
			'type': 'id_token',
			'value': request_object.json()['id_token'],
		}
	
	def change_email(self, id_token, email):
		""" Changes a user's email

		| For more details:
		| `Firebase Auth REST API | section-change-email`_

		.. _Firebase Auth REST API | section-change-email: https://firebase.google.com/docs/reference/rest/auth#section-change-email

		:type id_token: str
		:param id_token: A Firebase Auth ID token for the user.

		:type email: str
		:param email: User's new email.

		:return: UserInfo and Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"idToken": id_token, "email": email, "returnSecureToken": True})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()
	
	def change_password(self, id_token, password):
		""" Changes a user's password

		| For more details:
		| `Firebase Auth REST API | section-change-password`_

		.. _Firebase Auth REST API | section-change-password: https://firebase.google.com/docs/reference/rest/auth#section-change-password

		:type id_token: str
		:param id_token: A Firebase Auth ID token for the user.

		:type password: str
		:param password: User's new password.

		:return: UserInfo and Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"idToken": id_token, "password": password, "returnSecureToken": True})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

	def update_profile(self, id_token, display_name=None, photo_url=None, delete_attribute=None):
		""" Update a user's profile (display name / photo URL).

		| For more details:
		| `Firebase Auth REST API | section-update-profile`_

		.. _Firebase Auth REST API | section-update-profile: https://firebase.google.com/docs/reference/rest/auth#section-update-profile

		:type id_token: str
		:param id_token: A Firebase Auth ID token for the user.

		:type display_name: str or None
		:param display_name: User's new display name.

		:type photo_url: None or str
		:param photo_url: User's new photo url.

		:type delete_attribute: list[str] or None
		:param delete_attribute: List of attributes to delete,
			"DISPLAY_NAME" or "PHOTO_URL". This will nullify these
			values.

		:return: UserInfo and Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"idToken": id_token, "displayName": display_name, "photoURL": photo_url, "deleteAttribute": delete_attribute, "returnSecureToken": True})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

	def set_custom_user_claims(self, user_id, custom_claims):
		""" Add or remove custom claims from/to an existing user.

		| For more details:
		| `Firebase Auth REST API | Set and validate custom user claims`_

		.. _Firebase Auth REST API | Set and validate custom user claims: https://firebase.google.com/docs/auth/admin/custom-claims#set_and_validate_custom_user_claims_via_the_admin_sdk

		:type user_id: str
		:param user_id: Firebase User UID.

		:type custom_claims: dict
		:param custom_claims: Claims to add to that user's token.
		"""

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={0}".format(self.api_key)

		if not self.credentials.valid:
			self.credentials.refresh(Request())

		access_token = self.credentials.token

		headers = {"Authorization": "Bearer " + access_token, "content-type": "application/json; charset=UTF-8"}

		data = json.dumps({"localId": user_id, "customAttributes":json.dumps(custom_claims), "returnSecureToken": False})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

	def verify_id_token(self, id_token):
		""" Decode Firebase Auth ID token.

		| For more details:
		| `Firebase Authentication | Verify ID tokens using a third-party JWT library`_

		.. _Firebase Authentication | Verify ID tokens using a third-party JWT library: https://firebase.google.com/docs/auth/admin/verify-id-tokens#verify_id_tokens_using_a_third-party_jwt_library

		:type id_token: str
		:param id_token: A Firebase Auth ID token for the user.

		:return: Decoded claims of Firebase Auth ID token.
		:rtype: dict
		"""

		header, _ = jwt.process_jwt(id_token)

		response = self.requests.get('https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com')

		pub_pem = response.json()[header['kid']]

		pub_key = JWK.from_pem(bytes(pub_pem.encode('utf-8')))
		_, claims = jwt.verify_jwt(id_token, pub_key, [header['alg']], checks_optional=True)

		return claims


def _load_client_secret(secret):
	""" Load social providers' client secret from file if file path
	provided.

	This function also restructures the dict object to make it
	compatible for usage.


	:type secret: str or dict
	:param secret: File path to or the dict object from social client
		secret file.

	:return: social client secret
	:rtype: dict
	"""

	if type(secret) is str:
		with open(secret) as file:
			secret = json.load(file)

	# Google client secrets are stored within 'web' key
	# We will remove the key, and replace it with the dict type value of it
	if secret.get('web'):
		secret = secret['web']

	return secret


def _token_expire_time(user):
	""" Adds expire time of the token in the token dictionary.

	For safety purposes, token is set to expire after 59mins instead
	of an hour expiry time when received.

	:type user: dict
	:param user: The token dictionary received after signing in users.
	
	:return: Token dictionary with an ``expiresAt`` key.
	:rtype: dict
	"""

	user['expiresAt'] = math.floor(datetime.datetime.today().timestamp() + int(user.get('expiresIn', 3600)) - 60)

	return user


def _token_host(provider):
	if provider == 'google.com':
		return 'https://www.googleapis.com/oauth2/v4/token'

	elif provider == 'facebook.com':
		return 'https://graph.facebook.com/v14.0/oauth/access_token'
