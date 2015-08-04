================
Django Loose CMS
================

.. image:: https://travis-ci.org/lefterisnik/django-loose-cms.png?branch=master
    :target: https://travis-ci.org/lefterisnik/django-loose-cms
.. image:: https://codeclimate.com/github/lefterisnik/django-loose-cms/badges/gpa.svg
   :target: https://codeclimate.com/github/lefterisnik/django-loose-cms
   :alt: Code Climate

Django Loose CMS is a simple cms based on django framework.

Features
--------

* Build bootstrap grid
* Edit stylesheet of the plugins
* Template pages

Requirements
------------

Loose CMS requires:

* Django version 1.8
* Python 2.6 or 2.7
* tinycss
* django-dynamic-preferences
* bootstrap-admin

Quick Start
-----------

1. Instalation via pip::

    pip install https://github.com/lefterisnik/django-loose-cms/archive/master.zip

2. Create your django project::

    django-admin startproject myproject
    cd myproject
    python manage.py createsuperuser

3. Add "loosecms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'loosecms',
    )

4. Add "bootstrap_admin" to your INSTALLED_APPS setting like this before 'django.contrib.admin'::

    INSTALLED_APPS = (
        'bootstrap_admin',
        'django.contrib.admin',
    )

5. Add "dynamic_preferences" to your INSTALLED_APPS setting like this before 'loosecms'::

    INSTALLED_APPS = (
        ...
        'dynamic_preferences',
    )

6. Include the loosecms URLconf in your project urls.py like this::

    url(r'^', include('loosecms.urls')),

   Loose CMS handles all urls.

7. Run ``python manage.py migrate`` to create the loosecms and dynamic_preferences models.

9. Run development server ``python manage.py runserver`` and visit http://127.0.0.1:8000/ to start
   playing with the cms.


Plugins
-------

Some plugins:

* `django-loosecms-text`_.
* `django-loosecms-article`_.
* `django-loosecms-doc`_.


.. _django-loosecms-text: https://github.com/lefterisnik/django-loosecms-text
.. _django-loosecms-article: https://github.com/lefterisnik/django-loosecms-article
.. _django-loosecms-doc: https://github.com/lefterisnik/django-loosecms-doc