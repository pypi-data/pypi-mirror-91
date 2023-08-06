# -*- coding: utf-8 -*-

import requests as requests
from requests import (
    utils, packages, Request, Response,
    PreparedRequest, session, Session, codes
)
from requests.exceptions import (
    RequestException, Timeout, URLRequired,
    TooManyRedirects, HTTPError, ConnectionError,
    ConnectTimeout, ReadTimeout
)

from .api import request, get, options, head, post, put, patch, delete
from .model import SafeResponse, StatusFilter
