import numpy as np
from nastranpy.bdf.cards.card_interfaces import Item, Set
from nastranpy.bdf.cards.class_factory import class_factory
from nastranpy.bdf.cards.card import Card


GRID = class_factory(Item.grid, ['GRID', None, [Item.coord, 'CP'], [None, 'X1'], [None, 'X2'], [None, 'X3'], [Item.coord, 'CD'], [None, 'PS'], [None, 'SEID']])

class Grid(GRID):
    type = Item.grid

    def __init__(self, fields, large_field=False, free_field=False):
        super().__init__(fields, large_field=large_field, free_field=free_field)
        self.xyz0 = None
        self.elems = set()

    def update(self):

        if self.xyz0 is None:
            cp = self.fields[2]

            if cp:
                self.xyz0 = cp.get_xyz0(np.array(self.fields[3:6]))
            else:
                self.xyz0 = np.array(self.fields[3:6])

    @property
    def xyz(self):

        if self.xyz0 is None:
            return np.array(self.fields[3:6])

        cp = self.fields[2]

        if cp:
            return cp.get_xyz(self.xyz0)
        else:
            return self.xyz0

    @xyz.setter
    def xyz(self, value):
        self.fields[3:6] = value
        cp = self.fields[2]

        if cp:
            self.xyz0 = cp.get_xyz0(value)
        else:
            self.xyz0 = value

    def get_fields(self):
        self.fields[3:6] = self.xyz
        return super().get_fields()