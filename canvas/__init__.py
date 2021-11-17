# -*- coding: utf-8 -*-

from .CanvasManager import *

# Vytvoří canvas
canvas = Canvas()


def show_canvas() -> None:
    """Zkratka"""
    canvas.show_canvas()


def mainloop() -> None:
    """
    Tuto metodu je třeba použít na konec scriptu pokud chcete,
    aby okno zůstalo po vykonání skriptu.
    """
    canvas.mainloop()
