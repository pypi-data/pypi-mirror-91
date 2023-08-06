"""Vehicle class definitions."""

from typing import Final, List, Optional, Union

from ..base import Cached, ImageMixin, Named
from ..census import Query
from ..client import Client
from ..models import VehicleAttachmentData, VehicleData
from ..proxy import InstanceProxy, SequenceProxy

from .faction import Faction
from .item import Item
from .skill import SkillSet


class Vehicle(Named, ImageMixin, cache_size=50, cache_ttu=3600.0):
    """A mountable vehicle in PlanetSide 2.

    This includes aircraft and ground vehicles, as well as mountable
    turrets and constructible.
    """

    collection = 'vehicle'
    data: VehicleData
    dataclass = VehicleData
    id_field = 'vehicle_id'

    def factions(self) -> SequenceProxy[Faction]:
        """Return the factions that have access to this vehicle.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'vehicle_faction'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Vehicle.id_field, value=self.id)
        query.limit(5)
        return SequenceProxy(Faction, query, client=self._client)

    @classmethod
    async def get_by_faction(cls, faction: Union[Faction, int], *,
                             client: Client) -> List['Vehicle']:
        """Return all vehicles available to the given faction."""
        collection: Final[str] = 'vehicle_faction'
        faction_id = faction.id if isinstance(faction, Faction) else faction
        query = Query(collection, service_id=client.service_id)
        query.add_term(field=Faction.id_field, value=faction_id)
        query.limit(500)
        join = query.create_join(cls.collection)
        join.set_fields(cls.id_field)
        proxy: SequenceProxy['Vehicle'] = SequenceProxy(
            cls, query, client=client)
        return await proxy.flatten()

    def skill_sets(self, faction: Optional[Union[Faction, int]] = None
                   ) -> SequenceProxy[SkillSet]:
        """Return the skill sets associated with this vehicle.

        By default, this will list all skill sets for all empires. Note
        that this may result in duplicate results as some skill sets
        exist for all empires.
        To avoid duplicates, either generate a set from the returned
        proxy, or specify the faction to resolve skill sets for.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'vehicle_skill_set'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        if faction is not None:
            faction = faction.id if isinstance(faction, Faction) else faction
            query.add_term(field=Faction.id_field, value=faction)
        query.limit(500)
        query.sort('display_index')
        join = query.create_join(SkillSet.collection)
        join.set_fields(SkillSet.id_field)
        return SequenceProxy(SkillSet, query, client=self._client)


class VehicleAttachment(Cached, cache_size=250, cache_ttu=180.0):
    """Links vehicles to the items and attachments they support."""

    collection = 'vehicle_attachment'
    data: VehicleAttachmentData
    dataclass = VehicleAttachmentData
    id_field = 'vehicle_attachment_id'

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction this attachment is available to.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=self.data.faction_id)
        return InstanceProxy(Faction, query, client=self._client)

    def item(self) -> InstanceProxy[Item]:
        """Return the attachable item for the vehicle.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=self.data.item_id)
        return InstanceProxy(Item, query, client=self._client)

    def vehicle(self) -> InstanceProxy[Vehicle]:
        """Return the vehicle the item may be attached to.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Vehicle.collection, service_id=self._client.service_id)
        query.add_term(field=Vehicle.id_field, value=self.data.vehicle_id)
        return InstanceProxy(Vehicle, query, client=self._client)
