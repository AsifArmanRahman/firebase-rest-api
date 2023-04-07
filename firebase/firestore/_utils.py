
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from datetime import datetime
from base64 import b64encode, b64decode
from google.protobuf.json_format import MessageToDict
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

		if isinstance(val.get('mapValue'), dict):

			if val['mapValue'].get('fields', False):
				data_to_restructure[key] = _from_datastore(val['mapValue'])
			else:
				data_to_restructure[key] = {}

		elif isinstance(val.get('arrayValue'), dict):
			arr = []

			if val['arrayValue'].get('values'):
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

	elif isinstance(value.get('stringValue'), str):
		return str(value['stringValue'])

	elif value.get('mapValue'):
		return _from_datastore(value['mapValue'])

	elif value.get('timestampValue'):
		return DatetimeWithNanoseconds.from_rfc3339(value['timestampValue'])

	elif value.get('geoPointValue'):
		return GeoPoint(float(value['timestampValue']['latitude']), float(value['timestampValue']['longitude']))

	else:
		raise TypeError("Cannot convert to a Python Value", value, "Invalid type", type(value))


def _to_datastore(data):
	""" Converts a Python dictionary ``data``-s to map of Firestore.


	:type data: dict
	:param data: A Python dictionary containing data.


	:return: A map of Firebase values converted from the ``data``.
	:rtype: dict

	:raises ValueError: Raised when a key in the python dictionary is
		Non-alphanum char without *`* (ticks) at start and end.
	"""

	restructured_data = {}

	for key, val in data.items():

		if ' ' in key and (not key.startswith('`') or not key.endswith('`')):
			raise ValueError(f'Non-alphanum char in element with leading alpha: {key}')

		key = str(key)

		if isinstance(val, dict):
			restructured_data[key] = {'mapValue': _to_datastore(val)}

		elif isinstance(val, list):
			arr = []

			for x in val:
				arr.append(_encode_datastore_value(x))

			restructured_data[key] = {'arrayValue': {'values': arr}}

		else:
			restructured_data[key] = _encode_datastore_value(val)

	return {'fields': restructured_data}


def _encode_datastore_value(value):
	""" Converts a Python ``value`` to a Firebase value.


	:type value: :data:`None` or :class:`bool` or :class:`bytes`
		or :class:`int` or :class:`float` or :class:`str` or
		:class:`dict` or :class:`~datetime.datetime` or
		:class:`~google.api_core.datetime_helpers.DatetimeWithNanoseconds`
		or  :class:`~google.cloud.firestore_v1._helpers.GeoPoint`.
	:param value: A Python data to be encoded/converted to Firebase.


	:return: A Firebase value converted from ``value``.
	:rtype: dict

	:raises TypeError: Raised when unsupported data type given.
	"""

	if value is None:
		return {'nullValue': value}

	elif isinstance(value, bytes):
		return {'bytesValue': b64encode(value).decode('utf-8')}

	elif isinstance(value, bool):
		return {'booleanValue': value}

	elif isinstance(value, int):
		return {'integerValue': value}

	elif isinstance(value, float):
		return {'doubleValue': value}

	elif isinstance(value, str):
		return {'stringValue': value}

	elif isinstance(value, dict):
		return {'mapValue': _to_datastore(value)}

	elif isinstance(value, datetime):
		return {'timestampValue': value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}

	elif isinstance(value, DatetimeWithNanoseconds):
		return {'timestampValue': value.rfc3339()}

	elif isinstance(value, GeoPoint):
		return {'geoPointValue': MessageToDict(value.to_protobuf())}
	else:

		raise TypeError("Cannot convert to a Firestore Value", value, "Invalid type", type(value))
