"""Data classes for :mod:`auraxium.ps2.currency`."""

from ..base import Ps2Data
from ..types import LocaleData

__all__ = [
    'CurrencyData'
]

# pylint: disable=too-few-public-methods


class CurrencyData(Ps2Data):
    """Data class for :class:`auraxium.ps2.currency.Currency`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        currency_id: The unique ID of this currency entry.
        name: The localised name of this currency.
        icon_id: The image ID of the currency icon image asset.
        inventory_cap: The maximum amount of this currency a character
            may hold.

    """

    currency_id: int
    name: LocaleData
    icon_id: int
    inventory_cap: int
