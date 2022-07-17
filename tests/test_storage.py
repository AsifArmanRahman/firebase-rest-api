#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import pytest


class TestStorage:

	def test_child(self, storage):
		assert storage.child('firebase-test-001')

	def test_put(self, storage):
		assert storage.child('uploaded-file.txt').put("tests/static/test-file.txt") is None

	def test_get_url(self, storage):
		assert storage.child('firebase-test-001').child('uploaded-file.txt').get_url(None)

	def test_delete(self, storage):
		assert storage.delete('firebase-test-001/uploaded-file.txt', None) is None

	def test_list_of_files(self, storage):
		assert storage.list_files()
