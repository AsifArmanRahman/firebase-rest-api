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

Save Data
---------

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


Read Data
---------

To read data from an existing document of an collection, use ``get()`` method.

.. code-block:: python

   fsdb.collection('Marvels').document('Movies').get()
..



It is possible to filter the data of an document to receive specific fields.

.. code-block:: python

   fsdb.collection('Marvels').document('Movies').get(field_paths=['lead.name', 'released'])

   # Output:
   # {'lead': {'name': "Robert Downey Jr."}, 'released': False}
..



Update Data
-----------

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



To remove an existing document in a collection, use ``delete()``
method.

.. code-block:: python

   fsdb.collection('Marvels').document('Movies').delete()
..
