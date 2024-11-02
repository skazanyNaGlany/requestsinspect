from unittest import TestCase

import requests

import requestsinspect

from . import TEST_DOMAIN, httplib


class TestCallback(TestCase):
    """
    Test case for verifying the callback functionality in the requestsinspect module.
    """

    def test_callback(self):
        requestsinspect.patch()
        requestsinspect.user_data = {
            "got_request": False,
            "got_response": False,
            "got_exception": False,
            "counter": 0,
        }

        def callback(_request):
            if len(_request) > 0:
                requestsinspect.user_data["got_request"] = True

            if "_response" in _request:
                requestsinspect.user_data["got_response"] = True

            if "_exception" in _request:
                requestsinspect.user_data["got_exception"] = True

            requestsinspect.user_data["counter"] += 1

            return _request["_default_callback"](_request)

        requestsinspect.callback = callback

        try:
            resopnse = requests.get(TEST_DOMAIN)

            self.assertEqual(resopnse.status_code, httplib.OK)
            self.assertTrue(requestsinspect.user_data["got_request"])
            self.assertTrue(requestsinspect.user_data["got_response"])
            self.assertFalse(requestsinspect.user_data["got_exception"])
            self.assertEqual(requestsinspect.user_data["counter"], 2)
        except Exception as e:
            raise e
        finally:
            requestsinspect.unpatch()
            requestsinspect.restore_default_callback()
            requestsinspect.user_data = None

    def test_callback_affect_url(self):
        requestsinspect.patch()

        def callback(_request):
            # change the url to the wrong one
            # it should raise an exception
            _request["kwargs"]["url"] = TEST_DOMAIN + "123"

            return True

        requestsinspect.callback = callback

        try:
            with self.assertRaises(requests.exceptions.ConnectionError):
                requests.get(TEST_DOMAIN)
        except Exception as e:
            raise e
        finally:
            requestsinspect.unpatch()
            requestsinspect.restore_default_callback()
            requestsinspect.user_data = None
