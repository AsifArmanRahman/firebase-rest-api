Storage
=======

The storage service allows you to upload files (eg. text, image,
video) to Firebase Storage.

.. code-block:: python

   # Create storage instance
   storage = firebaseApp.storage()
..


child
-----

Just like with the Database service, you can build paths to your data
with the Storage service.

.. code-block:: python

   storage.child("images/example.jpg")

   # Alternative ways
   storage.child("images").child("example.jpg")
   storage.child("images", "example.jpg")
..

put
---

The put method takes the path to the local file and an optional user
token.

.. code-block:: python

   # as admin
   storage.child("images/example.jpg").put("example2.jpg")

   # as user
   storage.child("images/example.jpg").put("example2.jpg", user['idToken'])
..

download
--------

The download method takes the path to the saved database file and the
name you want the downloaded file to have.

.. code-block:: python

  # as admin
   storage.child("images/example.jpg").download("downloaded.jpg")

   # as user
   storage.child("images/example.jpg").download("downloaded.jpg", user['idToken'])
..

get_url
-------

The get_url method takes the path to the saved database file and user
token which returns the storage url.

.. code-block:: python

   # as admin
   storage.child("images/example.jpg").get_url()

   # as admin with expiration time for link to expire
   storage.child("images/example.jpg").get_url(expiration_hour=12)

   # as user
   storage.child("images/example.jpg").get_url(user["idToken"])

   # returned URL example:
   # https://firebasestorage.googleapis.com/v0/b/storage-url.appspot.com/o/images%2Fexample.jpg?alt=media&token=$token
..

delete
------

The delete method takes the path to the saved database file and user
token.

.. code-block:: python

   # as admin
   storage.child("images/example.jpg").delete()

   # as user
   storage.child("images/example.jpg").delete(user["idToken"])
..

list_of_files
-------------

The list_of_files method works only if used under admin credentials.

.. code-block:: python

   # as admin
   storage.list_of_files()
..
