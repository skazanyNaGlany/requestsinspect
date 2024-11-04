# Requests-inspect

Log or affect requests made by the requests library.

## Overview

`requestsinspect` is a very simple Python module that extends the `requests` library to include callback functionality for inspecting HTTP requests and responses. It allows you to log and format request and response data in various formats, such as plain text and cURL-like output.

## Features

- Callback functionality to inspect requests and responses.
- Multiple formatters for request and response data.
- Easy patching and unpatching of the `requests` library.
- Python 2 and 3 compatible.
- No dependencies.
- Very simple and customizable.

## Installation

```sh
pip install git+https://github.com/skazanyNaGlany/requestsinspect.git
```

## Usage

```python
import requests
import requestsinspect

requestsinspect.patch()

requests.get("http://excample.com")

requestsinspect.unpatch()
```

The request and response data will be logged using the default logger (logging) and formatter (cURL).

Output

```
>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<
> curl -X GET 'http://excample.com'
< 200 OK
< date: Sat, 02 Nov 2024 12:38:26 GMT
< server: Apache
< set-cookie: __tad=1730551106.2852277; expires=Tue, 31-Oct-2034 12:38:26 GMT; Max-Age=315360000
< vary: Accept-Encoding
< content-encoding: gzip
< content-length: 570
< content-type: text/html; charset=UTF-8
< connection: close
< (b'<html>\n<head>\n<title>excample.com</title>\n<script type="text/javascript"'
 b' src="/js/fingerprint/iife.min.js"></script>\n<script type="text/javascri'
 b'pt">\nvar redirect_link = \'http://excample.com/?\';\n\n// Set a timeout '
 b'of 300 microseconds to execute a redirect if the fingerprint promise fails f'
 b'or some reason\nfunction fallbackRedirect() {\n\twindow.location.replace(re'
 b"direct_link+'fp=-7');\n}\n\ntry {\n\tconst rdrTimeout = setTimeout(fallba"
 b'ckRedirect, 300);\n\tvar fpPromise = FingerprintJS.load({monitoring: false'
 b'});\n\tfpPromise\n\t\t.then(fp => fp.get())\n\t\t.then(\n\t\t\tresult =>'
 b" { \n\t\t\t\tvar fprt = 'fp='+result.visitorId;\n\t\t\t\tclearTimeout(rdrT"
 b'imeout);\n\t\t\t\twindow.location.replace(redirect_link+fprt);\n\t\t});\n'
 b'} catch(err) {\n\tfallbackRedirect();\n}\n\n</script>\n<style> body { back'
 b'ground:#101c36 } </style>\n</head>\n<body bgcolor="#ffffff" text="#000000"'
 b">\n<div style='display: none;'><a href='http://excample.com/?fp=-3'>Click"
 b' here to enter</a></div>\n<noscript><meta http-equiv="refresh" content="0'
 b'; URL=http://excample.com/?fp=-5"></noscript>\n</body>\n</html>')
>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<
```

## Affecting the request

```python
import requests
import requestsinspect


def my_callback(_request):
    # change the url of the request
    # it should raise an exception
    _request['kwargs']['url'] = 'http://example.com123'
    return True


requestsinspect.callback = my_callback
requestsinspect.patch()

# this should raise requests.exceptions.ConnectionError
requests.get("http://excample.com")

requestsinspect.unpatch()
```

Output (will return an exception since the domain is invalid)

```
...
requests.exceptions.ConnectionError: HTTPConnectionPool(host='example.com123', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f495a99e710>: Failed to establish a new connection: [Errno -2] Name or service not known'))
```


## Usage with plain formatter

```python
import requests
import requestsinspect


requestsinspect.formatter = requestsinspect.plain_formatter
requestsinspect.patch()

response = requests.get("http://excample.com")

print(response)

requestsinspect.unpatch()
```

Output

```
>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<
> GET http://excample.com
> 
> 
< 200 OK
< date: Sat, 02 Nov 2024 12:40:41 GMT
< server: Apache
< set-cookie: __tad=1730551241.6751207; expires=Tue, 31-Oct-2034 12:40:41 GMT; Max-Age=315360000
< vary: Accept-Encoding
< content-encoding: gzip
< content-length: 570
< content-type: text/html; charset=UTF-8
< connection: close
< (b'<html>\n<head>\n<title>excample.com</title>\n<script type="text/javascript"'
 b' src="/js/fingerprint/iife.min.js"></script>\n<script type="text/javascri'
 b'pt">\nvar redirect_link = \'http://excample.com/?\';\n\n// Set a timeout '
 b'of 300 microseconds to execute a redirect if the fingerprint promise fails f'
 b'or some reason\nfunction fallbackRedirect() {\n\twindow.location.replace(re'
 b"direct_link+'fp=-7');\n}\n\ntry {\n\tconst rdrTimeout = setTimeout(fallba"
 b'ckRedirect, 300);\n\tvar fpPromise = FingerprintJS.load({monitoring: false'
 b'});\n\tfpPromise\n\t\t.then(fp => fp.get())\n\t\t.then(\n\t\t\tresult =>'
 b" { \n\t\t\t\tvar fprt = 'fp='+result.visitorId;\n\t\t\t\tclearTimeout(rdrT"
 b'imeout);\n\t\t\t\twindow.location.replace(redirect_link+fprt);\n\t\t});\n'
 b'} catch(err) {\n\tfallbackRedirect();\n}\n\n</script>\n<style> body { back'
 b'ground:#101c36 } </style>\n</head>\n<body bgcolor="#ffffff" text="#000000"'
 b">\n<div style='display: none;'><a href='http://excample.com/?fp=-3'>Click"
 b' here to enter</a></div>\n<noscript><meta http-equiv="refresh" content="0'
 b'; URL=http://excample.com/?fp=-5"></noscript>\n</body>\n</html>')
>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<
```

## Affecting the request and pass it to the default callback

```python
import requests
import requestsinspect


def my_callback(_request):
    # change the url of the request
    # it should raise an exception
    _request['kwargs']['url'] = 'http://example.com123'
    return _request['_default_callback'](_request)


requestsinspect.callback = my_callback
requestsinspect.patch()

# this should raise requests.exceptions.ConnectionError
requests.get("http://excample.com")

requestsinspect.unpatch()
```

Response

```
>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<
> curl -X GET 'http://example.com123'
< HTTPConnectionPool(host='example.com123', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f0ff5202740>: Failed to establish a new connection: [Errno -2] Name or service not known'))
>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<
```

## License

© Paweł Kacperski, 2024 ~ time.Now

Released under the [MIT License](https://github.com/go-gorm/gorm/blob/master/LICENSE)
