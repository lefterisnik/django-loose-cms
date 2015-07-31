import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-loose-cms',
    version='0.1',
    packages=['loosecms'],
    include_package_data=True,
    license='BSD License',
    description='A loose Django cms to create a site.',
    long_description=README,
    url='http://www.example.com/',
    author='Lefteris Nikoltsios',
    author_email='lefteris.nikoltsios@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=1.7,<1.9',
        'tinycss',
        'django-constance',
        'django-ckeditor',
        'bootstrap-admin',
    ],
)
