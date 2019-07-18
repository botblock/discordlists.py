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


class DiscordListsException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RequestFailure(DiscordListsException):
    def __init__(self, status: int, response: str):
        super().__init__("{}: {}".format(status, response))


class Ratelimited(DiscordListsException):
    def __init__(self, json=None):
        super().__init__("The request to the API endpoint was ratelimited." +
                         ("\nPlease re-attempt this request after {:,} seconds.".format(json['retry_after'])
                          if json and "retry_after" in json else ""))


class EmptyResponse(DiscordListsException):
    def __init__(self):
        super().__init__("No response was received from the API")


class NotFound(DiscordListsException):
    def __init__(self):
        super().__init__("The requested entity was not found")
