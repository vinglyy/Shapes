# -*- coding: utf-8 -*-
"""
Tohle je modul CanvasManager, jeho úkolem je vytvořit virtuální
kanvas na , který jde zobrazit následující tvary:
    jednoduché obrazce:
        Rectangle,
        Elipse,
        Triangle
    složitější obrazce:
        Multishape
Tvary mohou měnit velikost, barvu a pozici.
Autor: Jan Lampa
verze: 1.2 16.11.2021
"""
import tkinter
from abc import ABC

from .Abstract_classes import *
from .Direction8 import *
from .NamedColor import *

# o kolik skáčou tvary
canvas_step = 50


class Text(Movable, ID, Paintable, ICopyable):
    """
    Instance třídy Text. Vytvoří normální text na plátně.
    """

    def __init__(self, x=0, y=0, text="text"):
        """
        Vytvoří instanci třídy Text.
        :param x: defaultně 0
        :param y: defaultně 0
        :param text: defaultně "text"
        """
        ID.__init__(self)
        Movable.__init__(self, x, y)
        self.text = text
        Paintable.__init__(self)

    def paint(self) -> None:
        if not self._is_painted_on_canvas:
            canvas.create_text(self.x, self.y, text=self.text, tag=self.__repr__())
            self._is_painted_on_canvas = True
        else:
            canvas.itemconfig(self.__repr__())
            canvas.coords(self.__repr__(), self.get_coord())
            canvas.tag_raise(self.__repr__())
            show_canvas()

    def copy(self):
        """
        Metoda vrátí kopii tvaru
        :return: vrácený tvar
        """
        return Text(self.x, self.y, self.text)

    def set_text(self, text):
        """
        Změní text, který je zobrazen.
        :param text: text
        """
        self.text = text
        self.paint()


class Shape(Resizable, ID, Paintable, ICopyable, ABC):
    """
    Rodičovská implementace obrazců, slouží k tomu aby
    jsme se nemusely psát metody pro některé obrazce
    několikrát.
    Také jsou zde implementována abstraktní třída, aby
    nešlo Shape instancovat .
    """

    def __init__(self, x, y, width, height, color=YELLOW):
        """
        Initializační dunder metoda pro třídu Shape.
        x a y jsou v pravém horním rohu.
        Také počítá id, každý obrazec má svoje číslo
        :param x: osa x
        :param y: osa y, nahoru je méně, dolu je výce
        :param width: šířka obrazce
        :param height: výška obrazce
        :param color: barva obrazce, je třeba použít metody NamedColor
        """
        ID.__init__(self)
        canvas.all_shapes.append(self)
        Resizable.__init__(self, x, y, width, height)

        self.color = color
        Paintable.__init__(self)

    def rub_out(self) -> None:
        """
        Dočasně přebarví tvar na barvu pozadí.
        """
        canvas.itemconfig(self.__repr__(), fill=canvas.canvas_color.tkn)
        show_canvas()

    def change_shape_color(self, color=None) -> None:
        """
        Změní barvu obrazce na tu která je uložená ve třídě,
        pokud vsak požit parametr s platnou COLOR tak na
        tuto barvu.
        """
        if color is not None:
            self.color = color
        canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
        show_canvas()

    def _count_corners(self) -> None:
        """
        Přepočítá souřadnice
        """
        self.corner_1 = (self.x, self.y)
        self.corner_2 = (self.x + self.width, self.y + self.height)

    def get_coord(self) -> list:
        """
        Z 2 corners vytvoří list
        :return: vrací souřadnice v jedné proměnné
        """
        coord = [item for sublist in [self.corner_1, self.corner_2]
                 for item in sublist]
        return coord

    def to_string(self) -> str:
        """
        Metoda vrátí info o obrazci
        :return: String s informavemi o obrazci
        """
        return self.__repr__() + "[x =" + str(self.x) + \
               " y =" + str(self.y) + " height =" + str(self.height) \
               + " width =" + str(self.width) + " color = " + \
               str(self.color.name) + "]"


class Ellipse(Shape):
    """
    Instance třídy Ellipse představují elipsy
    které jsou určeny pro práci na virtuálním plátně
    při prvním seznámení s objekty.
    Jsou definovány svou polohou, velikostí a barvou.
    Poloha instance je definována jako pozice
    levého horního rohu obvodového obdélníku.
    a její velikost je definována jako velikost
    tohoto obdélníku.
    """

    def __init__(self, x=0, y=0, width=2 * canvas_step, height=canvas_step, color=BLUE):
        """
        Vytvoří novou instanci Ellipse
        :param x: Vodorovná souřadnice, levý okraj plátna má x=0,
        souřadnice se zvětšuje směrem doprava.
        defaultně 0
        :param y: Svislá souřadnice, horní okraj plátna má y=0,
        souřadnice se zvyšuje směrem dolů.
        defaultně 0
        :param width: šířka instance
        defaultně 50(2 * canvas_step)
        :param height: výška instance
        defaultně 25 canvas_step
        :param color: barva instance
        defaulně BLUE
        """
        super().__init__(x, y, width, height, color)

    def paint(self) -> None:
        """
        Tato metoda zavolá kanvas a pokud tvar ještě nebyl
        vytvořen tak na něm vytvoří nový, pokud iž byl tak
        aktualizuje tvar na kanvasu podle tagu.
        """
        if not self._is_painted_on_canvas:
            canvas.create_oval(self.get_coord(), tag=self.__repr__(),
                               fill=self.color.tkn, width=0, outline="")
            self._is_painted_on_canvas = True
            show_canvas()
        else:
            canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            canvas.coords(self.__repr__(), self.get_coord())
            canvas.tag_raise(self.__repr__())
            show_canvas()

    def copy(self) -> Shape:
        return Ellipse(self.x, self.y, self.width, self.height, self.color)


class Rectangle(Shape):
    """
    Instance třídy  Rectangle představují obdélníky
    které jsou určeny pro práci na virtuálním plátně
    při prvním seznámení s objekty.
    Jsou definovány svou polohou, velikostí a barvou.
    Pozice instance je definována jako pozice
    jeho levého horního rohu.
    """

    def __init__(self, x=0, y=0, width=2 * canvas_step, height=canvas_step, color=RED):
        """
        Vytvoří novou instanci Rectangle
        :param x: Vodorovná souřadnice, levý okraj plátna má x=0,
        souřadnice se zvětšuje směrem doprava.
        defaultně 0
        :param y: Svislá souřadnice, horní okraj plátna má y=0,
        souřadnice se zvyšuje směrem dolů.
        defaultně 0
        :param width: šířka instance
        defaultně 50(2 * canvas_step)
        :param height: výška instance
        defaultně 25 canvas_step
        :param color: barva instance
        defaultně RED
        """
        super().__init__(x, y, width, height, color)

    def paint(self) -> None:
        """
        Tato metoda zavolá kanvas a pokud tvar ještě nebyl
        vytvořen tak na něm vytvoří nový, pokud iž byl tak
        aktualizuje tvar na kanvasu podle tagu.
        """
        if not self._is_painted_on_canvas:
            canvas.create_rectangle(self.get_coord(), tag=self.__repr__(),
                                    fill=self.color.tkn, width=0)
            self._is_painted_on_canvas = True
            show_canvas()
        else:
            canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            canvas.coords(self.__repr__(), self.get_coord())
            canvas.tag_raise(self.__repr__())
            show_canvas()

    def copy(self) -> Shape:
        return Rectangle(self.x, self.y, self.width, self.height, self.color)


class Triangle(Shape):
    """
    Instance třídy code Triangle představuje trojúhelníky
    které jsou určeny pro práci na virtuálním plátně
    při prvním seznámení s objekty.
    Jsou definovány svou polohou, velikostí, barvou a směrem.
    do kterého je natočen hlavní vrchol.
    Poloha instance je definována jako pozice
    levého horního rohu obvodového obdélníku.
    a její velikost je definována jako velikost tohoto obdélníku.
    Směr trojúhelníku je směr
    do kterého je natočen hlavní vrchol trojúhelníku.
    """

    def __init__(self, x=0, y=0, width=2 * canvas_step,
                 height=canvas_step, color=YELLOW, dir8=NORTH):
        """
        Vytvoří novou instanci Triangle
        :param x: Vodorovná souřadnice, levý okraj plátna má x=0,
        souřadnice se zvětšuje směrem doprava.
        defaultně 0
        :param y: Svislá souřadnice, horní okraj plátna má y=0,
        souřadnice se zvyšuje směrem dolů.
        defaultně 0
        :param width: šířka instance
        defaultně 50(2 * canvas_step)
        :param height: výška instance
        defaultně 25 canvas_step
        :param color: barva instance
        defaulně YELLOW
        :param dir8: Směr, kterým je natočen hlavní vrchol.
        defaultně NORTH
        """
        self.dir8 = dir8
        super().__init__(x, y, width, height, color)

    def paint(self) -> None:
        """
        Tato metoda zavolá kanvas a pokud tvar ještě nebyl
        vytvořen tak na něm vytvoří nový, pokud iž byl tak
        aktualizuje tvar na kanvasu podle tagu.
        """
        if not self._is_painted_on_canvas:
            canvas.create_polygon(self.get_coord(), tag=self.__repr__(),
                                  fill=self.color.tkn, width=0)
            self._is_painted_on_canvas = True
            show_canvas()
        else:
            canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            canvas.coords(self.__repr__(), self.get_coord())
            canvas.tag_raise(self.__repr__())
            show_canvas()

    def get_coord(self) -> list:
        """
        Propočítá body tak aby jsme dostaly výstup, který můžeme
        použít na plátně.
        """
        coord = [int, int, int, int, int, int]
        if self.dir8 == N:
            coord[0] = (self.corner_1[0] + self.corner_2[0]) / 2
            coord[1] = self.corner_1[1]
            coord[2] = self.corner_2[0]
            coord[3] = self.corner_2[1]
            coord[4] = self.corner_1[0]
            coord[5] = self.corner_2[1]
        elif self.dir8 == NE:
            coord[0] = self.corner_2[0]
            coord[1] = self.corner_1[1]
            coord[2] = self.corner_2[0]
            coord[3] = self.corner_2[1]
            coord[4] = self.corner_1[0]
            coord[5] = self.corner_1[1]
        elif self.dir8 == E:
            coord[0] = self.corner_1[0]
            coord[1] = self.corner_1[1]
            coord[2] = self.corner_2[0]
            coord[3] = (self.corner_1[1] + self.corner_2[1]) / 2
            coord[4] = self.corner_1[0]
            coord[5] = self.corner_2[1]
        elif self.dir8 == SE:
            coord[0] = self.corner_2[0]
            coord[1] = self.corner_1[1]
            coord[2] = self.corner_2[0]
            coord[3] = self.corner_2[1]
            coord[4] = self.corner_1[0]
            coord[5] = self.corner_2[1]
        elif self.dir8 == S:
            coord[0] = self.corner_1[0]
            coord[1] = self.corner_1[1]
            coord[2] = self.corner_2[0]
            coord[3] = self.corner_1[1]
            coord[4] = (self.corner_1[0] + self.corner_2[0]) / 2
            coord[5] = self.corner_2[1]
        elif self.dir8 == SW:
            coord[0] = self.corner_1[0]
            coord[1] = self.corner_1[1]
            coord[2] = self.corner_2[0]
            coord[3] = self.corner_2[1]
            coord[4] = self.corner_1[0]
            coord[5] = self.corner_2[1]
        elif self.dir8 == W:
            coord[0] = self.corner_2[0]
            coord[1] = self.corner_1[1]
            coord[2] = self.corner_2[0]
            coord[3] = self.corner_2[1]
            coord[4] = self.corner_1[0]
            coord[5] = (self.corner_1[1] + self.corner_2[1]) / 2
        elif self.dir8 == NW:
            coord[0] = self.corner_1[0]
            coord[1] = self.corner_1[1]
            coord[2] = self.corner_2[0]
            coord[3] = self.corner_1[1]
            coord[4] = self.corner_1[0]
            coord[5] = self.corner_2[1]
        return coord

    def set_direction(self, direction):
        """
        Tato metoda změní směr trojúhelníku.
        :param direction: směr
        """
        self.dir8 = direction
        self.get_coord()
        self.paint()

    def copy(self) -> Shape:
        return Triangle(self.x, self.y, self.width,
                        self.height, self.color, self.dir8)


class Multishape(IMovable, ABC):
    """
    Instance třídy Multishape představuje komplexy geometrických
    tvarů které jsou určeny pro práci na virtuálním plátně při
    prvním seznámení s objekty. Tyto tvary mohou být složeny z
    několika jednodušších tvarů, které jsou instancemi rozhraní
    Shape. Pozice instance je definována jako pozice levého
    horního rohu obvodového obdélníku a její velikost je
    definována jako velikost tohoto obdélníku.
    Multishape je postupně složen z jednodušších tvarů, které
    musí být instancemi rozhraní Shape. Nejsou na ně kladeny
    žádné další požadavky. Během skládání se multishape
    automaticky opravuje své vnitřní informace o své poloze a
    velikosti takovým způsobem, aby pozice trvale směřovala do
    levého horního rohu obrázku. obvodového obdélníku a
    velikost odpovídá velikosti tohoto obdélníku.
    """

    def __init__(self, name="", *parts):
        """
        Vytvoří multishape s daným názvem a případně složený z
        daných objektů, které jsou předány k vytvoření.
        objekty.
        :param name: Jméno multishapu
        :param parts: tvary ktere chceme přídat
        """
        self.name = name
        self.parts = []
        self.x_pos = 0
        self.y_pos = 0
        self.height = 0
        self.width = 0
        self.bool = True
        self.creation_done = False
        self.add_shapes(parts)

    def add_shapes(self, args) -> None:
        """
        Přidá kopii daných tvarů do tohoto multishapu
         a vhodně upraví jeho vnitřní pozici a velikost.
        :param args: Tvar(y) které chceme přidat
        """
        if self.creation_done:
            raise Exception("Attempt to add a shape " +
                            "after finishing the creation " +
                            "of the mutlishape ")
        if isinstance(args, tuple):
            for s in args:
                self.add_shape(s.copy())
        elif isinstance(args, Multishape):
            for s in args.parts:
                self.add_shape(s.shape.copy())
        elif isinstance(args, Shape):
            self.add_shape(args.copy())
        else:
            raise Exception("Wrong arguments")

    def add_shape(self, shape: Shape) -> None:
        """
        Přidá zadaný tvar do multishapu a vhodně upraví jeho polohu a velikost.
        :param shape: tvar který chceme přidat
        """
        asx = shape.x
        asy = shape.y
        asw = shape.width
        ash = shape.height
        if self.bool:
            self.x_pos = asx
            self.y_pos = asy
            self.width = asw
            self.height = ash
            self.parts.append(self._Part(shape, self))
            self.bool = False
            return

        mx = self.x_pos
        my = self.y_pos
        ms = self.width
        mv = self.height
        change = False

        if asx < self.x_pos:
            self.width += self.x_pos - asx
            self.x_pos = asx
            change = True
        if asy < self.y_pos:
            self.height += self.y_pos - asy
            self.y_pos = asy
            change = True
        if (self.x_pos + self.width) < (asx + asw):
            self.width = asx + asw - self.x_pos
            change = True
        if (self.y_pos + self.height) < (asy + ash):
            self.height = asy + ash - self.y_pos
            change = True
        if change:
            for p in self.parts:
                p.after_addition(mx, my, ms, mv)
        self.parts.append(self._Part(shape, self))

    def creation_is_done(self) -> None:
        """
        Dokončí vytvoření multishape. Po zavolání této metody již
        nebude možné přidat další tvar do multishapu.
        """
        if len(self.parts) < 1:
            raise Exception("The multishape has to have at least one part")
        self.creation_done = True

    def _verify_done(self) -> None:
        """
        Ověřte, zda bylo vytvoření instance
        dokončeno pokud ne, vyhodí výjimku.
        """
        if self.creation_done:
            return
        raise Exception("Unfinished shape cannot run method")

    def set_size(self, width: int, height: int) -> None:
        """
        Nastaví nové rozměry instance.Upraví pozice a velikosti všech
        jejích částí tak, aby si multishape i přes novou velikost a
        pozici zachoval svůj vzhled. Velikost instance je
        definována jako velikost obvodového obdélníku. Nastavené
        rozměry musí být nezáporné, nulová hodnota je nahrazena
        jedničkou.
        :param width: Nová šířka instance
        :param height: Nová výška instance
        """
        self._verify_done()
        if width < 0 or height < 0:
            raise Exception("The dimensions may not be negativ: width=" +
                            str(width) + ", height=" + str(height))
        for part in self.parts:
            part.after_resizing(width, height)
            """
            width_list.append(part.partWidth)
            height_list.append(part.partHeight)
            """

        self.width = max(1, width)
        self.height = max(1, height)
        self._move_shape_on_canvas()

    def set_position(self, x: int, y: int) -> None:
        """
        Přesunutí celého multishape na zadanou pozici. Všechny části
        se přesunou najednou jako jeden objekt. Poloha instance je
        definována jako poloha levého horního rohu obvodového
        obdélníku.
        :param x: Nově nastavená vodorovná souřadnice, levý
        okraj plátna má x=0, souřadnice se zvětšuje doprava.
        :param y: Nově nastavená svislá souřadnice, horní
        okraj plátna má y=0, souřadnice se zvyšuje směrem dolů.
        """
        # self.verify_done()
        dx = x - self.x_pos
        dy = y - self.y_pos
        for part in self.parts:
            shape = part.shape
            shape.set_position(dx + shape.x, dy + shape.y)
        self.x_pos = x
        self.y_pos = y
        self._move_shape_on_canvas()

    def move_right(self, length=25):
        self.set_position(self.x_pos + length, self.y_pos)

    def move_left(self, length=25):
        self.set_position(self.x_pos - length, self.y_pos)

    def move_up(self, length=25):
        self.set_position(self.x_pos, self.y_pos - length)

    def move_down(self, length=25):
        self.set_position(self.x_pos, self.y_pos + length)

    def set_x(self, x: int):
        self.set_position(x, self.y_pos)

    def set_y(self, y: int):
        self.set_position(self.x_pos, y)

    def _create_shape_on_canvas(self) -> None:
        """
        Zavolá plátno a vytvoří tvary na plátnu.
        """
        for part in self.parts:
            if isinstance(part.part, Rectangle):
                canvas.create_rectangle(part.part.get_coord(), fill=part.part.color.tkn,
                                        tag=part.part.__repr__() + "multi", width=0)
            elif isinstance(part.part, Ellipse):
                canvas.create_oval(part.part.get_coord(), fill=part.part.color.tkn,
                                   tag=part.part.__repr__() + "multi", width=0)
            elif isinstance(part.part, Triangle):
                canvas.create_polygon(part.part.get_coord(), fill=part.part.color.tkn,
                                      tag=part.part.__repr__() + "multi")

    def _move_shape_on_canvas(self) -> None:
        """
        Pohne postupně každým tvarem v multishapu.
        """
        for part in self.parts:
            canvas.coords(part.shape.__repr__() + "multi", part.shape.get_coord())

    class _Part:
        """
        Instance třídy slouží jako schránky pro pomocné
        informace pro změnu velikosti multishape
        """

        def __init__(self, part: Shape, outer_self):
            """
            Vytvoří objekt a zapamatuje si aktuální
            podíly daného tvaru v aktuálním stavu multishape.
            :param part: zabaleny tvar
            :param outer_self: python je hloupen a nejde dostat
            atributy vnější třídy z vnitřní třídy, proto
            to musíme takhle obcházet
            """
            self.shape = part
            self.outer_self = outer_self
            self.partX = part.x
            self.partY = part.y
            part_width = part.width
            part_height = part.height
            try:
                self.dx = (self.partX - self.outer_self.x_pos) / float(self.outer_self.width)
            except ZeroDivisionError:
                self.dx = 0.0
            try:
                self.dy = (self.partY - self.outer_self.y_pos) / float(self.outer_self.height)
            except ZeroDivisionError:
                self.dy = 0.0
            try:
                self.dw = part_width / float(self.outer_self.width)
            except ZeroDivisionError:
                self.dw = 0.0
            try:
                self.dh = part_height / float(self.outer_self.height)
            except ZeroDivisionError:
                self.dh = 0.0

        def after_addition(self, ox: int, oy: int, ow: int, oh: int) -> None:
            """
            Aktualizuje uloženou relativní polohu a velikost dílu v celém
            multishape po přidání nového dílu, který způsobí změnu polohy
            a/nebo velikosti multishapu.
            :param ox: originální x
            :param oy: originální y
            :param ow: originální šířka
            :param oh: originální výška
            """
            self.dx = (ox - self.outer_self.x_pos * ow) / self.outer_self.width
            self.dy = (oy - self.outer_self.y_pos * oh) / self.outer_self.height

            self.dw = self.dw * ow / self.outer_self.width
            self.dh = self.dh * oh / self.outer_self.height

        def after_resizing(self, width: int, height: int) -> None:
            """
            Aktualizuje uložené relativní pozice a velikosti této části
            v celém multishapu po změně jeho velikosti.
            :param width: šířka celého multitvaru
            :param height: výška celého multitvaru
            """
            self.shape.set_position(int(round(self.outer_self.x_pos +
                                              self.dx * width)),
                                    int(round(self.outer_self.y_pos +
                                              self.dy * height)))
            self.shape.set_size(int(round(self.dw * width)),
                                int(round(self.dh * height)))


class Canvas(tkinter.Canvas):
    """
    Třída za kterou je prohlášen Canvas(plátno), je zároveň i kořenem.
    """

    def __init__(self, canvas_color=CREAMY, canvas_width=600, canvas_height=600
                 , pos_x=100, pos_y=100):
        tkinter.Canvas.__init__(self)
        self.master.title("Plátno")
        self.master.geometry("+%d+%d" % (pos_x, pos_y))
        self.canvas_color = canvas_color
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # pokud si neuložíte tvary tak jsou všechny v tomto atributu
        self.all_shapes = []

        self.config(bg=self.canvas_color.tkn,
                    width=self.canvas_height,
                    height=self.canvas_width)
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
        Změní barvu plátna
        :param bg_color: nová barva
        """
        self.canvas_color = bg_color
        canvas.config(bg=self.canvas_color.tkn)
        canvas.update()

    def show_canvas(self) -> None:
        """
        aktualizuje tvary na plátně
        """
        self.update()

