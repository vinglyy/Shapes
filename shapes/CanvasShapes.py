import tkinter

from .NamedColor import CREAMY


class CanvasShapes(tkinter.Canvas):
    """
    Třída která dědí Canvas(plátno). Na toto plátno se následně vykreslí
    jednotlivé tvary balíčku shapes.
    Tato třída je instancována jednou při importování balíčku shapes.
    """

    def __init__(self, canvas_color=CREAMY, canvas_width=600, canvas_height=600):
        """
        Vytvoří instanci plátna.
        :param canvas_color: Barva pozadí plátna
        :param canvas_width: Šířka plátna
        :param canvas_height: Výška plátna
        """
        tkinter.Canvas.__init__(self)
        self.master.title("Plátno")
        # self.master.geometry(f"{pos_x}+{pos_y}")
        self.canvas_color = canvas_color
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # pokud si neuložíte tvary tak jsou všechny v tomto atributu
        self.all_shapes = []

        # nastaví různé atributy plátna
        self.config(bg=self.canvas_color.tkn,
                    width=self.canvas_height,
                    height=self.canvas_width)
        # aktivuje správce geometrie
        self.pack()

    def change_canvas_size(self, height: int, width: int) -> None:
        """
        Změní výšku a šířku plátna
        :param height: výška
        :param width: šířka
        """
        self.canvas_width = width
        self.canvas_height = height
        self._update_canvas_config()

    def _update_canvas_config(self) -> None:
        """
        Aktualizuje platno
        """
        self.config(bg=self.canvas_color.tkn, width=self.canvas_height,
                    height=self.canvas_width)
        self.pack()
        self.master.attributes("-topmost", True)

    def change_canvas_color(self, bg_color) -> None:
        """
        Změní barvu pozadí plátna.
        :param bg_color: nová barva
        """
        self.canvas_color = bg_color
        self.config(bg=self.canvas_color.tkn)
        self.update()

    def update_shapes(self) -> None:
        """
        Aktualizuje tvary na plátně.
        """
        self.update()


# o kolik skáčou obrazce
canvas_step = 50

# Vytvoří plátno
canvas = CanvasShapes()
