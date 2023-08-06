import sys

import django
from django.conf import settings as django_settings
from djangoldp.conf.ldpsettings import LDPSettings

# create a test configuration
config = {
    # add the packages to the reference list
    'ldppackages': ['djangoldp_project','djangoldp_invoice','djangoldp_invoice.tests'],

    # required values for server
    'server': {
        'AUTH_USER_MODEL': 'tests.User',
        'REST_FRAMEWORK': {
            'DEFAULT_PAGINATION_CLASS': 'djangoldp.pagination.LDPPagination',
            'PAGE_SIZE': 5
        },
        # map the config of the core settings (avoid asserts to fail)
        'SITE_URL': 'http://happy-dev.fr',
        'BASE_URL': 'http://happy-dev.fr',
        # TODO: https://git.startinblox.com/djangoldp-packages/djangoldp/issues/341
        'SERIALIZER_CACHE': False,
        'PERMISSIONS_CACHE': False
    }
}

ldpsettings = LDPSettings(config)
django_settings.configure(ldpsettings)

django.setup()
from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests([
    'djangoldp_invoice.tests.tests_permissions',
    'djangoldp_invoice.tests.tests_get',
])
if failures:
    sys.exit(failures)
