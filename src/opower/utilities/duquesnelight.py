"""Duquesne Light"""

from typing import Optional

import aiohttp

from .base import UtilityBase

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
        raise NotImplementedError
