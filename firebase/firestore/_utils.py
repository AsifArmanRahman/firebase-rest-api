
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from base64 import b64decode
from google.cloud.firestore_v1._helpers import GeoPoint
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


def _from_datastore(data):
	""" Converts a map of Firestore ``data``-s to Python dictionary.


	:type data: dict
	:param data: A map of firestore data.


	:return: A dictionary of native Python values converted
		from the ``data``.
	:rtype: dict
	"""

	data_to_restructure = data['fields']

	for key, val in data_to_restructure.items():

		if val.get('mapValue'):
			data_to_restructure[key] = _from_datastore(val['mapValue'])

		elif val.get('arrayValue'):
			arr = []

			for x in val['arrayValue']['values']:
				arr.append(_decode_datastore(x))

			data_to_restructure[key] = arr

		else:
			data_to_restructure[key] = _decode_datastore(val)

	return data_to_restructure


def _decode_datastore(value):
	""" Converts a Firestore ``value`` to a native Python value.


	:type value: dict
	:param value: A Firestore data to be decoded / parsed /
		converted.


	:return: A native Python value converted from the ``value``.
	:rtype: :data:`None` or :class:`bool` or :class:`bytes`
		or :class:`int` or :class:`float` or :class:`str` or
		:class:`dict` or
		:class:`~google.api_core.datetime_helpers.DatetimeWithNanoseconds`
		or  :class:`~google.cloud.firestore_v1._helpers.GeoPoint`.

	:raises TypeError: For value types that are unsupported.
	"""

	if value.get('nullValue', False) is None:
		return value['nullValue']

	elif value.get('booleanValue') is not None:
		return bool(value['booleanValue'])

	elif value.get('bytesValue'):
		return b64decode(value['bytesValue'].encode('utf-8'))

	elif value.get('integerValue'):
		return int(value['integerValue'])

	elif value.get('doubleValue'):
		return float(value['doubleValue'])

	elif value.get('stringValue'):
		return str(value['stringValue'])

	elif value.get('mapValue'):
		return _from_datastore(value['mapValue'])

	elif value.get('timestampValue'):
		return DatetimeWithNanoseconds.from_rfc3339(value['timestampValue'])

	elif value.get('geoPointValue'):
		return GeoPoint(float(value['timestampValue']['latitude']), float(value['timestampValue']['longitude']))

	else:
		raise TypeError("Cannot convert to a Python Value", value, "Invalid type", type(value))
