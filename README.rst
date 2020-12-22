# Kosher Pickles

.. -*- mode: rst -*-
.. role:: green

.. image:: assets/kosher_pickle_logo.png
  :target: https://github.com/ForestMars/Kosher

`Kosher Pickles is an encryption model for securing serialized objects. ``


Installation
------------

Dependencies
~~~~~~~~~~~~

- Crypto
- cryptography
- pickle

=======


Installation
~~~~~~~~~~~~~~~~~

Using ``pip``   ::

    pip install -U kosher

conda package is in the works.



Development
-----------

It would be great to see more contributers to Kosher Pickles. We welcome any feature requests, and of course, pull requests.
In particular, if you are interested in expanding test coverage, this is obivious very important for an encryption module.



Source code
~~~~~~~~~~~

To check out the latest version for development or other use::

    git clone https://github.com/forestmars/kosher


Supported Standards
~~~~~~~~~~~

Kosher Pickles currently supports AES and Fernet.

The included AES implementation defaults to CBF (Cipher feedback) block cipher mode mode.

Fernet also uses 128-bit AES, but in CBC mode with PKCS7 padding, and HMAC using SHA256 for authentication.


Testing
~~~~~~~

Currently using Nose2 for test runner. To run the test suite make sure you have Node2 installed and issue the command::


Project History
---------------

Based on a discussion at PyCon about the need to encrypted pickles in general, then created to meet financial company compliance requirements.


Roadmap
~~~~~~~
* Add support for AES-192 and AES-256.
* Add support for Galois/Counter Mode (GCM)


Additional Resources
---------------

https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/archived-crypto-projects/aes-development
