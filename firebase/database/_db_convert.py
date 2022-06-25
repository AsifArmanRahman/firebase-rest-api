
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from collections import OrderedDict


class FirebaseKeyValue:

	def __init__(self, item):
		self.item = item

	def val(self):
		return self.item[1]

	def key(self):
		return self.item[0]


class FirebaseResponse:

	def __init__(self, firebases, query_key):
		self.firebases = firebases
		self.query_key = query_key

	def __getitem__(self, index):
		return self.firebases[index]

	def val(self):
		if isinstance(self.firebases, list):

			# unpack firebases into OrderedDict
			firebase_list = []

			# if firebase response was a list
			if isinstance(self.firebases[0].key(), int):

				for firebase in self.firebases:
					firebase_list.append(firebase.val())

				return firebase_list

			# if firebase response was a dict with keys
			for firebase in self.firebases:
				firebase_list.append((firebase.key(), firebase.val()))

			return OrderedDict(firebase_list)

		else:

			return self.firebases

	def key(self):
		return self.query_key

	def each(self):
		if isinstance(self.firebases, list):
			return self.firebases


def convert_to_firebase(items):
	firebase_list = []

	for item in items:
		firebase_list.append(FirebaseKeyValue(item))

	return firebase_list


def convert_list_to_firebase(items):
	firebase_list = []

	for item in items:
		firebase_list.append(FirebaseKeyValue([items.index(item), item]))

	return firebase_list
