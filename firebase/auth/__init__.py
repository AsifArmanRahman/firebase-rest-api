
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


"""
A simple python wrapper for Google's
`Firebase Authentication REST API`_

.. _Firebase Authentication REST API: https://firebase.google.com/docs/reference/rest/auth
"""

import json
import datetime
import python_jwt as jwt
import jwcrypto.jwk as jwk

from firebase._exception import raise_detailed_error


class Auth:
	""" Firebase Authentication Service

	:type api_key: str
	:param api_key: ``apiKey`` from Firebase configuration

	:type credentials: :class:`~oauth2client.service_account.ServiceAccountCredentials`
	:param credentials: Service Account Credentials

	:type requests: :class:`~requests.Session`
	:param requests: Session to make HTTP requests
	"""

	def __init__(self, api_key, credentials, requests):
		""" Constructor method """

		self.api_key = api_key
		self.credentials = credentials
		self.requests = requests

		self.current_user = None

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
		self.current_user = request_object.json()

		return request_object.json()

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
		self.current_user = request_object.json()

		return request_object.json()

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
		private_key = jwk.JWK.from_pem(self.credentials._private_key_pkcs8_pem.encode('utf-8'))

		payload = {
			"iss": service_account_email,
			"sub": service_account_email,
			"aud": "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit",
			"uid": uid
		}

		if additional_claims:
			payload["claims"] = additional_claims

		exp = datetime.timedelta(minutes=expiry_minutes)

		return jwt.generate_jwt(payload, private_key, "RS256", exp, other_headers={'kid': self.credentials._private_key_id})

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

		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={0}".format(self.api_key)	# noqa

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"returnSecureToken": True, "token": token})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()

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
			"userId": request_object_json["user_id"],
			"idToken": request_object_json["id_token"],
			"refreshToken": request_object_json["refresh_token"]
		}

		return user

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
		:param delete_attribute: List of attributes

			to delete, "DISPLAY_NAME" or "PHOTO_URL". This will nullify
			these values.

		:return: UserInfo and Firebase Auth Tokens.
		:rtype: dict
		"""

		request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:update?key={0}".format(self.api_key)

		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"idToken": id_token, "displayName": display_name, "photoURL": photo_url, "deleteAttribute": delete_attribute, "returnSecureToken": True})
		request_object = self.requests.post(request_ref, headers=headers, data=data)

		raise_detailed_error(request_object)

		return request_object.json()
