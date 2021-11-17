# -*- coding: utf-8 -*-

from canvas import *

"""
e = canvas.Ellipse(50, 200, 150, 80)
r.move_up(50)
r.set_height(55)
e.move_left(100)
t = canvas.Triangle()
canvas.step = 100
t.move_right(100)
t.set_direction(canvas.NW)

r = canvas.Rectangle()
r2= r.copy()

e = canvas.Ellipse(20, 20, 50, 50)
e2 = canvas.Ellipse(70, 70, 50, 50)

t = canvas.Triangle()
t.set_size(50,200)

m = canvas.Multishape([e2, e, t])
m.set_position(100, 100)
m.set_size(10, 80)

m.set_position(300, 200)



r.move_right(200)
r.move_down()

text = canvas.Text(300,300)
text2 = text.copy()
text2.set_position(200,200)

canvas.Ellipse()

e.paint()
e.rub_out()

r.rub_out()


m.set_position(300,400)
m.set_size(50,50)
canvas.canvas.itemconfig("Rectangle4", fill="black")
canvas.canvas.move("Rectangle4",  0,50)
canvas.canvas.move("Ellipse5", 0,50)
canvas.canvas.itemconfig("Ellipse5", fill="black")

for i in canvas.canvas.find_all():
    print(canvas.canvas.gettags(i),i)
"""
canvas.change_canvas_size(300, 300)
m1 = Multishape("m1", Rectangle(), Ellipse(10,10,80,35), Triangle())
m1.creation_is_done()
m2 = Multishape("m2")
m2.add_shapes(m1)
m1.set_size(120, 30)
m1.set_position(100, 75)
m2.add_shapes(m1)
m1.set_size(20,20)
m1.set_position(150, 100)
m2.creation_is_done()
"""

canvas.change_canvas_size(500, 300)
cap = Triangle(100, 25, 50, 25, GREEN)
head = Rectangle(100, 50, 50, 50, RED)
body = Rectangle(75, 100, 100, 125, CYAN)
leftHand = Rectangle(50, 100, 25, 100, STEELY)
rightHand = Rectangle(175, 100, 25, 100, STEELY)
leftWheel = Ellipse(75, 225, 50, 50, BLACK)
rightWheel = Ellipse(125, 225, 50, 50, BLACK)

robot = Multishape("robot", cap, head,
                   body, leftHand, rightHand,
                   leftWheel, rightWheel)
robot.move_right(200)
"""
done()
