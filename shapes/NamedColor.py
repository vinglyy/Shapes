# -*- coding: utf-8 -*-
"""
Modul definuje multiton pojmenovaných barev.
Umožňuje vytvářet nové barvy, ale nepovoluje vytvářet barvy,
které již existují.

Author:  Rudolf PECINOVSKÝ
Version: 2021_Summer
"""
from typing import Tuple


def getColor(red=-1, green=-1, blue=-1, name=None):
    """Vrátí barvu se zadaným názvem, resp. rgb charakteristikami.
    Není-li ještě vytvořena, vytvoří ji.
    Pro vyhledání barvy je třeba zadat název nebo rgb charakteristiky.
    Pro vytvoření barvy je třeba zadat oboje.
    Je-li některá z barevných složek zadána záporná,
    hledá se barva se zadaným názvem.
    Jsou-li všechny složky nezáporné, kontroluje se,
    zda již neexistuje barva se stejným názvem a různými složkami.
    nebo se stejnými složkami a různým názvem.
    Existuje-li, vyhodí se výjimka. Neexistuje-li, vytvoří se nová.
    """
    if (red < 0) or (green < 0) or (blue < 0):  # Barevné složky nezadány
        if name is None:  # Není zadán ani název
            raise Exception(
                f'Je třeba zadat název barvy nebo všechny její rgb složky.')
        else:  # Název zadán je, podívám se, je-li barva již vytvořena
            if name in _name2color:
                return _name2color[name]  # Známá barva - vracím ji
            else:
                raise KeyError(
                    f'Barva se zadaným názvem není definována: {name=}')

    # Už víme, že všechny barevné složky jsou zadány
    rgb = (red, green, blue)

    if _name2color is None:  # Nebyl zadán název
        if rgb in _rgb2color:
            return _rgb2color[rgb]  # Barva existuje => vracím ji
        else:  # Barva ještě neexistuje
            # Vytvořím ji s názvem shodným s názvem pro knihovnu Tkinter
            _not_new = True
            result = _NC(rgb, _create_tkname(*rgb))
            return result

    else:  # Byly zadány složky i název
        if (rgb not in _rgb2color) and (name not in _name2color):
            # Barva se zadanýmm názvem nebo barevnými složkami
            # není zatím vytvořena
            _not_new = True
            result = _NC(rgb, name)
            return result  # Vytvořil jsem ji a vracím ji

        else:  # Název či rgb složka jsou již použity a nesedí
            if rgb in _rgb2color:
                print(f'{(rgb in _rgb2color)=}')
                for col in _rgb2color:
                    print(f'{_rgb2color[col]}')
            if name in _name2color:
                print(f'{(name in _rgb2color)=}')
                for cn in _name2color:
                    print(f'{_name2color[cn]}')
            raise KeyError(
                'Zadané barevné složky nebo název kolidují s některou\n'
                f'existující barvou: {name=}, {rgb=}')


def print_named_colors():
    """Vytiskne definované barvy.
    """
    for name in _name2color:
        print(f'{_name2color[name]}')


############################################################################

def _create_tkname(red: int, green: int, blue: int) -> str:
    """Vytvoří název z hodnot barevných složek."""
    return '#' + hex(0x1_00_00_00
                     + ((red * 256) + green) * 256 + blue)[3:]


class _NC:
    """Třída definující instanční metody jednotlivých barev.
    """

    def __init__(self, rgb: Tuple[int, int, int], name: str):
        """Vytvoří barvu se zadanými barevnými složkam a názvem.
        Tvorba je ale podmíněna - atribut _not_new musí být False
        """
        if _NC._not_new:
            raise Exception('Barvu lze získat pouze prostřednictvím '
                            'volání tovární metody getColor()')
        self._name = name
        self._rgb = rgb
        self._tk_name = _create_tkname(*rgb)
        _name2color[self._name] = self
        _tkname2color[self._tk_name] = self
        _rgb2color[self._rgb] = self
        _NC._not_new = False

    def _n(self): return self._name

    def _t(self): return self._tk_name

    def _c(self): return self._rgb

    name = property(_n, doc='Název barvy')
    rgb = property(_c, doc='Ntice barevných složek')
    tkn = property(_t, doc='Název barvy pro knihovnu Tk')

    _not_new = False

    def __repr__(self):
        return f'NameColor(tkn={self.tkn}, rgb={self.rgb}, ' \
               f'name={self.name})'


############################################################################

_name2color = {}
_tkname2color = {}
_rgb2color = {}

BLACK = getColor(red=0, green=0, blue=0, name='black')
BLUE = getColor(0x00, 0x00, 0xFF, 'blue')  # (0,   0,   255)
RED = getColor(0xFF, 0x00, 0x00, 'red')  # (255, 0,     0)
MAGENTA = getColor(0xFF, 0x00, 0xFF, 'magenta')  # (255, 0,   255)
GREEN = getColor(0x00, 0xFF, 0x00, 'green')  # (0,   255,   0)
CYAN = getColor(0x00, 0xFF, 0xFF, 'cyan')  # (0,   255, 255)
YELLOW = getColor(0xFF, 0xFF, 0x00, 'yellow')  # (255, 255,   0)
WHITE = getColor(0xFF, 0xFF, 0xFF, 'white')  # (255, 255, 255)
GRAY = getColor(0x80, 0x80, 0x80, 'gray')  # (128, 128, 128)
DARK_GRAY = getColor(0x40, 0x40, 0x40, 'dark_gray')  # (64, 64,  64)
PINK = getColor(0xFF, 0xAF, 0xAF, 'pink')  # (255, 175, 175)
ORANGE = getColor(0xFF, 0xC8, 0x00, 'orange')  # (255, 200,   0)
AMBER = getColor(0xFF, 0xCC, 0x00, 'amber')  # (255, 204,   0)
BRICK = getColor(0xFF, 0x66, 0x00, 'brick')  # (255, 102,   0)
BROWN = getColor(0x99, 0x33, 0x00, 'brown')  # (153,  51,   0)
CREAMY = getColor(0xFF, 0xFF, 0xCC, 'creamy')  # (255, 255, 204)
GOLD = getColor(0xFF, 0xE0, 0x00, 'gold')  # (255, 224,   0)
KHAKI = getColor(0x99, 0x99, 0x00, 'khaki')  # (153, 153,   0)
OCHRE = getColor(0xFF, 0x99, 0x00, 'ochre')  # (255, 153,   0)
SILVER = getColor(0xD8, 0xD8, 0xD8, 'silver')  # (216, 216, 216)
STEELY = getColor(0x00, 0x99, 0xCC, 'steely')  # (255, 102,   0)
NO = None
