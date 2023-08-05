#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Alexa devices (echo dot, etc) programmatically.

This provides a login by proxy method.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""
import binascii
import logging
import secrets
from typing import Text

from aiohttp import web
import multidict
from yarl import URL

from alexapy.alexalogin import AlexaLogin
from alexapy.const import LOCALE_KEY
from alexapy.stackoverflow import get_open_port

_LOGGER = logging.getLogger(__name__)


class AlexaProxy:
    """Class to handle proxy login connections to Alexa."""

    def __init__(self, login: AlexaLogin, base_url: Text) -> None:
        """Initialize proxy object.

        Args:
            login (AlexaLogin): AlexaLogin object to update after completion of proxy.
            base_url (Text): base url for proxy location. e.g., http://192.168.1.1

        """
        self._login: AlexaLogin = login
        self._base_url: Text = str(base_url)
        self._port: int = 0
        self.runner = None
        self.data = {}
        self._config_flow_id: Text = ""
        self._callback_url: Text = ""

    @property
    def port(self) -> int:
        """Return port."""
        return self._port

    def access_url(self) -> URL:
        """Return access url for proxy."""
        return f"{URL(self._base_url).with_port(self.port)}"

    async def start_handler(self, request: web.Request) -> web.Response:
        """Handle start of proxy interaction.

        This will attempt a login starting at the Alexa oauth signin page.

        Args
            request (web.Request): The request to process

        Returns
            web.Response: The webresponse to display in the browser

        """
        self._config_flow_id = request.query["config_flow_id"]
        self._callback_url = request.query["callback_url"]
        _LOGGER.debug(
            "Starting auth for domain %s for configflow %s with callback %s",
            self._login.url,
            self._config_flow_id,
            self._callback_url,
        )
        site: URL = URL("https://www.amazon.com/ap/signin")
        deviceid: Text = f"{binascii.hexlify(secrets.token_hex(16).encode()).decode()}23413249564c5635564d32573831"
        query = {
            "openid.return_to": "https://www.amazon.com/ap/maplanding",
            "openid.assoc_handle": "amzn_dp_project_dee_ios",
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "pageId": "amzn_dp_project_dee_ios",
            "accountStatusPolicy": "P1",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.mode": "checkid_setup",
            "openid.ns.oa2": "http://www.amazon.com/ap/ext/oauth/2",
            "openid.oa2.client_id": f"device:{deviceid}",
            "openid.ns.pape": "http://specs.openid.net/extensions/pape/1.0",
            "openid.oa2.response_type": "token",
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.pape.max_auth_age": "0",
            "openid.oa2.scope": "device_auth_access",
            "language": LOCALE_KEY.get(self._login.url.replace("amazon", ""))
            if LOCALE_KEY.get(self._login.url.replace("amazon", ""))
            else "en_US",
        }
        site = site.update_query(query)
        headers = multidict.MultiDict(request.headers)
        headers.update({"Host": "www.amazon.com"})
        resp = await self._login._session.get(site, headers=headers)
        text = (await resp.text()).replace("https://www.amazon.com", self.access_url())
        return web.Response(text=text, content_type=resp.content_type,)

    async def get_handler(self, request: web.Request) -> web.Response:
        """Handle get requests.

        Args
            request (web.Request): The get request to process

        Returns
            web.Response: The webresponse to the browser

        """

        _LOGGER.debug("Get Request: %s", request.url)
        if request.url.path == "/":
            return await self.start_handler(request)
        if request.url.path == "/resume" and self._login.lastreq:
            _LOGGER.debug("Resuming request: %s", self._login.lastreq)
            self._config_flow_id = request.query["config_flow_id"]
            self._callback_url = request.query["callback_url"]
            resp = self._login.lastreq
        else:
            site = str(request.url).replace(self.access_url(), "https://www.amazon.com")
            resp = await self._login._session.get(site)
        content_type = resp.content_type
        if content_type == "text/html":
            text = (await resp.text()).replace(
                "https://www.amazon.com", self.access_url()
            )
            return web.Response(text=text, content_type=content_type,)
        # handle non html content
        return web.Response(body=await resp.content.read(), content_type=content_type)

    async def post_handler(self, request: web.Request) -> web.Response:
        """Handle post requests.

        Args
            request (web.Request): The post request to process

        Returns
            web.Response: The webresponse to the browser

        Raises
            web.HTTPFound: Redirect URL upon success

        """

        _LOGGER.debug("Post Request: %s", request.url)
        data = await request.post()
        self.data.update(data)
        site = str(request.url).replace(self.access_url(), "https://www.amazon.com")
        headers = multidict.MultiDict(request.headers)
        headers.update(
            {
                "Host": "www.amazon.com",
                "Origin": "www.amazon.com",
                "Referer": "www.amazon.com",
            }
        )
        # submit post
        resp = await self._login._session.post(site, data=data, headers=headers)
        text = await resp.text()
        content_type = resp.content_type
        if resp.url.path == "/ap/maplanding":
            self._login.access_token = resp.url.query.get("openid.oa2.access_token")
            if self.data.get("email"):
                self._login.email = self.data.get("email")
            if self.data.get("password"):
                self._login.password = self.data.get("password")
            if self._callback_url:
                _LOGGER.debug("Success. Redirecting to: %s", self._callback_url)
                raise web.HTTPFound(location=URL(self._callback_url))
            return web.Response(
                text=f"Successfully logged in as {self._login.email} for flow {self._config_flow_id}. Please close the window.",
            )
        text = text.replace("https://www.amazon.com", self.access_url())
        return web.Response(text=text, content_type=content_type)

    async def start_proxy(self) -> None:
        """Start proxy."""

        app = web.Application()
        app.add_routes(
            [
                web.route("get", "/{tail:.*}", self.get_handler),
                web.route("post", "/{tail:.*}", self.post_handler),
            ]
        )
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        if not self.port:
            self._port = get_open_port()
        site = web.TCPSite(self.runner, "0.0.0.0", self.port)
        await site.start()
        _LOGGER.debug("Starting proxy at %s", f"{self._base_url}:{self.port}")

    async def stop_proxy(self):
        """Stop proxy."""
        _LOGGER.debug("Stopping proxy at %s", f"{self._base_url}:{self.port}")
        await self.runner.cleanup()
        await self.runner.shutdown()
