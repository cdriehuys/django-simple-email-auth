########################
Django Simple Email Auth
########################

.. image:: https://img.shields.io/travis/com/cdriehuys/django-simple-email-auth/master
   :alt: Travis CI Build Status
   :target: https://travis-ci.com/cdriehuys/django-simple-email-auth

.. image:: https://img.shields.io/codecov/c/github/cdriehuys/django-simple-email-auth/master
   :alt: Code Coverage
   :target: https://codecov.io/github/cdriehuys/django-simple-email-auth

.. image:: https://img.shields.io/pypi/v/django-simple-email-auth
   :alt: PyPI Version
   :target: django-simple-email-auth-pypi_

.. image:: https://img.shields.io/pypi/l/django-simple-email-auth
   :alt: License
   :target: https://github.com/cdriehuys/django-simple-email-auth/blob/master/LICENSE

A Django library for authenticating using verified email addresses. Users may
authenticate using any email address they have verified ownership of.

Project Homepage
  https://github.com/cdriehuys/django-simple-email-auth

Documentation
  https://django-simple-email-auth.readthedocs.io

**********
Alpha Note
**********

This project is below version 1.0.0, which means any changes to the minor
number may be breaking changes.

********
Features
********

A brief overview of the features offered by this package:

* Verification of email ownership
* Password resets

************
Installation
************

From `PyPI <django-simple-email-auth-pypi>`_::

    pip install django-simple-email-auth

********
Road Map
********

The current focus is on getting the basic data models down. After that, we would
like to add the following features:

* A default REST API built with Django Rest Framework
* A set of default Django views for people who don't have a separate frontend.
* (Maybe) A default GraphQL backend

Feel free to `open a new issue <issues-new>`_ if you have an additional feature
request that is not listed here.

*******
License
*******

This project is licensed under the MIT License.

.. _issues-new: https://github.com/cdriehuys/django-simple-email-auth/issues/new
.. _django-simple-email-auth-pypi: https://pypi.org/project/django-simple-email-auth/
