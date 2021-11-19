# -*- coding: utf-8 -*-
"""
Tohle je modul CanvasManager, jeho úkolem je vytvořit virtuální
plátno na, které jde zobrazit následující tvary:
    jednoduché obrazce:
        Rectangle,
        Elipse,
        Triangle
    složitější obrazce:
        Multishape
    a text
Tvary mohou měnit velikost, barvu a pozici.
Autor: Jan Lampa
verze: 1.2 17.11.2021
"""
import tkinter

from .Abstract_classes import *
from .Direction8 import *
from .NamedColor import *

# o kolik skáčou obrazce
canvas_step = 50


class Text(Movable, ID, Paintable, ICopyable, IRemovable):
    """
    Instance třídy Text. Vytvoří normální text na plátně.
    Text je možné:
        posouvat,
        změnit text
        okopírovat
        odstranit z plátna
    """

    def __init__(self, x=0, y=0, text="text"):
        """
        Vytvoří instanci třídy Text.
        :param x: x souřadnice, základně 0
        :param y: y souřadnice, základně 0
        :param text: text který bude vypsán, základně "text"
        """
        ID.__init__(self)
        Movable.__init__(self, x, y)
        Paintable.__init__(self)
        self.text = text

    def paint(self) -> None:
        """
        Metoda paint vytvoří tvar na plátně, pokud není vytvořen.
        Pokud je pouze aktualizuje stav tvaru na plátně podle
        atributů třídy.
        """
        if not self._is_painted_on_canvas:
            _canvas.create_text(self.x, self.y, text=self.text, tag=self.__repr__())
            self._is_painted_on_canvas = True
        else:
            _canvas.itemconfig(self.__repr__())
            _canvas.coords(self.__repr__(), self.x, self.y)
            _canvas.tag_raise(self.__repr__())
            _canvas.show_canvas()

    def copy(self):
        """
        Metoda vrátí kopii tvaru.
        :return: vracená kopie tvaru
        """
        return Text(self.x, self.y, self.text)

    def set_text(self, text):
        """
        Změní text, který je zobrazen.
        :param text: text
        """
        self.text = text
        self.paint()

    def remove(self):
        """
        Odstraní text z plátna. Nezničí ale objekt, takže je ho
        možné znovu zobrazit na plátně pomocí metody paint.
        """
        self._is_painted_on_canvas = False
        _canvas.delete(self.id)


class Shape(Resizable, ID, Paintable, ICopyable, IRemovable, ABC):
    """
    Rodičovská implementace obrazců, slouží k tomu aby
    jsme se nemusely psát metody pro některé obrazce
    několikrát.
    Také jsou zde implementována abstraktní třída, aby
    nešlo vytvořit Shape instanci.
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
        _canvas.all_shapes.append(self)
        Resizable.__init__(self, x, y, width, height)

        self.color = color
        Paintable.__init__(self)

    def rub_out(self) -> None:
        """
        Dočasně přebarví tvar na barvu pozadí.
        """
        _canvas.itemconfig(self.__repr__(), fill=_canvas.canvas_color.tkn)
        _canvas.show_canvas()

    def change_shape_color(self, color=None) -> None:
        """
        Změní barvu obrazce na tu která je uložená ve třídě,
        pokud vsak požit parametr s platnou COLOR tak na
        tuto barvu.
        """
        if color is not None:
            self.color = color
        _canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
        _canvas.show_canvas()

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
               str(self.color._name) + "]"  # noqa

    def remove(self):
        """
        Odstraní tvar z plátna.
        """
        self._is_painted_on_canvas = False
        _canvas.delete(self.id)


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
        Tato metoda zavolá plátno a pokud tvar ještě nebyl
        vytvořen tak na něm vytvoří nový, pokud již byl tak
        aktualizuje tvar na plátně podle atributů x,y,width,
        height a color.
        """
        if not self._is_painted_on_canvas:
            _canvas.create_oval(self.get_coord(), tag=self.__repr__(),
                                fill=self.color.tkn, width=0, outline="")
            self._is_painted_on_canvas = True
            _canvas.show_canvas()
        else:
            _canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            _canvas.coords(self.__repr__(), self.get_coord())
            _canvas.tag_raise(self.__repr__())
            _canvas.show_canvas()

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
        Metoda paint vytvoří tvar na plátně, pokud není vytvořen.
        Pokud je pouze aktualizuje stav tvaru na plátně podle
        atributů třídy.
        """
        if not self._is_painted_on_canvas:
            _canvas.create_rectangle(self.get_coord(), tag=self.__repr__(),
                                     fill=self.color.tkn, width=0)
            self._is_painted_on_canvas = True
            _canvas.show_canvas()
        else:
            _canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            _canvas.coords(self.__repr__(), self.get_coord())
            _canvas.tag_raise(self.__repr__())
            _canvas.show_canvas()

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
        Metoda paint vytvoří tvar na plátně, pokud není vytvořen.
        Pokud je pouze aktualizuje stav tvaru na plátně podle
        atributů třídy.
        """
        if not self._is_painted_on_canvas:
            _canvas.create_polygon(self.get_coord(), tag=self.__repr__(),
                                   fill=self.color.tkn, width=0)
            self._is_painted_on_canvas = True
            _canvas.show_canvas()
        else:
            _canvas.itemconfig(self.__repr__(), fill=self.color.tkn)
            _canvas.coords(self.__repr__(), self.get_coord())
            _canvas.tag_raise(self.__repr__())
            _canvas.show_canvas()

    def get_coord(self) -> list:
        """
        Přepočítá body tak aby jsme dostaly výstup, který můžeme
        použít na plátně.
        """
        coord = [int, int, int, int, int, int]
        match self.dir8.short_name:
            case "N":
                coord[0] = (self.corner_1[0] + self.corner_2[0]) / 2
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
            case "NE":
                coord[0] = self.corner_2[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_1[1]
            case "E":
                coord[0] = self.corner_1[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = (self.corner_1[1] + self.corner_2[1]) / 2
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
            case "SE":
                coord[0] = self.corner_2[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
            case "S":
                coord[0] = self.corner_1[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_1[1]
                coord[4] = (self.corner_1[0] + self.corner_2[0]) / 2
                coord[5] = self.corner_2[1]
            case "SW":
                coord[0] = self.corner_1[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = self.corner_2[1]
            case "W":
                coord[0] = self.corner_2[0]
                coord[1] = self.corner_1[1]
                coord[2] = self.corner_2[0]
                coord[3] = self.corner_2[1]
                coord[4] = self.corner_1[0]
                coord[5] = (self.corner_1[1] + self.corner_2[1]) / 2
            case "NW":
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


class Multishape(IMovable, IRemovable, ABC):
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
        self._name = name
        self.parts = []
        self._x_pos = 0
        self._y_pos = 0
        self._height = 0
        self._width = 0
        self._bool = True
        self._creation_done = False
        self.add_shapes(*parts)

    def add_shapes(self, *args) -> None:
        """
        Přidá kopii daných tvarů do tohoto multishapu
         a vhodně upraví jeho vnitřní pozici a velikost.
        :param args: Tvar(y) které chceme přidat
        """
        if self._creation_done:
            raise Exception("Attempt to add a shape " +
                            "after finishing the creation " +
                            "of the mutlishape ")
        list_of_shapes = self._flatten_nested_list_or_tuple(args)
        for shape in list_of_shapes:
            if isinstance(shape, Shape):
                self.add_shape(shape)
            elif isinstance(shape, Multishape):
                for s in shape.parts:
                    self.add_shape(s.shape.copy())
            else:
                raise Exception("Wrong arguments")

    @staticmethod
    def _flatten_nested_list_or_tuple(nested_list_or_tuple: tuple or list) -> list:
        """
        Metoda z vnořených listů nebo N-tic(tuple) tvarů vytvoří
        jednoduchý list tvarů.
        :param nested_list_or_tuple: list nebo N-tice
        :return: vrátí zploštělý list s tvary
        """
        flat_list = []
        for element in nested_list_or_tuple:
            if isinstance(element, list or tuple):
                flat_list.extend(Multishape._flatten_nested_list_or_tuple(element))
            elif isinstance(element, Shape or Multishape):
                flat_list.append(element)
            else:
                raise Exception("Unknown shape was attempted to be added to multishape")
        return flat_list

    def add_shape(self, shape: Shape) -> None:
        """
        Přidá zadaný tvar do multishapu a vhodně upraví jeho polohu a velikost.
        :param shape: tvar se má přidat do multishapu
        """
        asx = shape.x
        asy = shape.y
        asw = shape.width
        ash = shape.height
        if self._bool:
            self._x_pos = asx
            self._y_pos = asy
            self._width = asw
            self._height = ash
            self.parts.append(self._Part(shape, self))
            self._bool = False
            return

        mx = self._x_pos
        my = self._y_pos
        ms = self._width
        mv = self._height
        change = False

        if asx < self._x_pos:
            self._width += self._x_pos - asx
            self._x_pos = asx
            change = True
        if asy < self._y_pos:
            self._height += self._y_pos - asy
            self._y_pos = asy
            change = True
        if (self._x_pos + self._width) < (asx + asw):
            self._width = asx + asw - self._x_pos
            change = True
        if (self._y_pos + self._height) < (asy + ash):
            self._height = asy + ash - self._y_pos
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
        self._creation_done = True

    def _verify_done(self) -> None:
        """
        Ověřte, zda bylo vytvoření instance
        dokončeno pokud ne, vyhodí výjimku.
        """
        if self._creation_done:
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

        self._width = max(1, width)
        self._height = max(1, height)
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
        dx = x - self._x_pos
        dy = y - self._y_pos
        for part in self.parts:
            shape = part.shape
            shape.set_position(dx + shape.x, dy + shape.y)
        self._x_pos = x
        self._y_pos = y
        self._move_shape_on_canvas()

    def move_right(self, length=25):
        self.set_position(self._x_pos + length, self._y_pos)

    def move_left(self, length=25):
        self.set_position(self._x_pos - length, self._y_pos)

    def move_up(self, length=25):
        self.set_position(self._x_pos, self._y_pos - length)

    def move_down(self, length=25):
        self.set_position(self._x_pos, self._y_pos + length)

    def set_x(self, x: int):
        self.set_position(x, self._y_pos)

    def set_y(self, y: int):
        self.set_position(self._x_pos, y)

    def _create_shape_on_canvas(self) -> None:
        """
        Zavolá plátno a vytvoří tvary na plátnu.
        """
        for part in self.parts:
            if isinstance(part.part, Rectangle):
                _canvas.create_rectangle(part.part.get_coord(), fill=part.part.color.tkn,
                                         tag=part.part.__repr__() + "multi", width=0)
            elif isinstance(part.part, Ellipse):
                _canvas.create_oval(part.part.get_coord(), fill=part.part.color.tkn,
                                    tag=part.part.__repr__() + "multi", width=0)
            elif isinstance(part.part, Triangle):
                _canvas.create_polygon(part.part.get_coord(), fill=part.part.color.tkn,
                                       tag=part.part.__repr__() + "multi")

    def _move_shape_on_canvas(self) -> None:
        """
        Pohne postupně každým tvarem v multishapu.
        """
        for part in self.parts:
            _canvas.coords(part.shape.__repr__() + "multi", part.shape.get_coord())

    class _Part:
        """
        Instance třídy slouží jako schránky pro pomocné
        informace pro změnu velikosti multishape
        """

        def __init__(self, part: Shape, outer_self):
            """
            Vytvoří objekt a zapamatuje si aktuální
            podíly daného tvaru v aktuálním stavu multishape.
            :param part: zabalený tvar
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
                self.dx = (self.partX - self.outer_self._x_pos) / float(self.outer_self._width)  # noqa
            except ZeroDivisionError:
                self.dx = 0.0
            try:
                self.dy = (self.partY - self.outer_self._y_pos) / float(self.outer_self._height)  # noqa
            except ZeroDivisionError:
                self.dy = 0.0
            try:
                self.dw = part_width / float(self.outer_self._width)  # noqa
            except ZeroDivisionError:
                self.dw = 0.0
            try:
                self.dh = part_height / float(self.outer_self._height)  # noqa
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
            self.dx = (ox - self.outer_self._x_pos * ow) / self.outer_self._width  # noqa
            self.dy = (oy - self.outer_self._y_pos * oh) / self.outer_self._height  # noqa

            self.dw = self.dw * ow / self.outer_self._width  # noqa
            self.dh = self.dh * oh / self.outer_self._height  # noqa

        def after_resizing(self, width: int, height: int) -> None:
            """
            Aktualizuje uložené relativní pozice a velikosti této části
            v celém multishapu po změně jeho velikosti.
            :param width: šířka celého multitvaru
            :param height: výška celého multitvaru
            """
            self.shape.set_position(int(round(self.outer_self._x_pos +  # noqa
                                              self.dx * width)),
                                    int(round(self.outer_self._y_pos +  # noqa
                                              self.dy * height)))
            self.shape.set_size(int(round(self.dw * width)),
                                int(round(self.dh * height)))


class Canvas(tkinter.Canvas):
    """
    Třída za kterou je prohlášen Canvas(plátno), je zároveň i kořenem.
    Tato třída je vytvořena při importování balíčku shapes.
    """

    def __init__(self, canvas_color=CREAMY, canvas_width=600, canvas_height=600,
                 pos_x=100, pos_y=100):
        """
        Vytvoří instanci plátna.
        :param canvas_color: Barva pozadí plátna
        :param canvas_width: Šířka plátna
        :param canvas_height: Výška plátna
        :param pos_x: Pozice x kde bude okno vytvořeno
        :param pos_y: Pozice y kde bude okno vytvořeno
        """
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
        Změní barvu pozadí plátna.
        :param bg_color: nová barva
        """
        self.canvas_color = bg_color
        _canvas.config(bg=self.canvas_color.tkn)
        _canvas.update()

    def show_canvas(self) -> None:
        """
        Aktualizuje tvary na plátně.
        """
        self.update()


# Vytvoří shapes
_canvas = Canvas()


def change_canvas_size(height: int, width: int) -> None:
    """
    Změní výšku a šířku plátna
    :param height: výška
    :param width: šířka
    """
    _canvas.change_canvas_size(height, width)


def change_canvas_color(bg_color) -> None:
    """
    Změní barvu plátna
    :param bg_color: nová barva
    """
    change_canvas_color(bg_color)


def mainloop() -> None:
    """
    Tuto metodu je třeba použít na konec scriptu pokud chcete,
    aby okno zůstalo po vykonání skriptu.
    """
    _canvas.mainloop()
