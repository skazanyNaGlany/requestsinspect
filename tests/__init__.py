import sys

if sys.version_info.major == 2:
    import httplib
elif sys.version_info.major == 3:
    import http.client as httplib
else:
    raise Exception("Unsupported Python version")

TEST_DOMAIN = "http://exmaple.com"
