
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import pytest
import requests.exceptions


class TestAuth:

	user = None
	anonymous_user = None

	def test_sign_in_with_non_existing_account_email_and_password(self, auth, email, password):
		with pytest.raises(requests.exceptions.HTTPError) as exc_info:
			auth.sign_in_with_email_and_password(email, password)
		assert "EMAIL_NOT_FOUND" in str(exc_info.value)

	def test_create_user_with_email_and_password(self, auth, email, password):
		assert auth.create_user_with_email_and_password(email, password)

	def test_create_user_with_existing_email_and_password(self, auth, email, password):
		with pytest.raises(requests.exceptions.HTTPError) as exc_info:
			auth.create_user_with_email_and_password(email, password)
		assert "EMAIL_EXISTS" in str(exc_info.value)

	def test_sign_in_with_email_and_wrong_password(self, auth, email):
		with pytest.raises(requests.exceptions.HTTPError) as exc_info:
			auth.sign_in_with_email_and_password(email, 'WrongPassword123')
		assert "INVALID_PASSWORD" in str(exc_info.value)

	def test_sign_in_with_email_and_password(self, auth, email, password):
		user = auth.sign_in_with_email_and_password(email, password)
		self.__class__.user = user
		assert user

	def test_sign_in_anonymous(self, auth):
		user = auth.sign_in_anonymous()
		self.__class__.anonymous_user = user
		assert user

	def test_create_custom_token(self, auth):
		with pytest.raises(AttributeError):
			auth.create_custom_token('CreateCustomToken1')

	def test_create_custom_token_with_claims(self, auth):
		with pytest.raises(AttributeError):
			auth.create_custom_token('CreateCustomToken2', {'premium': True})

	def test_sign_in_with_custom_token(self, auth):
		with pytest.raises(requests.exceptions.HTTPError):
			auth.sign_in_with_custom_token(None)

	def test_refresh(self, auth):
		assert auth.refresh(self.__class__.user.get('refreshToken'))

	def test_get_account_info(self, auth):
		assert auth.get_account_info(self.__class__.user.get('idToken'))

	def test_send_email_verification(self, auth):
		assert auth.send_email_verification(self.__class__.user.get('idToken'))

	def test_send_password_reset_email(self, auth):
		assert auth.send_password_reset_email(self.__class__.user.get('email'))

	@pytest.mark.xfail
	def test_verify_password_reset_code(self, auth):
		assert auth.verify_password_reset_code('123456', 'NewTestPassword123')


	def test_change_email(self, auth, email_2, password):
		user = auth.change_email(self.__class__.user.get('idToken'), email_2)
		self.__class__.user = None

		assert user
		assert self.__class__.user is None

		user = auth.sign_in_with_email_and_password(email_2, password)
		self.__class__.user = user

		assert user
		assert self.__class__.user.get('email') == email_2

	def test_change_password(self, auth,email_2, password_2):
		user = auth.change_password(self.__class__.user.get('idToken'), password_2)
		self.__class__.user = None

		assert user
		assert self.__class__.user is None

		user = auth.sign_in_with_email_and_password(email_2, password_2)
		self.__class__.user = user

		assert user

	def test_update_profile_display_name(self, auth):
		new_name = 'Test User'
		user = auth.update_profile(self.__class__.user.get('idToken'), display_name=new_name)
		assert user
		assert new_name == user['displayName']

	def test_set_custom_user_claims(self, auth):
		with pytest.raises(AttributeError) as exc_info:
			auth.set_custom_user_claims(self.__class__.user.get('localId'), {'premium': True})
			auth.set_custom_user_claims(self.__class__.anonymous_user.get('localId'), {'premium': True})

		assert "'NoneType' object has no attribute 'valid'" in str(exc_info.value)

	def test_verify_id_token(self, auth):
		with pytest.raises(KeyError) as exc_info:
			auth.verify_id_token(self.__class__.user.get('idToken'))['premium'] is True
		assert "'premium'" in str(exc_info.value)

		with pytest.raises(KeyError) as exc_info:
			auth.verify_id_token(self.__class__.anonymous_user.get('idToken'))['premium'] is True
		assert "'premium'" in str(exc_info.value)

	def test_delete_user_account(self, auth):
		assert auth.delete_user_account(self.__class__.user.get('idToken'))
		assert auth.delete_user_account(self.__class__.anonymous_user.get('idToken'))


class TestAuthAdmin:

	user = None
	anonymous_user = None
	custom_token = None
	custom_token_with_claims = None
	custom_user = None
	custom_user_with_claims = None

	def test_sign_in_with_non_existing_account_email_and_password(self, auth_admin, email, password):
		with pytest.raises(requests.exceptions.HTTPError) as exc_info:
			auth_admin.sign_in_with_email_and_password(email, password)
		assert "EMAIL_NOT_FOUND" in str(exc_info.value)

	def test_create_user_with_email_and_password(self, auth_admin, email, password):
		assert auth_admin.create_user_with_email_and_password(email, password)

	def test_create_user_with_existing_email_and_password(self, auth_admin, email, password):
		with pytest.raises(requests.exceptions.HTTPError) as exc_info:
			auth_admin.create_user_with_email_and_password(email, password)
		assert "EMAIL_EXISTS" in str(exc_info.value)

	def test_sign_in_with_email_and_wrong_password(self, auth_admin, email):
		with pytest.raises(requests.exceptions.HTTPError) as exc_info:
			auth_admin.sign_in_with_email_and_password(email, 'WrongPassword123')
		assert "INVALID_PASSWORD" in str(exc_info.value)

	def test_sign_in_with_email_and_password(self, auth_admin, email, password):
		user = auth_admin.sign_in_with_email_and_password(email, password)
		self.__class__.user = user
		assert user

	def test_sign_in_anonymous(self, auth_admin):
		user = auth_admin.sign_in_anonymous()
		self.__class__.anonymous_user = user
		assert user

	def test_create_custom_token(self, auth_admin):
		token = auth_admin.create_custom_token('CreateCustomToken1')
		self.__class__.custom_token = token
		assert token

	def test_create_custom_token_with_claims(self, auth_admin):
		token = auth_admin.create_custom_token('CreateCustomToken2', {'premium': True})
		self.__class__.custom_token_with_claims = token
		assert token

	def test_sign_in_with_custom_token(self, auth_admin):
		user1 = auth_admin.sign_in_with_custom_token(self.__class__.custom_token)
		user2 = auth_admin.sign_in_with_custom_token(self.__class__.custom_token_with_claims)

		self.__class__.custom_user = user1
		self.__class__.custom_user_with_claims = user2

		assert user1
		assert user2

	def test_get_account_info(self, auth_admin):
		assert auth_admin.get_account_info(self.__class__.user.get('idToken'))

	def test_send_email_verification(self, auth_admin):
		assert auth_admin.send_email_verification(self.__class__.user.get('idToken'))

	def test_send_password_reset_email(self, auth_admin):
		assert auth_admin.send_password_reset_email(self.__class__.user.get('email'))

	@pytest.mark.xfail
	def test_verify_password_reset_code(self, auth_admin):
		assert auth_admin.verify_password_reset_code('123456', 'NewTestPassword123')

	def test_update_profile_display_name(self, auth_admin):
		new_name = 'Test User'
		user = auth_admin.update_profile(self.__class__.user.get('idToken'), display_name=new_name)
		assert user
		assert new_name == user['displayName']

	def test_set_custom_user_claims(self, auth_admin):
		auth_admin.set_custom_user_claims(self.__class__.user.get('localId'), {'premium': True})
		auth_admin.set_custom_user_claims(self.__class__.anonymous_user.get('localId'), {'premium': True})

	def test_refresh(self, auth_admin):
		self.__class__.user = auth_admin.refresh(self.__class__.user.get('refreshToken'))
		self.__class__.custom_user = auth_admin.refresh(self.__class__.custom_user.get('refreshToken'))
		self.__class__.anonymous_user = auth_admin.refresh(self.__class__.anonymous_user.get('refreshToken'))

	def test_verify_id_token(self, auth_admin):
		assert auth_admin.verify_id_token(self.__class__.user.get('idToken'))['premium'] is True
		assert auth_admin.verify_id_token(self.__class__.anonymous_user.get('idToken'))['premium'] is True
		assert auth_admin.verify_id_token(self.__class__.custom_user_with_claims.get('idToken'))['premium'] is True

		with pytest.raises(KeyError) as exc_info:
			auth_admin.verify_id_token(self.__class__.custom_user.get('idToken'))['premium'] is True
		assert "'premium'" in str(exc_info.value)

	def test_delete_user_account(self, auth_admin):
		assert auth_admin.delete_user_account(self.__class__.user.get('idToken'))
		assert auth_admin.delete_user_account(self.__class__.anonymous_user.get('idToken'))
		assert auth_admin.delete_user_account(self.__class__.custom_user.get('idToken'))
		assert auth_admin.delete_user_account(self.__class__.custom_user_with_claims.get('idToken'))
