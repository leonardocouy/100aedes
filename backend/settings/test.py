from .base import *


INSTALLED_APPS += (
    'test_without_migrations',
    'django_nose',
)

# django-nose
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# NOSE_ARGS = [
#     '--with-coverage',
#     '--cover-html',
#     '--cover-package=backend'
# ]
#
