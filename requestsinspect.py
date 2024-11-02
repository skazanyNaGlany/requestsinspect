import logging
import pprint

import requests

original_session = None
enable_callback = True
user_data = None


class InspectedSession(requests.Session):
    """
    InspectedSession is a subclass of requests.Session that allows for inspection
    and modification of HTTP requests and responses.
    """

    def request(self, *args, **kwargs):
        _request = {
            "_default_callback": default_callback,
            "args": args,
            "kwargs": kwargs,
        }

        try:
            if enable_callback:
                if not callback(_request):
                    return None

            response = super(InspectedSession, self).request(
                *_request["args"], **_request["kwargs"]
            )

            _request["_response"] = response

            if enable_callback:
                if not callback(_request):
                    return None

            return response
        except Exception as e:
            _request["_exception"] = e

            if enable_callback:
                if not callback(_request):
                    return None

            raise _request["_exception"]


def _plain_request_formatter(_request):
    url = "{} {}".format(
        _request["kwargs"]["method"].upper(), _request["kwargs"]["url"]
    )

    request_data = []
    request_data.append(url)

    if "headers" in _request["kwargs"]:
        for key, value in _request["kwargs"]["headers"].items():
            request_data.append("{}: {}".format(key, value))
    else:
        request_data.append("")

    if "data" in _request["kwargs"]:
        request_data.append(pprint.pformat(_request["kwargs"]["data"]))
    elif "json" in _request["kwargs"]:
        request_data.append(pprint.pformat(_request["kwargs"]["json"]))
    else:
        request_data.append("")

    return request_data


def _curl_request_formatter(_request):
    command = "curl -X " + _request["kwargs"]["method"].upper()

    if "headers" in _request["kwargs"]:
        headers = [
            '"{0}: {1}"'.format(k, v) for k, v in _request["kwargs"]["headers"].items()
        ]

        if headers:
            command += " -H " + " -H ".join(headers)

    url = _request["kwargs"]["url"]
    data = ""

    if "data" in _request["kwargs"]:
        data = pprint.pformat(_request["kwargs"]["data"])
    elif "json" in _request["kwargs"]:
        data = pprint.pformat(_request["kwargs"]["json"])

    if data:
        command += ' -d "{}"'.format(data)

    command += " '{}'".format(url)

    return [command]


def _plain_response_formatter(_request):
    response_data = []

    # response
    response_data.append(
        "{} {}".format(
            _request["_response"].status_code,
            _request["_response"].reason,
        )
    )

    for key, value in _request["_response"].headers.items():
        response_data.append("{}: {}".format(key, value))

    try:
        response_data.append(pprint.pformat(_request["_response"].json()))
    except:
        response_data.append(pprint.pformat(_request["_response"].content))

    return response_data


def plain_formatter(_request):
    """
    Formats the given request and its response or exception into a plain text format.

    Args:
        _request (dict): The request dictionary containing request, response, and exception data.

    Returns:
        str: The formatted plain text representation of the request and its response or exception.
    """
    formatted = ""

    if "_exception" in _request:
        request_data = _plain_request_formatter(_request)

        for line in request_data:
            formatted += "> {}\n".format(line)

        formatted += "< {}\n".format(_request["_exception"])
    elif "_response" in _request:
        request_data = _plain_request_formatter(_request)
        response_data = _plain_response_formatter(_request)

        for line in request_data:
            formatted += "> {}\n".format(line)

        for line in response_data:
            formatted += "< {}\n".format(line)

    formatted = formatted.strip()

    if not formatted:
        return formatted

    formatted = "\n\n>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<\n{}\n>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<\n\n".format(
        formatted
    )

    return formatted


def curl_formatter(_request):
    """
    Formats a given request dictionary into a cURL-like command string.

    This function processes the request dictionary to generate a formatted string
    that represents the request and its response (if available) in a cURL-like format.
    It handles both exceptions and responses.

    Args:
        _request (dict): The request dictionary containing request and response data.

    Returns:
        str: A formatted string representing the request and response in a cURL-like format.
    """
    formatted = ""

    if "_exception" in _request:
        request_data = _curl_request_formatter(_request)

        for line in request_data:
            formatted += "> {}\n".format(line)

        formatted += "< {}\n".format(_request["_exception"])
    elif "_response" in _request:
        request_data = _curl_request_formatter(_request)
        response_data = _plain_response_formatter(_request)

        for line in request_data:
            formatted += "> {}\n".format(line)

        for line in response_data:
            formatted += "< {}\n".format(line)

    formatted = formatted.strip()

    if not formatted:
        return formatted

    formatted = "\n\n>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<\n{}\n>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<\n\n".format(
        formatted
    )

    return formatted


def patch():
    """
    Patches the requests library to use the InspectedSession class.

    This function replaces the default requests.sessions.Session class with
    the InspectedSession class. If the patch has already been applied, it
    will not apply it again.

    Returns:
        bool: True if the patch was applied successfully, False if the patch
              was already applied.
    """
    global original_session

    if requests.sessions.Session == InspectedSession:
        return False

    original_session = requests.sessions.Session

    requests.sessions.Session = InspectedSession

    return True


def unpatch():
    """
    Restores the original `requests.Session` class if it has been patched.

    This function checks if the `original_session` global variable is not None.
    If it is not None, it restores the `requests.Session` class to its original
    state and returns True. If `original_session` is None, it means the session
    has not been patched, and the function returns False.

    Returns:
        bool: True if the `requests.Session` was successfully restored to its
              original state, False otherwise.
    """
    global original_session

    if original_session is None:
        return False

    requests.Session = original_session

    return True


def default_callback(_request):
    """
    Processes a request using a formatter and logs the formatted result.
    """
    formatted = formatter(_request)

    if not formatted:
        return True

    logger(formatted)
    return True


def print_logger(data):
    """
    Default logger. Logs the provided data by printing it to the console.

    Args:
        data (str): The data to be logged.
    """
    print(data)


def logging_logger(data):
    """
    Logs the provided data using the logging module.

    Args:
        data (str): The data to be logged.
    """
    logging.debug(data)


def restore_default_callback():
    """
    Restores the default callback function.
    """
    global callback

    callback = default_callback


def restore_default_logger():
    """
    Restores the default logger function.
    """
    global logger

    logger = print_logger


def restore_default_formatter():
    """
    Restores the default formatter function.
    """
    global formatter

    formatter = curl_formatter


formatter = curl_formatter
logger = print_logger
callback = default_callback
