# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# http exceptions have backwards compatability issues across python 2  and python 3
# https://stackoverflow.com/questions/43676939
#  Base exception for RemoteDisconnected
from six import PY2

from requests.packages.urllib3.exceptions import SSLError, ProtocolError
from requests.exceptions import Timeout, SSLError as RequestsSSLError, ConnectionError as RequestsConnectionError

from azure.common import AzureHttpError

_AZURE_EXCEPTIONS = (AzureHttpError,)

_REQUESTS_EXCEPTIONS = (Timeout, RequestsSSLError, RequestsConnectionError)

_SSL_EXCEPTIONS = (SSLError, RequestsSSLError)

if PY2:
    from httplib import HTTPException
    _HTTP_EXCEPTIONS = (HTTPException, ProtocolError)
else:
    from http.client import HTTPException, RemoteDisconnected
    _HTTP_EXCEPTIONS = (ConnectionError, HTTPException, RemoteDisconnected)

RETRY_EXCEPTIONS = _HTTP_EXCEPTIONS + _REQUESTS_EXCEPTIONS + _SSL_EXCEPTIONS + _AZURE_EXCEPTIONS
