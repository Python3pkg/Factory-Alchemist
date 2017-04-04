from unittest import TestCase
import sys
from tests.dummy_models import metadata


PY3 = (3,) <= sys.version_info < (4,)


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

    if PY3:
        def assertItemsEqual(self, expected_seq, actual_seq, msg=None):
            if len(expected_seq) != len(actual_seq):
                self.fail('Sequences have distinct number of items')

            for item_1, item_2 in zip(sorted(expected_seq), sorted(actual_seq)):
                if item_1 != item_2:
                    self.fail('%s is different from %s' % (item_1, item_2))
