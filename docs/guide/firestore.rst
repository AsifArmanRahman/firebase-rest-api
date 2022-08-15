Firestore
=========

The firestore service allows you to run CRUD operations to your Firebase Firestore
Database.

.. code-block:: python

   # Create database instance
   fsdb = firebaseApp.firestore()
..

   .. note::
      Each of the following methods accepts a user token:
      ``get()``,  ``set()``, ``update()``, and ``delete()``.


Build Path
----------

You can build paths to your data by using the ``collection()`` and ``document()`` method.

.. code-block:: python

   fsdb.collection('Marvels').document('Movies')
   fsdb.collection('Marvels').document('Movies').collection('PhaseOne').document('2008')

..

      .. note::
         The methods available/used after ``collection()`` method and
         ``document()`` method are **NOT SAME**. Both method is a
         reference to different classes with different methods in them.


Save Data
---------

set
^^^

To store data in a collection named ``Marvels`` and a document inside
the collection named ``Movies``, use  ``set()`` method.

.. code-block:: python

   data = {
      "name": "Iron Man",
      "lead": {
         "name": "Robert Downey Jr."
      },
      'cast': ['Gwyneth Paltrow']
      'released': False,
      'prequel': None
   }

   fsdb.collection('Marvels').document('Movies').set(data)
..

   .. attention::
      Using this method on an existing document will overwrite the existing
      document.


add
^^^

To store data in a collection named ``Marvels`` within an auto
generated document ID, use ``add()`` method.

.. code-block:: python

   data = {
      "name": "Iron Man",
      "lead": {
         "name": "Robert Downey Jr."
      },
      'cast': ['Gwyneth Paltrow']
      'released': False,
      'prequel': None
   }

   id = fsdb.collection('Marvels').add(data)
..


Read Data
---------

|document-get|
^^^^^^^^^^^^^^

.. |document-get| replace::
   get

To read data from an existing document ``Movies`` of the collection
``Marvels``, use ``get()`` method.

.. code-block:: python

   fsdb.collection('Marvels').document('Movies').get()
..



It is possible to filter the data of an document to receive specific fields.

.. code-block:: python

   fsdb.collection('Marvels').document('Movies').get(field_paths=['lead.name', 'released'])

   # Output:
   # {'lead': {'name': "Robert Downey Jr."}, 'released': False}
..


|collection-get|
^^^^^^^^^^^^^^^^

.. |collection-get| replace::
      get

To fetch data regarding all existing document (document ID and the data
it contains) of an collection ``Marvels``, use ``get()`` method.

.. code-block:: python

   fsdb.collection('Marvels').get()
..

   .. warning::
      This ``get()`` method is different from the above stated one, and
      receives different parameters and returns different output.


list_of_documents
^^^^^^^^^^^^^^^^^

To fetch all existing document ID's in a collection ``Marvels``, use
``list_of_documents()`` method.

.. code-block:: python

   fsdb.collection('Marvels').list_of_documents()
..


Update Data
-----------

update
^^^^^^

To add more data to an existing document, use ``update()`` method.

.. code-block:: python

   # add new data to an existing document

   data = {
      'year': 2008,
   }

   fsdb.collection('Marvels').document('Movies').update(data)
..



To update existing data to an existing document, use ``update()`` method.

.. code-block:: python

   # update data of an existing document

   data = {
      'released': True,
   }

   fsdb.collection('Marvels').document('Movies').update(data)
..



To add an item to an array field in an existing document, use
``update()`` method.

.. code-block:: python

   from google.cloud.firestore import ArrayUnion
   data = {
      'cast': ArrayUnion(['Terrence Howard'])
   }

   fsdb.collection('Marvels').document('Movies').update(data)
..


Delete Data
-----------

|delete-update|
^^^^^^^^^^^^^^^

.. |delete-update| replace::
      update

To remove an field from an existing document, use ``update()`` method.

.. code-block:: python

   from google.cloud.firestore import DELETE_FIELD
   data = {
      'prequel': DELETE_FIELD
   }

   fsdb.collection('Marvels').document('Movies').update(data)
..



To remove an item to an array field in an existing document, use
``update()`` method.

.. code-block:: python

   from google.cloud.firestore import ArrayRemove
   data = {
      'cast': ArrayRemove(['Terrence Howard'])
   }

   fsdb.collection('Marvels').document('Movies').update(data)
..


delete
^^^^^^

To remove an existing document in a collection, use ``delete()``
method.

.. code-block:: python

   fsdb.collection('Marvels').document('Movies').delete()
..


Complex Queries
---------------

order_by
^^^^^^^^

To fetch documents with it's data in a collection ``Marvels``, ordered 
of field ``year``-s value.

.. code-block:: python

   fsdb.collection('Marvels').order_by('year').get()
..



To order the documents in descending order of field ``year``s value
, add ``direction`` keyword argument.

.. code-block:: python

   from google.cloud.firestore import Query

   fsdb.collection('Marvels').order_by('year', direction=Query.DESCENDING).get()
..


limit_to_first
^^^^^^^^^^^^^^

To limit the number of documents returned in a query to first *N*
documents, we use ``limit_to_first`` method.

.. code-block:: python

   docs = fsdb.collection('Marvels').order_by('year', direction='DESCENDING').limit_to_first(2).get()
..

   .. note::
      `limit_to_first` and `limit_to_last` are mutually
      exclusive. Setting `limit_to_first` will drop
      previously set `limit_to_last`.


limit_to_last
^^^^^^^^^^^^^

To limit the number of documents returned in a query to last *N*
documents, we use ``limit_to_last`` method.

.. code-block:: python

   docs = fsdb.collection('Marvels').order_by('year', direction='ASCENDING').limit_to_last(2).get()
..

   .. note::
      `limit_to_first` and `limit_to_last` are mutually
      exclusive. Setting `limit_to_first` will drop
      previously set `limit_to_last`.


start_at
^^^^^^^^

To fetch documents with field ``year`` with a ``2007`` or higher will
be fetched from a collection ``Marvels``, and anything before ``2007``
will be ignored.

.. code-block:: python

   docs = fsdb.collection('Marvels').order_by('year').start_at({'year': 2007}).get()
..


start_after
^^^^^^^^^^^

To fetch documents with field ``year`` with a value greater than
``2007`` will be fetched from a collection ``Marvels``, and any
document with a value ``2007`` or less will be ignored.

.. code-block:: python

   docs = fsdb.collection('Marvels').order_by('year').start_after({'year': 2007}).get()
..


end_at
^^^^^^

To fetch documents with field ``year`` with a ``2022`` or less will
be fetched from a collection ``Marvels``, and anything after ``2022``
will be ignored.

.. code-block:: python

   docs = fsdb.collection('Marvels').order_by('year').end_at({'year': 2022}).get()
..


end_before
^^^^^^^^^^

To fetch documents with field ``year`` with a value less than
``2023`` will be fetched from a collection ``Marvels``, and any
document with a value ``2023`` or greater will be ignored.

.. code-block:: python

   docs = fsdb.collection('Marvels').order_by('year').end_before({'year': 2007}).get()
..


offset
^^^^^^

To filter out the first *N* documents from a query in collection 
``Marvels``.

.. code-block:: python

   docs = fsdb.collection('Marvels').order_by('year').offset(5).get()
..


select
^^^^^^

To filter the fields ``lead.nam`` and ``released`` to be returned from
documents in collection ``Marvels``.

.. code-block:: python

   docs = fsdb.collection('Marvels').select(['lead.name', 'released']).get()
..


where
^^^^^

To fetch all documents and its data in a collection ``Marvels`` where
a field ``year`` exists with a value less than ``2008``.

.. code-block:: python

   fsdb.collection('Marvels').where('year', '<', 2008).get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a field ``year`` exists with a value less than equal to ``2008``.

.. code-block:: python

   fsdb.collection('Marvels').where('year', '<=', 2008).get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a field ``released`` exists with a value equal to ``True``.

.. code-block:: python

   fsdb.collection('Marvels').where('released', '==', True).get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a field ``released`` exists with a value not equal to ``False``.

.. code-block:: python

   fsdb.collection('Marvels').where('released', '!=', False).get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a field ``year`` exists with a value greater than equal to ``2008``.

.. code-block:: python

   fsdb.collection('Marvels').where('year', '>=', 2008).get()
..


To fetch all documents and its data in a collection ``Marvels`` where
a field ``year`` exists with a value greater than ``2008``.

.. code-block:: python

   fsdb.collection('Marvels').where('year', '>', 2008).get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a array field ``cast`` exists and contains a value ``Gwyneth Paltrow``.

.. code-block:: python

   fsdb.collection('Marvels').where('cast', 'array_contains', 'Gwyneth Paltrow').get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a array field ``cast`` exists and contains either ``Gwyneth Paltrow``
or ``Terrence Howard`` as a value.

.. code-block:: python

   fsdb.collection('Marvels').where('cast', 'array_contains_any', ['Gwyneth Paltrow', 'Terrence Howard']).get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a field ``lead.name`` exists with a value ``Robert Downey Jr.`` or
``Benedict Cumberbatch``.

.. code-block:: python

   fsdb.collection('Marvels').where('lead.name', 'in', ['Robert Downey Jr.', 'Benedict Cumberbatch']).get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a field ``lead.name`` exists without a value ``Robert Downey Jr.`` or
``Benedict Cumberbatch``.

.. code-block:: python

   fsdb.collection('Marvels').where('lead.name', 'not-in', ['Robert Downey Jr.', 'Benedict Cumberbatch']).get()
..



To fetch all documents and its data in a collection ``Marvels`` where
a array field ``cast`` exists with a value ``Gwyneth Paltrow``.

.. code-block:: python

   fsdb.collection('Marvels').where('cast', 'in', [['Gwyneth Paltrow']]).get()
..
