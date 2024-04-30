# -*- coding: utf-8 -*-
"""
Balíček shapes určený pro výuku programování v objektově orientovaném
prostředí.
Při importu balíčku se vytvoří instanci třídy Canvas, která
implementuje Canvas z tkinter. Tato třída představuje plátno, na
které se dá kreslit tvary.
Tyto tvary se dají kreslit vytvořením instancí tvarů.
Tvary které se dají vytvořit:
    jednoduché obrazce:
        Rectangle,
        Elipse,
        Triangle
    složitější obrazce:
        Multishape
    a text
Příklad vytvoření čtverce:
import shapes
shapes.Rectangle(10,10,10,10,BLACK)

Pokud bude použita Python konzole, tak to takto stačí.
Pokud ovšem chcete tento balíček použít ve skriptu tak na konec
musíte připojit příkaz:
shapes.mainloop()
Autor: Jan Lampa
verze: 1.3 29.04.2024
"""

from .CanvasShapes import canvas, canvas_step
from .Multishape import Multishape
from .Rectangle import Rectangle
from .Triangle import Triangle
from .Ellipse import Ellipse
from .Text import Text
from .NamedColor import *
from .Direction8 import *



def mainloop() -> None:
    """
    Tuto metodu je třeba použít na konec skriptu pokud chcete,
    aby okno zůstalo po vykonání skriptu.
    """
    canvas.mainloop()
