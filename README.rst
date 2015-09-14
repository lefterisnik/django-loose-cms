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
* Edit stylesheet of the plugins (no functional)
* Template pages
* File manager with custom model field

Requirements
------------

Loose CMS requires:

* Django version 1.8
* Python 2.6 or 2.7
* tinycss
* beautifulsoup4
* django-admin-bootstrapped
* django-taggit
* django-ckeditor

You should install manually:

* unidecode: if your tags wan in non-latin format.

Quick Start
-----------

Installation via startproject template (quick way)
``````````````````````````````````````````````````

1. Make the project folder::

    mkdir project_name
    cd project_name

2. Create the virtualenv of python::

    virtualenv env
    source env/bin/activate

3. Install django package (version 1.8)::

    pip install django


4. Create the django project with custom template::

    django-admin.py startproject <project_name> --template=https://github.com/lefterisnik/django-template/archive/master.zip
    cd <project_name>

5. Install the requirements::

    pip install -r requirements.txt

6. Sync database::

    python manage.py migrate

6. Create one superuser account::

    python manage.py createsuperuser

7. Visit http://127.0.0.1:8000/ to start playing with the cms

Normal installation (slow way)
``````````````````````````````

Following this way you must edit settings.py file to provide some settings.

Using virtualenv
''''''''''''''''

1. Make the project folder::

    mkdir project_name
    cd project_name

2. Create the virtualenv of python::

    virtualenv env
    source env/bin/activate

3. Installation via pip::

    pip install https://github.com/lefterisnik/django-loose-cms/archive/master.zip

   The above command will download and setup all the requirements including the django.

4. Create your django project::

    django-admin startproject myproject
    cd myproject

5. Add "loosecms" to your INSTALLED_APPS setting at settings.py file like this::

    INSTALLED_APPS = (
        ...
        'loosecms',
    )

6. Add "bootstrap_admin" to your INSTALLED_APPS setting like this before 'django.contrib.admin'::

    INSTALLED_APPS = (
        'bootstrap_admin',
        'django.contrib.admin',
    )

7. Include the loosecms URLconf in your project urls.py like this::

    url(r'^', include('loosecms.urls')),

   Loose CMS handles all urls.

8. Run ``python manage.py migrate`` to create the loosecms models.

9. Run ``python manage.py createsuperuser`` to create a superuser account.

10. Run development server ``python manage.py runserver`` and visit http://127.0.0.1:8000/ to start
    playing with the cms.

Using system python
'''''''''''''''''''

1. Make the project folder::

    mkdir project_name
    cd project_name

3. Installation via pip::

    sudo pip install https://github.com/lefterisnik/django-loose-cms/archive/master.zip

   The above command will download and setup all the requirements including the django.

4. Create your django project::

    django-admin startproject myproject
    cd myproject

5. Add "loosecms" to your INSTALLED_APPS setting at settings.py file like this::

    INSTALLED_APPS = (
        ...
        'loosecms',
    )

6. Add "bootstrap_admin" to your INSTALLED_APPS setting like this before 'django.contrib.admin'::

    INSTALLED_APPS = (
        'bootstrap_admin',
        'django.contrib.admin',
    )

7. Include the loosecms URLconf in your project urls.py like this::

    url(r'^', include('loosecms.urls')),

   Loose CMS handles all urls.

8. Run ``python manage.py migrate`` to create the loosecms models.

9. Run ``python manage.py createsuperuser`` to create a superuser account.

10. Run development server ``python manage.py runserver`` and visit http://127.0.0.1:8000/ to start
    playing with the cms.


Plugins
-------

Some plugins:

* `django-loosecms-text`_.
* `django-loosecms-article`_.
* `django-loosecms-doc`_.
* `django-loosecms-cas`_.
* `django-loosecms-menu`_.
* `django-loosecms-link`_.
* `django-loosecms-rss`_.
* `django-loosecms-dynamo`_.
* `django-loosecms-search`_.


.. _django-loosecms-text: https://github.com/lefterisnik/django-loosecms-text
.. _django-loosecms-article: https://github.com/lefterisnik/django-loosecms-article
.. _django-loosecms-doc: https://github.com/lefterisnik/django-loosecms-doc
.. _django-loosecms-cas: https://github.com/lefterisnik/django-loosecms-cas
.. _django-loosecms-menu: https://github.com/lefterisnik/django-loosecms-menu
.. _django-loosecms-link: https://github.com/lefterisnik/django-loosecms-link
.. _django-loosecms-rss: https://github.com/lefterisnik/django-loosecms-rss
.. _django-loosecms-search: https://github.com/lefterisnik/django-loosecms-search
.. _django-loosecms-dynamo: https://github.com/lefterisnik/django-loosecms-dynamo