from unittest import TestCase

import requests

import requestsinspect

from . import TEST_DOMAIN, httplib


class TestSimple(TestCase):
    """
    TestSimple is a test case class that tests the basic functionality of the
    requestsinspect library.
    """

    def test_simple(self):
        requestsinspect.patch()

        try:
            resopnse = requests.get(TEST_DOMAIN)

            self.assertEqual(resopnse.status_code, httplib.OK)
        except Exception as e:
            raise e
        finally:
            requestsinspect.unpatch()
