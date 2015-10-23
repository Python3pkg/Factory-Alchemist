from unittest import TestCase
from tests.dummy_models import metadata


def _rebuild_schema():
    if 'sqlite' in metadata.bind.url.drivername:
        metadata.drop_all()
        metadata.create_all()
    else:
        raise Exception('dont date to test in {}!'.format(metadata.bind.url.drivername))


class BaseTest(TestCase):
    def __call__(self, *args, **kwargs):
        _rebuild_schema()
        return super(BaseTest, self).__call__(*args, **kwargs)
