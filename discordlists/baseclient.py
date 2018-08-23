"""
 *  discordlists.py: A simple API wrapper for botblock.org providing server count posting to all bot lists and fetching
 *   bot information from all.
 *  <https://github.com/MattIPv4/discordlists.py/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
 *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 *   documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 *   the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
 *   to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 *  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
 *   the Software.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
 *   THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
 *   CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 *   IN THE SOFTWARE.
 *
 *   <https://github.com/MattIPv4/discordlists.py/blob/master/LICENSE>
"""

from typing import Union

import aiohttp

from .exceptions import *

API_BASE = "https://botblock.org/api/"


class BaseClient:
    """
    This class is used to directly interact with the botblock.org API via http requests.
    """

    def __init__(self):
        self.base = API_BASE  # API base url
        self.session = None  # aiohttp session
        self.auth = {}  # Store of authorisation tokens

    def __session_init(self):
        """
        Starts up the aiohttp session if one does not yet exist
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

    def __headers(self) -> dict:
        """
        Gets standard headers used in an API request

        Returns
        =======

        json: dict
            The http request headers
        """
        return {'content-type': 'application/json'}

    async def __handle_response(self, resp: aiohttp.ClientResponse) -> dict:
        """
        Handles all responses returned from any API request

        Parameter
        ========

        resp: aiohttp.ClientResponse
            The raw response from the aiohttp request to the API

        Returns
        =======

        json: dict
            The formatted response from the API endpoint
        """
        status = resp.status
        text = await resp.text()
        try:
            json = await resp.json()
        except:
            json = {}

        # Empty
        if json == {} and text.strip() == "":
            raise EmptyResponse()

        # Ratelimited
        if status == 429:
            raise Ratelimited(json)

        # Error
        if status != 200:
            raise RequestFailure(status, text)

        return json

    async def __post(self, endpoint: str, content: Union[list, dict]) -> dict:
        """
        POST data to an API endpoint

        Parameter
        ========

        endpoint: str
            The endpoint to access on the API

        content: Union[list, dict]
            The data to be posted to the endpoint

        Returns
        =======

        json: dict
            The formatted response from the API endpoint
        """
        self.__session_init()
        async with self.session.post(url=self.base + endpoint, json=content, headers=self.__headers()) as resp:
            return await self.__handle_response(resp)

    async def __get(self, endpoint: str) -> dict:
        """
        GET data from an API endpoint

        Parameter
        ========

        endpoint: str
            The endpoint to access on the API

        Returns
        =======

        json: dict
            The formatted response from the API endpoint
        """
        self.__session_init()
        async with self.session.get(url=self.base + endpoint, headers=self.__headers()) as resp:
            return await self.__handle_response(resp)

    def set_auth(self, list_id: str, auth_token: str):
        """
        Sets an authorisation token for the given list ID from botblock.org

        Parameter
        ========

        list_id: str
            The ID of the list from botblock.org

        auth_token: str
            The authorisation token this list provided you to use their API.
        """
        self.auth[list_id] = auth_token

    def remove_auth(self, list_id: str):
        """
        Removes an authorisation token for the given list ID from botblock.org

        Parameter
        ========

        list_id: str
            The ID of the list from botblock.org
        """
        if list_id in self.auth.keys():
            del self.auth[list_id]

    def __guild_count_body(self, bot_id: int, guild_count: int) -> dict:
        """
        Gets the body used for a server/guild count post API request

        Parameter
        ========

        bot_id: int
            The ID of the bot you want to update server/guild count for

        guild_count: int
            The server/guild count for the bot

        Returns
        =======

        json: dict
            The json body to send
        """
        data = self.auth.copy()
        data["server_count"] = guild_count
        data["bot_id"] = bot_id
        return data

    async def post_guild_count(self, bot_id: int, guild_count: int) -> dict:
        """
        POST a server/guild count for a bot

        Parameter
        ========

        bot_id: int
            The ID of the bot you want to update server/guild count for

        guild_count: int
            The server/guild count for the bot

        Returns
        =======

        json: dict
            The response from the API endpoint
        """
        return await self.__post("count", self.__guild_count_body(bot_id, guild_count))

    async def get_bot_information(self, bot_id: int) -> dict:
        """
        GET information about a bot

        Parameter
        ========

        bot_id: int
            The ID of the bot you want to fetch from the API

        Returns
        =======

        json: dict
            The response from the API endpoint
        """
        return await self.__get("bots/{}".format(bot_id))
