"""
 *  discordlists.py: A simple API wrapper for botblock.org providing server count posting to all bot lists and fetching
 *   bot information from all.
 *  <https://github.com/MattIPv4/discordlists.py/>
 *  Copyright (C) 2019 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
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

import asyncio
from typing import Tuple, Union

from discord import User

from .baseclient import BaseClient
from .exceptions import NotFound


class Client:
    """
    This class is used to interact with the botblock.org API using a discord.py bot instance.

    Parameters
    ==========

    bot :
        An instance of a discord.py Bot or Client object
    interval : int[Optional]
        Seconds between each automatic posting of server/guild count. Defaults to 1800 seconds (30 minutes)
    """

    def __init__(self, bot, interval: int = 30 * 60):
        self.bot = bot
        self.interval = interval
        self.base = BaseClient()

    @property
    def guild_count(self) -> int:
        """
        Gets the guild count from the bot

        Returns
        =======

        count: int
            The current number of guilds the bot is in
        """
        try:
            count = len(self.bot.guilds)
        except AttributeError:
            count = len(self.bot.servers)

        return count

    @property
    def server_count(self) -> int:
        """
        Gets the server count from the bot

        Returns
        =======

        count: int
            The current number of servers the bot is in
        """
        return self.guild_count

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
        self.base.set_auth(list_id, auth_token)

    def remove_auth(self, list_id: str):
        """
        Removes an authorisation token for the given list ID from botblock.org

        Parameter
        ========

        list_id: str
            The ID of the list from botblock.org
        """
        self.base.remove_auth(list_id)

    async def post_count(self) -> dict:
        """
        POST current server/guild count based on bot data

        Returns
        =======

        json: dict
            The response from the API endpoint
        """
        return await self.base.post_guild_count(self.bot.user.id, self.guild_count)

    def start_loop(self):
        """
        Start a loop that automatically updates the server/guild count for the bot
        """
        self.bot.loop.create_task(self.__loop(self.interval))

    async def __loop(self, interval: float):
        """
        The internal loop used for automatically posting server/guild count stats
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.post_count()
            await asyncio.sleep(interval)

    async def get_bot_info(self, bot_id: int) -> Tuple[Union[User, None], dict]:
        """
        GET information about a bot

        Parameter
        ========

        bot_id: int
            The ID of the bot you want to fetch from the API

        Returns
        =======

        user: Union[User, None]
            The User object from discord.py if found or None

        json: dict
            The response from the API endpoint
        """
        # Attempt to fetch from Discord
        try:
            user_info = await self.bot.get_user_info(str(bot_id))
        except AttributeError:
            user_info = await self.bot.fetch_user(bot_id)
        except:
            user_info = None

        # Get from API
        api_result = await self.base.get_bot_information(bot_id)

        # Inject Discord data
        if user_info and api_result:
            api_result['username'] = user_info.name
            api_result['discriminator'] = str(user_info.discriminator)

        # Failed
        if not user_info and not api_result['username']:
            raise NotFound()

        # Return
        return (user_info, api_result)
