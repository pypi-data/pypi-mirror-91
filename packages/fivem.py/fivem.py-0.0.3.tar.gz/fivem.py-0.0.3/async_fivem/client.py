"""
Copyright (c) 2021 Wiper-R

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import typing
import aiohttp
from .exceptions import HttpException
from .models import Dynamic, Identifiers, Info, Player, Vars


def parse_int(val):
    if val:
        return int(val)
    return val


class Route:
    def __init__(self, method: str, endpoint: str, **kwargs):
        BASE_URL = kwargs.pop('url')
        self.url = BASE_URL + endpoint
        self.kwargs = kwargs
        self.endpoint = endpoint
        self.method = method


class HttpClient:
    def __init__(self, **kwargs):
        self.loop = kwargs.get('loop')
        self.return_defaults = kwargs.get('return_defaults', False)
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.ip = kwargs.pop('ip')
        self.port = kwargs.pop('port')
        self.url = f'http://{self.ip}:{self.port}'

    async def request(self, route: Route):
        # Ensuring that session isn't closed
        if self.session.closed:
            self.session = aiohttp.ClientSession(loop=self.loop)

        try:
            type = route.kwargs.pop('type')
        except KeyError:
            type = dict

        response = await self.session.request(route.method, route.url, **route.kwargs)

        try:
            response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            if self.return_defaults:
                return type()

            raise HttpException(
                f'Message: {e.message}\nResponse: {e.status}'
            )

        return await response.json(content_type=None)

    async def fetch_players(self, **kwargs):
        route = Route('GET', '/players.json', url=self.url, **kwargs)
        return await self.request(route)

    async def fetch_info(self, **kwargs):
        route = Route('GET', '/info.json', url=self.url, **kwargs)
        return await self.request(route)

    async def fetch_dynamic(self, **kwargs):
        route = Route('GET', '/dynamic.json', url=self.url, **kwargs)
        return await self.request(route)


class Client:
    def __init__(self, ip: str, port: str, loop: asyncio.AbstractEventLoop = None,):
        if loop is not None:
            assert isinstance(
                loop, asyncio.AbstractEventLoop), f'Loop must be of type asyncio.AbstractEventLoop got {type(loop)}'
        self.http = HttpClient(loop=loop, ip=ip, port=port)

    async def fetch_players(self, raw=False) -> typing.List[Player]:
        """[summary]

        Args:
            raw (bool, optional): If True it returns a raw list received from server, otherwise Player Defaults to False.

        Returns:
            Players: List of Players
        """
        data = await self.http.fetch_players(type=list)

        if raw:
            return data

        players = []

        for raw in data:
            endpoint = raw.get('endpoint')
            id = parse_int(raw.get('id'))
            name = raw.get('name')
            ping = float(raw.get('ping'))

            # Parsing Identifiers
            identifiers: typing.List[str] = raw.get('identifiers', [])
            licenses = []
            discord_id = None
            steam_id = None
            fivem_id = None
            xbl = None
            live = None

            for identifier in identifiers:
                if identifier.startswith('license'):
                    licenses.append(identifier.split(':')[1])

                elif identifier.startswith('discord'):
                    discord_id = parse_int(identifier.split(':')[1])

                elif identifier.startswith('steam'):
                    steam_id = identifier.split(':')[1]

                elif identifier.startswith('fivem'):
                    fivem_id = identifier.split(':')[1]

                elif identifier.startswith('xbl'):
                    xbl = identifier.split(':')[1]

                elif identifier.startswith('live'):
                    live = identifier.split(':')[1]

            identifiers = Identifiers(
                licenses,
                discord_id,
                steam_id,
                fivem_id,
                xbl,
                live
            )

            player = Player(
                endpoint,
                id,
                identifiers,
                name,
                ping
            )

            players.append(player)

        return players

    async def fetch_dynamic(self, raw=False) -> Dynamic:
        """
        Returns:
            Dynamic: Dynamic Info of FivM Server.
        """
        data = await self.http.fetch_dynamic(type=dict)

        if raw:
            return data

        clients = int(data.get('clients', 0))
        gametype = data.get('gametype')
        hostname = data.get('hostname', '127.0.0.1')
        iv = parse_int(data.get('iv'))
        mapname = data.get('mapname')
        max_clients = parse_int(data.get('sv_maxclients'))
        return Dynamic(
            clients,
            gametype,
            hostname,
            iv,
            mapname,
            max_clients
        )

    def parse_vars(self, data):
        vars = data.get('vars', {})
        banner_connecting = vars.get('banner_connecting')
        banner_detail = vars.get('banner_detail')
        gamename = vars.get('gamename')
        onesync_enabled = vars.get('onesync_enabled')
        sv_enhanced_host_support = vars.get('sv_enhancedHostSupport')
        sv_lan = vars.get('sv_lan')
        sv_license_key_token = vars.get('sv_licenseKeyToken')
        sv_max_clients = parse_int(vars.get('sv_maxClients', 64))
        sv_queue_connected_count = parse_int(
            vars.get('sv_queueConnectedCount'))
        sv_queue_connecting_count = parse_int(
            vars.get('sv_queueConnectingCount'))

        sv_queue_count = parse_int(vars.get('sv_queueCount'))
        sv_script_hook_allowed = vars.get('sv_scriptHookAllowed')
        tags = vars.get('tags', '').split(', ')

        return Vars(
            banner_connecting,
            banner_detail,
            gamename,
            onesync_enabled,
            sv_enhanced_host_support,
            sv_lan,
            sv_license_key_token,
            sv_max_clients,
            sv_queue_connected_count,
            sv_queue_connecting_count,
            sv_queue_count,
            sv_script_hook_allowed,
            tags
        )

    async def fetch_info(self, raw=False, need_icon=True) -> Info:
        """
        Args:
            need_icon (bool, optional): If this set to false, the icon returned by this function will be a empty byte. Defaults to True.

        Returns:
            Info: Info About FiveM Server.
        """
        data = await self.http.fetch_info(type=dict)

        if raw:
            return data

        enhanced_host_support = data.get('enhancedHostSupport', False)

        if need_icon:
            icon = data.get('icon', b'')
        else:
            icon = b''

        resources = data.get('resources', [])
        server = data.get('server')
        version = parse_int(data.get('version'))
        vars = self.parse_vars(data)

        return Info(enhanced_host_support, icon, resources, server, vars, version,)
