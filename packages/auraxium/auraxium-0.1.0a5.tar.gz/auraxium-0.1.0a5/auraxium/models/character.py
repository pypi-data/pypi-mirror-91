"""Data classes for :mod:`auraxium.ps2.character`."""

from typing import Optional

from ..base import Ps2Data
from ..types import LocaleData

__all__ = [
    'CharacterAchievement',
    'CharacterData',
    'CharacterDirective',
    'TitleData'
]

# pylint: disable=too-few-public-methods


class CharacterAchievement(Ps2Data):
    """Data container for a character's achievement status.

    Attributes:
        character_id: The ID of the character for this entry.
        achievement_id: The ID of the achievement for this entry.
        earned_count: How often the character has earned the given
            achievement.
        start: The UTC timestamp the character started progression
            towards this achievement at.
        start_date: Human-readable version of :attr:`start`.
        finish: The time the character completed this achievement. Only
            valid for one-time achievements such as medals.
        finish_date: Human-readable version of :attr:`finish`.
        last_save: The last time the character gained this
            achievement at as a UTC timestamp.
        last_save_date: Human-readable version of :attr:`last_save`.

    """

    character_id: int
    achievement_id: int
    earned_count: int
    start: int
    start_date: str
    finish: int
    finish_date: str
    last_save: int
    last_save_date: str


class CharacterData(Ps2Data):
    """Data class for :class:`auraxium.ps2.character.Character`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        character_id: The unique name of the character.
        name: The name of the player.
        faction_id: The faction the character belongs to.
        head_id: The head model for this character.
        title_id: The current title selected for this character. May be
            zero.
        times: Play and login time data for the character.
        certs: Certification data for the character.
        battle_rank: Battle rank data for the character.
        profile_id: The last profile the character used.
        daily_ribbon: Daily ribbon data for the character.
        prestige_level: The ASP rank of the character.

    """

    class BattleRank(Ps2Data):
        """Object representation of the "battle_rank" sub-key.

        Attributes:
            value: The current battle rank.
            percent_to_next: The progress to the next battle rank.

        """

        value: int
        percent_to_next: float

    class Certs(Ps2Data):
        """Object representation of the "certs" sub-key.

        Attributes:
            earned_points: Certification points the player has ever
                earned.
            gifted_points: Certification points the player was gifted
                through events.
            spent_points: Certification points the character has spent.
            available_points: The current certification point balance
                of the character.
            percent_to_next: The progress to the next certification
                point for the character.

            """

        earned_points: int
        gifted_points: int
        spent_points: int
        available_points: int
        percent_to_next: float

    class DailyRibbon(Ps2Data):
        """Object representation of the "daily_ribbon" sub-key.

        Attributes:
            count: The number of daily ribbon bonuses available.
            time: (Not yet documented)
            date: Human-readable version of :attr:`time`.

        """

        count: int  # type: ignore
        time: Optional[int] = None
        date: Optional[str] = None

    class Name(Ps2Data):
        """Object representation of the "name" sub-key.

        Attributes:
            first: The name of the character.
            first_lower: Lowercase version of :attr:`first`.

        """

        first: str
        first_lower: str

    class Times(Ps2Data):
        """Object representation of the "times" sub-key.

        Attributes:
            creation: The time the character was created.
            creation_date: Human-readable version of :attr:`creation`.
            last_save: The last time the character was updated. This
                roughly matches the last time the character logged out.
            last_save_date: Human-readable version of
                :attr:`last_save`.
            last_login: The last time the character logged in.
            last_login_date: Human-readable version of
                :attr:`last_login_date`.
            login_count: The number of times the character has logged
                in.
            minutes_played: The total number of minutes this character
                was logged into PS2.

            """

        creation: int
        creation_date: str
        last_save: int
        last_save_date: str
        last_login: int
        last_login_date: str
        login_count: int
        minutes_played: int

    character_id: int
    name: Name
    faction_id: int
    head_id: int
    title_id: int
    times: Times
    certs: Certs
    battle_rank: BattleRank
    profile_id: int
    daily_ribbon: DailyRibbon
    prestige_level: int


class CharacterDirective(Ps2Data):
    """Data container for a character's directive status.

    Attributes:
        character_id: The ID of the character for this entry.
        directive_tree_id: The ID of the directive tree for this entry.
        directive_id: The ID of the directive for this entry.
        completion_time: The time the character completed this
            directive.
        completion_time_date: Human-readable version of
            :attr:`completion_time`.

    """

    character_id: int
    directive_tree_id: int
    directive_id: int
    completion_time: int
    completion_time_date: str


class TitleData(Ps2Data):
    """Data class for :class:`auraxium.ps2.character.Title`.

    .. important::
        Unlike most other forms of API data, the ID used by titles is
        **not** unique.

        This is due to the ASP system re-using the same title IDs while
        introducing a different name ("A.S.P. Operative" for ``en``).

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        title_id: The ID of this title.
        name: The localised name of this title.

    """

    title_id: int
    name: LocaleData
