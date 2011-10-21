# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from modelhistory import VERSION

long_description = """Simple model logging helper for django projects. Covers functionality of discovering action taken on object: DELETE, UPDATE, CREATE and creates and saves suitable message to database. Supports simple db.models.Models objects as well as forms, formset and inlineformset based on Django ORM Models."""


setup(
    name='django-modelhistory',
    version=".".join(map(str, VERSION)),
    description='django-modelhistory reusable application for loggin models changes.',
    long_description=long_description,
    author='Sebastian Pawluś',
    author_email='sebastian.pawlus@gmail.com',
    url='https://github.com/xando/django-modelhistory',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='modelhistory.tests.runtests.runtests'
)
