Storage
=======

The storage service allows you to upload files (eg. text, image,
video) to Firebase.

child
-----

Just like with the Database service, you can build paths to your data
with the Storage service.

.. code-block:: python

   storage.child("images/example.jpg")
..

put
---

The put method takes the path to the local file and an optional user
token.

.. code-block:: python

   storage = firebaseApp.storage()
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

   storage.child("images/example.jpg").download("downloaded.jpg")
..

get_url
-------

The get_url method takes the path to the saved database file and user
token which returns the storage url.

.. code-block:: python

   storage.child("images/example.jpg").get_url(user["idToken"])
   # https://firebasestorage.googleapis.com/v0/b/storage-url.appspot.com/o/images%2Fexample.jpg?alt=media
..

delete
------

The delete method takes the path to the saved database file and user
token.

.. code-block:: python

   storage.delete("images/example.jpg",user["idToken"])
..
