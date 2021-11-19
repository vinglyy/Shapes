# -*- coding: utf-8 -*-

import shapes
"""
e = shapes.Ellipse(50, 200, 150, 80)
r.move_up(50)
r.set_height(55)
e.move_left(100)
t = shapes.Triangle()
shapes.step = 100
t.move_right(100)
t.set_direction(shapes.NW)

r = shapes.Rectangle()
r2= r.copy()

e = shapes.Ellipse(20, 20, 50, 50)
e2 = shapes.Ellipse(70, 70, 50, 50)

t = shapes.Triangle()
t.set_size(50,200)

m = shapes.Multishape([e2, e, t])
m.set_position(100, 100)
m.set_size(10, 80)

m.set_position(300, 200)



r.move_right(200)
r.move_down()

text = shapes.Text(300,300)
text2 = text.copy()
text2.set_position(200,200)

shapes.Ellipse()

e.paint()
e.rub_out()

r.rub_out()


m.set_position(300,400)
m.set_size(50,50)
shapes.shapes.itemconfig("Rectangle4", fill="black")
shapes.shapes.move("Rectangle4",  0,50)
shapes.shapes.move("Ellipse5", 0,50)
shapes.shapes.itemconfig("Ellipse5", fill="black")

for i in shapes.shapes.find_all():
    print(shapes.shapes.gettags(i),i)
"""
shapes.change_canvas_size(400, 400)
m1 = shapes.Multishape("m1", shapes.Rectangle(), shapes.Ellipse(10, 10, 80, 35), shapes.Triangle())
m1.creation_is_done()
m2 = shapes.Multishape("m2")
m2.add_shapes(m1)
m1.move_down()

m2.creation_is_done()

m2.move_right(100)
m2.set_size(60,20)
m3 = shapes.Multishape("m3", m2)
m3.move_down(100)
m3.creation_is_done()
m3.set_size(20,60)
text = shapes.Text(50, 50)
text.set_text("adfadgdag")

"""

shapes.change_canvas_size(500, 300)
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
shapes.mainloop()
