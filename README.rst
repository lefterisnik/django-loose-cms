=====
Django Loose CMS
=====

Django Loose CMS is a simple cms based on django framework.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "loosecms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'loosecms',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^', include('loosecms.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ to participate in the poll.

CONSTANCE_CONFIG = {
    'SITE_TITLE': ('Site', _('Give the name of the site.')),
    'FAVICON': ('images/favicon.ico', _('Give the path of the site favicon.'))
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Standard',
        'height': 'auto',
        'width': 'auto',
    }
}

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_IMAGE_BACKEND = 'pillow'


python manage.py createsuperuser