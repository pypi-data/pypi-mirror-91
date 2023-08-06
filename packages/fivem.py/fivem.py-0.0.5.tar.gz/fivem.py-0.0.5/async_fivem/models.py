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

from dataclasses import dataclass
import typing


@dataclass
class Identifiers:
    licenses: typing.List[str]
    discord_id: int
    steam_id: str
    fivem_id: int
    xbl: int
    live: int


@dataclass
class Player:
    endpoint: str
    id: int
    identifiers: Identifiers
    name: str
    ping: float


@dataclass
class Dynamic:
    clients: int
    gametype: str
    hostname: str
    iv: int
    mapname: str
    sv_maxclients: int


@dataclass
class Vars:
    banner_connecting: str
    banner_detail: str
    game_name: str
    onesync_enabled: bool
    sv_enhanced_host_support: bool
    sv_lan: bool
    sv_license_key_token: str
    sv_max_clients: int
    sv_queue_connected_count: int
    sv_queue_connecting_count: int
    sv_queue_count: int
    sv_script_hook_allowed: bool
    tags: list


@dataclass
class Info:
    enhanced_host_support: bool
    icon: bytes
    resources: list
    server: str
    vars: Vars
    version: int
