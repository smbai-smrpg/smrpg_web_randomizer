# Data module for areas and location data and base classes for key item/chest shuffle..

from enum import Enum, auto

from randomizer.data import items
from randomizer.logic import utils
from randomizer.logic.patch import Patch


class Area(Enum):
    MariosPad = auto()
    MushroomWay = auto()
    MushroomKingdom = auto()
    BanditsWay = auto()
    KeroSewers = auto()
    TadpolePond = auto()
    RoseWay = auto()
    RoseTown = auto()
    RoseTownClouds = auto()
    ForestMaze = auto()
    MolevilleMines = auto()
    BoosterPass = auto()
    BoosterTower = auto()
    PipeVault = auto()
    YosterIsle = auto()
    Marrymore = auto()
    SeasideTown = auto()
    Sea = auto()
    SunkenShip = auto()
    LandsEnd = auto()
    BelomeTemple = auto()
    MonstroTown = auto()
    BeanValley = auto()
    NimbusLand = auto()
    BarrelVolcano = auto()
    BowsersKeep = auto()
    Factory = auto()


class ItemLocation:
    """Base class for an item location, either a key item or quest reward or chest."""
    area = Area.MariosPad
    addresses = []
    item = None
    missable = False

    def __init__(self, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld):

        """
        self.world = world

    def __str__(self):
        return '<{}: item {}>'.format(self.__class__.__name__, self.item.__name__)

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self.__class__.__name__

    def get_patch(self):
        """

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = Patch()

        for addr in self.addresses:
            patch.add_data(addr, utils.ByteField(self.item.index).as_bytes())

        return patch

    @staticmethod
    def can_access(inventory):
        """

        Args:
            inventory(Inventory): Current inventory of collected items.

        Returns:
            bool: True if this location is accessible with the given inventory, False otherwise.

        """
        return True

    def item_allowed(self, item):
        """

        Args:
            item(randomizer.data.items.Item): Item to check.

        Returns:
            bool: True if the given item is allowed to be placed in this spot, False otherwise.

        """
        # If this is a missable location, it cannot contain a key item.
        if self.missable and not utils.isclass_or_instance(item, items.ChestReward) and item.is_key:
            return False

        # Normal locations can be anything except an invincibility star.
        return not utils.isclass_or_instance(item, items.InvincibilityStar)

    @property
    def has_item(self):
        return self.item is not None
