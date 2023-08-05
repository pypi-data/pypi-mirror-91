"""Async HTTP authentication flow to get XMPP loggin credentials"""
# TODO: Refactor the two login flows for DRYness

try:
    import re2 as re
except ImportError:
    import re
import logging
import aiohttp
from lxml import etree
from .const import (
    API_URL,
    LOGIN_URL,
    OAUTH2_APP_ID,
    OAUTH2_CLIENT_ID,
    OAUTH2_CLIENT_SECRET,
    OAUTH2_REDIRECT_URI,
)
from .exception import GeAuthFailedError, GeGeneralServerError

from typing import Dict
from urllib.parse import urlparse, parse_qs

_LOGGER = logging.getLogger(__name__)


async def async_get_oauth2_token(session: aiohttp.ClientSession, username: str, password: str) -> Dict:
    """Hackily get an oauth2 token until I can be bothered to do this correctly"""
    params = {
        'client_id': OAUTH2_CLIENT_ID,
        'response_type': 'code',
        'access_type': 'offline',
        'redirect_uri': OAUTH2_REDIRECT_URI,
    }

    async with session.get(f'{LOGIN_URL}/oauth2/auth', params=params) as resp:
        if 400 <= resp.status < 500:
            raise GeAuthFailedError(await resp.text())
        if resp.status >= 500:
            raise GeGeneralServerError(await resp.text())
        resp_text = await resp.text()

    email_regex = (
        r'^\s*(\w+(?:(?:-\w+)|(?:\.\w+)|(?:\+\w+))*\@'
        r'[A-Za-z0-9]+(?:(?:\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9][A-Za-z0-9]+)\s*$'
    )
    clean_username = re.sub(email_regex, r'\1', username)

    etr = etree.HTML(resp_text)
    post_data = {
        i.attrib['name']: i.attrib['value']
        for i in etr.xpath("//form[@id = 'frmsignin']//input")
        if 'value' in i.keys()
    }
    post_data['username'] = clean_username
    post_data['password'] = password

    async with session.post(f'{LOGIN_URL}/oauth2/g_authenticate', data=post_data, allow_redirects=False) as resp:
        if 400 <= resp.status < 500:
            raise GeAuthFailedError(await resp.text())
        if resp.status >= 500:
            raise GeGeneralServerError(await resp.text())
        code = parse_qs(urlparse(resp.headers['Location']).query)['code'][0]

    post_data = {
        'code': code,
        'client_id': OAUTH2_CLIENT_ID,
        'client_secret': OAUTH2_CLIENT_SECRET,
        'redirect_uri': OAUTH2_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    auth = aiohttp.BasicAuth(OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET)
    async with session.post(f'{LOGIN_URL}/oauth2/token', data=post_data, auth=auth) as resp:
        if 400 <= resp.status < 500:
            raise GeAuthFailedError(await resp.text())
        if resp.status >= 500:
            raise GeGeneralServerError(await resp.text())
        oauth_token = await resp.json()
    try:
        return {'Authorization': 'Bearer ' + oauth_token['access_token']}
    except KeyError:
        raise GeAuthFailedError(f'Failed to get a token: {oauth_token}')


async def async_get_mobile_device_token(session: aiohttp.ClientSession, auth_header: Dict) -> str:
    """Get a mobile device token"""
    mdt_data = {
        'kind': 'mdt#login',
        'app': OAUTH2_APP_ID,
        'os': 'google_android'
    }
    async with session.post(f'{API_URL}/v1/mdt', json=mdt_data, headers=auth_header) as resp:
        if resp.status != 200:
            raise GeAuthFailedError(await resp.text())
        results = await resp.json()

    try:
        return results['mdt']
    except KeyError:
        raise GeAuthFailedError(f'Failed to get a mobile device token: {results}')


async def async_get_ge_token(session: aiohttp.ClientSession, auth_header: Dict, mobile_device_token: str) -> str:
    """Get the GE token that we can use to get XMPP credentials"""
    params = {
        'client_id': OAUTH2_CLIENT_ID,
        'client_secret': OAUTH2_CLIENT_SECRET,
        'mdt': mobile_device_token
    }
    async with session.post(f'{LOGIN_URL}/oauth2/getoken', params=params, headers=auth_header) as resp:
        if 400 <= resp.status < 500:
            raise GeAuthFailedError(await resp.text())
        if resp.status >= 500:
            raise GeGeneralServerError(await resp.text())
        results = await resp.json()

    try:
        return results['access_token']
    except KeyError:
        raise GeAuthFailedError(f'Failed to get a GE token: {results}')


async def async_get_xmpp_credentials(session: aiohttp.ClientSession, ge_token: str) -> Dict:
    """Get XMPP credentials"""
    uri = f'{API_URL}/v1/mdt/credentials'
    headers = {'Authorization': f'Bearer {ge_token}'}
    async with session.get(uri, headers=headers) as resp:
        if 400 <= resp.status < 500:
            raise GeAuthFailedError(await resp.text())
        if resp.status >= 500:
            raise GeGeneralServerError(await resp.text())
        return await resp.json()


async def async_get_wss_credentials(session: aiohttp.ClientSession, auth_header: Dict) -> Dict:
    """Get WSS credentials"""
    uri = f'{API_URL}/v1/websocket'
    async with session.get(uri, headers=auth_header) as resp:
        if 400 <= resp.status < 500:
            raise GeAuthFailedError(await resp.text())
        if resp.status >= 500:
            raise GeGeneralServerError(await resp.text())
        return await resp.json()


async def async_do_full_xmpp_flow(session: aiohttp.ClientSession, username: str, password: str) -> Dict:
    """Perform a complete login flow, returning XMPP credentials."""

    _LOGGER.debug('Getting oauth2 token')
    auth_header = await async_get_oauth2_token(session, username, password)

    _LOGGER.debug('Getting mobile device token')
    mdt = await async_get_mobile_device_token(session, auth_header)

    _LOGGER.debug('Getting GE token')
    ge_token = await async_get_ge_token(session, auth_header, mdt)

    _LOGGER.debug('Getting XMPP credentials')
    xmpp_credentials = await async_get_xmpp_credentials(session, ge_token)

    return xmpp_credentials


async def async_do_full_wss_flow(session: aiohttp.ClientSession, username: str, password: str) -> Dict:
    """Perform a complete login flow, returning WSS credentials."""

    _LOGGER.debug('Getting oauth2 token')
    auth_header = await async_get_oauth2_token(session, username, password)

    _LOGGER.debug('Getting mobile device token')
    wss_credentials = await async_get_wss_credentials(session, auth_header)

    return wss_credentials
