import sys
import os

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                'NAME': ':memory:',
            }
        },
        ROOT_URLCONF="urls",
        INSTALLED_APPS=[
            "django_admin_bootstrapped",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.sessions",
            "django.contrib.contenttypes",
            "django.contrib.staticfiles",
            "django.contrib.humanize",
            "django.contrib.sites",
            "taggit",
            "ckeditor",
            "loosecms",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        STATIC_URL='/static/',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.template.context_processors.request',
                        'django.contrib.messages.context_processors.messages',
                        'loosecms.template.context_processors.global_settings',
                    ],
                },
            },
        ],
        MEDIA_URL='/media/',
        MEDIA_ROOT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media'),
        DAB_FIELD_RENDERER='django_admin_bootstrapped.renderers.BootstrapFieldRenderer',
        CKEDITOR_UPLOAD_PATH = 'images/',

    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
