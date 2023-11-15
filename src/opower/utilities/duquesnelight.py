"""Duquesne Light"""

import re
import logging
from typing import Optional
import urllib.parse

import aiohttp

from ..const import USER_AGENT
from ..exceptions import InvalidAuth
from .base import UtilityBase

_LOGGER = logging.getLogger(__file__)

class DuquesneLight(UtilityBase):
    """Duquesne Light"""

    @staticmethod
    def name() -> str:
        """Distinct recognizable name of the utility."""
        return "Duquesne Light Company"
    
    @staticmethod
    def subdomain() -> str:
        """Return the opower.com subdomain for this utility."""
        return "duq"

    @staticmethod
    def timezone() -> str:
        """Return the timezone.

        Should match the siteTimeZoneId of the API responses.
        """
        return "America/New_York"
    
    @staticmethod
    async def async_login(
        session: aiohttp.ClientSession,
        username: str,
        password: str,
        optional_mfa_secret: Optional[str],
    ) -> Optional[str]:
        """Login to the utility website.

        Return the Opower access token or None if this function authorizes with Opower in other ways.

        :raises InvalidAuth: if login information is incorrect
        """
   
        # First, get logged in so we have a valid AuthToken cookie
        login_url = "https://www.duquesnelight.com/login/login"
        async with session.post(
            "https://www.duquesnelight.com/login/login",
            data={
                'Username': username,
                'Password': password,
            },
            headers={"User-Agent": USER_AGENT},
            raise_for_status=True,
        ) as resp:
            result = await resp.json()
            if "Messages" in result:
                raise InvalidAuth(', '.join(result["Messages"]))

        # Then, visit a page that has the OPower token embedded
        async with session.get(
            "https://www.duquesnelight.com/energy-money-savings/my-electric-use",
            headers={"User-Agent": USER_AGENT},
            raise_for_status=True,
        ) as resp:
            result = await resp.text()
        match = re.search('"OPowerToken": "([^"]+)"', result)
        if not match:
            _LOGGER.debug("Unable to find OPowerToken: %s", result)
            raise InvalidAuth("Could not extract OPowerToken")
        opowertoken = match.group(1)
        return opowertoken
