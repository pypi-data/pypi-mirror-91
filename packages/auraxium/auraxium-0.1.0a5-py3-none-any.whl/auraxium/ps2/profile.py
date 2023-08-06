"""Profile and loadout class definitions."""

from typing import Final

from ..base import Cached, FallbackMixin
from ..census import Query
from ..models import LoadoutData, ProfileData
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData

from .armour import ArmourInfo
from .faction import Faction
from .resist import ResistInfo


class Profile(Cached, cache_size=200, cache_ttu=60.0):
    """An entity in the game world.

    This is used to specify the resistance and armour values to
    apply to a given object.

    Profiles include faction-specific classes, vehicles, facility
    infrastructure such as turrets, generators or shields, as well as
    other non-static entities such as Cortium nodes or pumpkins.
    """

    collection = 'profile_2'
    data: ProfileData
    dataclass = ProfileData
    id_field = 'profile_id'

    def armour_info(self) -> SequenceProxy[ArmourInfo]:
        """Return the armour info of the profile.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'profile_armor_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(ArmourInfo.collection)
        join.set_fields(ArmourInfo.id_field)
        return SequenceProxy(ArmourInfo, query, client=self._client)

    def resist_info(self) -> SequenceProxy[ResistInfo]:
        """Return the resist info of the profile.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'profile_resist_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(500)
        join = query.create_join(ResistInfo.collection)
        join.set_fields(ResistInfo.id_field)
        return SequenceProxy(ResistInfo, query, client=self._client)


def _get_fallback(id_: int) -> CensusData:
    profile_id = id_ + 162 if id_ != 45 else 252
    code_name = {
        28: 'NSO Infiltrator',
        29: 'NSO Light Assault',
        30: 'NSO Medic',
        31: 'NSO Engineer',
        32: 'NSO Heavy Assault',
        45: 'NSO MAX'}
    return {
        'loadout_id': id_,
        'profile_id': profile_id,
        'faction_id': 4,
        'code_name': code_name[id_]}


class Loadout(Cached, FallbackMixin, cache_size=20, cache_ttu=3600.0):
    """Represents a faction-specific infantry class."""

    collection = 'loadout'
    data: LoadoutData
    dataclass = LoadoutData
    id_field = 'loadout_id'
    _fallback = {k: _get_fallback(k) for k in (*range(28, 33), 45)}

    def armour_info(self) -> SequenceProxy[ArmourInfo]:
        """Return the armour info of the loadout.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'profile_armor_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        query.limit(20)
        join = query.create_join(ArmourInfo.collection)
        join.set_fields(ArmourInfo.id_field)
        return SequenceProxy(ArmourInfo, query, client=self._client)

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction of the loadout.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=self.data.faction_id)
        return InstanceProxy(Faction, query, client=self._client)

    def profile(self) -> InstanceProxy[Profile]:
        """Return the profile of the loadout.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Profile.collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        return InstanceProxy(Profile, query, client=self._client)

    def resist_info(self) -> SequenceProxy[ResistInfo]:
        """Return the resist info of the loadout.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'profile_resist_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        query.limit(500)
        join = query.create_join(ResistInfo.collection)
        join.set_fields(ResistInfo.id_field)
        return SequenceProxy(ResistInfo, query, client=self._client)
