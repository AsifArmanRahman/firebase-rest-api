
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import pytest


class TestAuth:

	user = None
	anonymous_user = None
	custom_token = None
	custom_token_with_claims = None
	custom_user = None
	custom_user_with_claims = None

	@pytest.mark.xfail
	def test_sign_in_with_non_existing_account_email_and_password(self, auth, email, password):
		assert auth.sign_in_with_email_and_password(email, password)

	def test_create_user_with_email_and_password(self, auth, email, password):
		assert auth.create_user_with_email_and_password(email, password)

	@pytest.mark.xfail
	def test_create_user_with_existing_email_and_password(self, auth, email, password):
		assert auth.create_user_with_email_and_password(email, password)

	@pytest.mark.xfail
	def test_sign_in_with_email_and_wrong_password(self, auth, email):
		assert auth.sign_in_with_email_and_password(email, 'WrongPassword123')

	def test_sign_in_with_email_and_password(self, auth, email, password):
		user = auth.sign_in_with_email_and_password(email, password)
		self.__class__.user = user
		assert user

	def test_sign_in_anonymous(self, auth):
		user = auth.sign_in_anonymous()
		self.__class__.anonymous_user = user
		assert user

	def test_create_custom_token(self, auth):
		token = auth.create_custom_token('CreateCustomToken1')
		self.__class__.custom_token = token
		assert token

	def test_create_custom_token_with_claims(self, auth):
		token = auth.create_custom_token('CreateCustomToken2', {'premium': True})
		self.__class__.custom_token_with_claims = token
		assert token

	def test_sign_in_with_custom_token(self, auth):
		user1 = auth.sign_in_with_custom_token(self.__class__.custom_token)
		user2 = auth.sign_in_with_custom_token(self.__class__.custom_token_with_claims)

		self.__class__.custom_user = user1
		self.__class__.custom_user_with_claims = user2

		assert user1
		assert user2

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

	def test_update_profile_display_name(self, auth):
		assert auth.update_profile(self.__class__.user.get('idToken'), display_name='Test User')

	def test_delete_user_account(self, auth):
		assert auth.delete_user_account(self.__class__.user.get('idToken'))
		assert auth.delete_user_account(self.__class__.anonymous_user.get('idToken'))
		assert auth.delete_user_account(self.__class__.custom_user.get('idToken'))
		assert auth.delete_user_account(self.__class__.custom_user_with_claims.get('idToken'))
