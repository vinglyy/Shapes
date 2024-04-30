# Shapes

## Description
Balíček shapes určený pro výuku programování v objektově orientovaném
prostředí.
Při importu balíčku se vytvoří instanci třídy Canvas, která
implementuje Canvas z tkinter. Tato třída představuje plátno, na
které se dá kreslit tvary.
Tyto tvary se dají kreslit vytvořením instancí tvarů.

Tvary které se dají vytvořit:

### Jednoduché obrazce:
* Rectangle,
* Elipse,
* Triangle

### Složitější obrazce:
* Multishape
    
a text

### Příklad vytvoření čtverce:
```
import shapes
shapes.Rectangle(10,10,10,10,BLACK)
```

Pokud bude použita Python konzole, tak to takto stačí.
Pokud ovšem chcete tento balíček použít ve skriptu tak na konec
musíte připojit příkaz:
```
shapes.mainloop()
```
### Příklad vytvoření multishape:
```
import shapes
shapes.canvas.change_canvas_size(500, 300)
cap = shapes.Triangle(100, 25, 50, 25, shapes.GREEN)
head = shapes.Rectangle(100, 50, 50, 50, shapes.RED)
body = shapes.Rectangle(75, 100, 100, 125, shapes.CYAN)
leftHand = shapes.Rectangle(50, 100, 25, 100, shapes.STEELY)
rightHand = shapes.Rectangle(175, 100, 25, 100, shapes.STEELY)
leftWheel = shapes.Ellipse(75, 225, 50, 50, shapes.BLACK)
rightWheel = shapes.Ellipse(125, 225, 50, 50, shapes.BLACK)

robot = shapes.Multishape("robot", cap, head,
                   body, leftHand, rightHand,
                   leftWheel, rightWheel)
#You can move robot by calling move methods (move_up, move_down, move_left, move_right)
robot.move_right(200)
shapes.mainloop()
```


Autor: *Jan Lampa*

verze: *1.3 29.04.2024*