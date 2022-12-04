import asyncio
import logging
from urlparse import urlparse

from pyisy import ISY
from pyisy.connection import ISYConnectionError, ISYInvalidAuthError, get_new_client_session
_LOGGER = logging.getLogger(__name__)

"""Validate the user input allows us to connect."""
user = "admin"
password = "password"
host = urlparse("http://192.168.1.113:80/")
tls_version = "1.2" # Can be False if using HTTP

if host.scheme == "http":
    https = False
    port = host.port or 80
elif host.scheme == "https":
    https = True
    port = host.port or 443
else:
    _LOGGER.error("host value in configuration is invalid.")
    return False

# Use the helper function to get a new aiohttp.ClientSession.
websession = get_new_client_session(https, tls_ver)

# Connect to ISY controller.
isy_conn = Connection(
    host.hostname,
    port,
    user,
    password,
    use_https=https,
    tls_ver=tls_version,
    webroot=host.path,
    websession=websession,
)

try:
    with async_timeout.timeout(30):
        isy_conf_xml = await isy_conn.test_connection()
except (ISYInvalidAuthError, ISYConnectionError):
    _LOGGER.error(
        "Failed to connect to the ISY, please adjust settings and try again."
    )