from unittest import TestCase

import requests

import requestsinspect

from . import TEST_DOMAIN, httplib


class TestLogger(TestCase):
    """
    Test cases for the custom logger and formatter in the requestsinspect module.
    """

    def _curl_formatter_custom_logger(self, data):
        lines = data.strip().split("\n")

        self.assertGreater(len(lines), 5)

        self.assertEqual(lines[0], ">>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<")
        self.assertEqual(lines[1], "> curl -X GET '{}'".format(TEST_DOMAIN))
        self.assertEqual(lines[2], "< 200 OK")
        self.assertGreaterEqual(len(lines[len(lines) - 2]), 1)
        self.assertEqual(lines[len(lines) - 1], ">>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<")

    def test_logger_with_curl_formatter(self):
        # curl formatter is default formatter
        # do not need to set it
        requestsinspect.patch()
        requestsinspect.logger = self._curl_formatter_custom_logger

        try:
            resopnse = requests.get(TEST_DOMAIN)

            self.assertEqual(resopnse.status_code, httplib.OK)
        except Exception as e:
            raise e
        finally:
            requestsinspect.unpatch()
            requestsinspect.restore_default_logger()

    def _plain_formatter_custom_logger(self, data):
        lines = data.strip().split("\n")

        self.assertGreater(len(lines), 7)

        self.assertEqual(lines[0], ">>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<")
        self.assertEqual(lines[1], "> GET {}".format(TEST_DOMAIN))
        self.assertEqual(lines[2], "> ")
        self.assertEqual(lines[3], "> ")
        self.assertGreaterEqual(len(lines[len(lines) - 2]), 1)
        self.assertEqual(lines[len(lines) - 1], ">>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<")

    def test_logger_with_plain_formatter(self):
        requestsinspect.patch()
        requestsinspect.formatter = requestsinspect.plain_formatter
        requestsinspect.logger = self._plain_formatter_custom_logger

        try:
            resopnse = requests.get(TEST_DOMAIN)

            self.assertEqual(resopnse.status_code, httplib.OK)
        except Exception as e:
            raise e
        finally:
            requestsinspect.unpatch()
            requestsinspect.restore_default_formatter()
            requestsinspect.restore_default_logger()
