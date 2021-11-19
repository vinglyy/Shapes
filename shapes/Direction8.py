# -*- coding: utf-8 -*-
"""
Modul definuje atributy reprezentující instance výčtového typu
definujícího 9 směrů: 4 hlavní, 4 vedlejší a směr "NIKAM".

Author:  Rudolf PECINOVSKÝ
Version: 2021_Summer
"""


class _Dir8:
    """Třída definující instanční metody jednotlivých směrů.
    """

    _ord = 0    # Pořadí vytvářené instance

    def __init__(self, short: str, long: str):
        """Každá instance bude znát svůj krátký a dlouhý název
        a svůj index v rámci ostatních instancí.
        Po vytvoření zadaného počtu instancí odmítne vytvářet další.
        """
        if _Dir8._ord < 0:
            raise Exception("Nelze vytvářet další instance výčtového typu")
        self._ordinal = _Dir8._ord;      _Dir8._ord += 1
        self._short   = short
        self._long    = long
        if self._short == 'X':  _Dir8._ord = -1     # Další už nebudou

    def _o4(self): return self._ordinal // 2
    def _o8(self): return self._ordinal
    def _sh(self): return self._short
    def _lo(self): return self._long

    ordinal4  = property(_o8, doc='Pořadí mezi hlavními směry')
    ordinal8  = property(_o8, doc='Pořadí mezi všemi směry')
    long_name = property(_lo, doc='Dlouhý název')
    short_name= property(_sh, doc='Zkratka názvu')

    def turn_by(self, eighths: int):
        """Vrátí směr otočený o zadaný počet 45° vlevo.
        """
        if self is X:  return X
        return values8[(self._ordinal + 8 + eighths) % 8]

    def turn_left(self):
        """Vrátí směr otočený o 90° vlevo.
        """
        self.turn_by(2)

    def turn_right(self):
        """Vrátí směr otočený o 90° vpravo.
        """
        return self.turn_by(-2)

    def half_left(self):
        """Vrátí směr otočený o 45° vlevo.
        """
        self.turn_by(1)

    def half_right(self):
        """Vrátí směr otočený o 45° vpravo.
        """
        self.turn_by(-1)

    def turn_around(self):
        """Vrátí směr otočený o 180°.
        """
        self.turn_by(4)

E  = EAST       = _Dir8("E",  "EAST")
NE = NORTH_EAST = _Dir8("NE", "NORTH_EAST")
N  = NORTH      = _Dir8("N",  "NORTH")
NW = NORTH_WEST = _Dir8("NW", "NORTH_WEST")
W  = WEST       = _Dir8("W",  "WEST")
SW = SOUTH_WEST = _Dir8("SW", "SOUTH_WEST")
S  = SOUTH      = _Dir8("S",  "SOUTH")
SE = SOUTH_EAST = _Dir8("SE", "SOUTH_EAST")
X  = NOWHERE    = _Dir8("X",  "NOWHERE")

values4 = (E,     N,     W,     S,      )
values8 = (E, NE, N, NW, W, SW, S, SE,  )
values9 = (E, NE, N, NW, W, SW, S, SE, X)
