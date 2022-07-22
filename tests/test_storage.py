#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------
import os.path

import pytest


class TestStorage:

	test_user = None

	def test_user_for_storage(self, auth):
		self.__class__.test_user = auth.sign_in_anonymous()
		assert self.__class__.test_user is not None

	def test_child(self, storage):
		assert storage.child('firebase-test-001')

	def test_put(self, storage):
		assert storage.child('uploaded-file.txt').put("tests/static/test-file.txt", self.__class__.test_user.get('idToken'))

	def test_get_url(self, storage):
		assert storage.child('firebase-test-001').child('uploaded-file.txt').get_url(self.__class__.test_user.get('idToken'))

	def test_download(self, storage):
		assert storage.child('firebase-test-001').child('uploaded-file.txt').download('tests/static/downloaded.txt', self.__class__.test_user.get('idToken')) is None
		assert os.path.exists('tests/static/downloaded.txt')

	def test_delete(self, storage):
		os.remove('tests/static/downloaded.txt')
		assert storage.child('firebase-test-001/uploaded-file.txt').delete(self.__class__.test_user.get('idToken')) is None

	def test_list_of_files(self, storage):
		with pytest.raises(AttributeError) as exc_info:
			storage.list_files()
		assert 'bucket' in str(exc_info.value)

	def test_clean_user(self, auth):
		assert auth.delete_user_account(self.__class__.test_user.get('idToken'))


class TestStorageAdmin:

	def test_child(self, storage_admin):
		assert storage_admin.child('firebase-test-001')

	def test_put(self, storage_admin):
		assert storage_admin.child('uploaded-file.txt').put("tests/static/test-file.txt") is None

	def test_get_url(self, storage_admin):
		assert storage_admin.child('firebase-test-001').child('uploaded-file.txt').get_url(None)

	def test_download(self, storage_admin):
		assert storage_admin.child('firebase-test-001').child('uploaded-file.txt').download('tests/static/downloaded.txt') is None
		assert os.path.exists('tests/static/downloaded.txt')

	def test_delete(self, storage_admin):
		os.remove('tests/static/downloaded.txt')
		assert storage_admin.child('firebase-test-001/uploaded-file.txt').delete() is None

	def test_list_of_files(self, storage_admin):
		assert storage_admin.list_files()
