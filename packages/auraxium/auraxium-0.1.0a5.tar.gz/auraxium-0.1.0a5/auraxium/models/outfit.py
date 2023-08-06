"""Data classes for :mod:`auraxium.ps2.outfit`."""

from ..base import Ps2Data

__all__ = [
    'OutfitData',
    'OutfitMemberData',
    'OutfitRankData'
]

# pylint: disable=too-few-public-methods


class OutfitData(Ps2Data):
    """Data class for :class:`auraxium.ps2.outfit.Outfit`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        outfit_id: The unique ID of the outfit.
        name: The name of the outfit.
        name_lower: Lowercase version of :attr`name`. Useful for
            optimising case-insensitive searches.
        alias: The alias (or tag) of the outfit.
        alias_lower: Lowercase version of :attr:`alias`. Useful for
            optimising case-insensitive searches.
        time_created: The creation date of the outfit as a UTC
            timestamp.
        time_created_date: Human-readable version of
            :attr:`time_created`.
        leader_character_id: The character/member ID of the outfit
            leader.
        member_count: The number of members in the outfit.

    """

    outfit_id: int
    name: str
    name_lower: str
    alias: str
    alias_lower: str
    time_created: int
    time_created_date: str
    leader_character_id: int
    member_count: int


class OutfitMemberData(Ps2Data):
    """Data class for :class:`auraxium.ps2.outfit.OutfitMember`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        outfit_id: The ID of the outfit this member is a part of.
        character_id: The ID of the associated character.
        member_since: The date the character joined the outfit at as
            a UTC timestamp.
        member_since_date: Human-readable version of
            :attr:`member_since`.
        rank: The name of the member's in-game outfit rank.
        rank_ordinal: The ordinal position of the member's rank within
            the outfit. The lower the value, the higher the rank.

    """

    outfit_id: int
    character_id: int
    member_since: int
    member_since_date: str
    rank: str
    rank_ordinal: int


class OutfitRankData(Ps2Data):
    """Data class for :class:`auraxium.ps2.outfit.OutfitRank`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        outfit_id: The unique ID of the outfit the rank belongs to.
        ordinal: The position of the rank within the outfit, lower
            values indicate higher ranks.
        name: The name of the rank.
        description: The description of the rank.

    """

    outfit_id: int
    ordinal: int
    name: str
    description: str
