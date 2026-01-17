import pygame
import turtle
import time

# ----- PYGAME SETUP -----
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected")
    quit()

js = pygame.joystick.Joystick(0)
js.init()

# ----- TURTLE SETUP -----
screen = turtle.Screen()
screen.title("Joystick Turtle Draw")

pen = turtle.Turtle()
pen.speed(0)
pen.width(3)
pen.pendown()

# Cursor skins
shapes = ["classic", "arrow", "turtle", "circle", "square", "triangle"]
shape_index = 0
pen.shape(shapes[shape_index])

# Colors
colors = ["black", "red", "blue", "green", "purple", "yellow"]
color_index = 0

# ----- SETTINGS -----
DEADZONE = 0.15
SPEED = 6

a_lock = False   # color
b_lock = False   # clear
x_lock = False   # pen up/down
y_lock = False   # cursor skin

pen_is_down = True

# ----- MAIN LOOP -----
while True:
    pygame.event.pump()

    # LEFT joystick (usually axes 0,1)
    lx = js.get_axis(0)
    ly = js.get_axis(1)

    # RIGHT joystick (usually axes 2,3)
    rx = js.get_axis(2)
    ry = js.get_axis(3)

    # Deadzone handling
    if abs(lx) < DEADZONE: lx = 0
    if abs(ly) < DEADZONE: ly = 0
    if abs(rx) < DEADZONE: rx = 0
    if abs(ry) < DEADZONE: ry = 0

    # Combine both sticks
    dx = (lx + rx) * SPEED
    dy = (ly + ry) * SPEED

    pen.goto(
        pen.xcor() + dx,
        pen.ycor() - dy
    )

    # A → change color
    a = js.get_button(0)
    if a and not a_lock:
        color_index = (color_index + 1) % len(colors)
        pen.color(colors[color_index])
        a_lock = True
    if not a:
        a_lock = False

    # X → pen up / down
    x_btn = js.get_button(2)
    if x_btn and not x_lock:
        if pen_is_down:
            pen.penup()
        else:
            pen.pendown()
        pen_is_down = not pen_is_down
        x_lock = True
    if not x_btn:
        x_lock = False

    # B → clear canvas
    b = js.get_button(1)
    if b and not b_lock:
        pen.clear()
        b_lock = True
    if not b:
        b_lock = False

    # Y → change cursor skin
    y_btn = js.get_button(3)
    if y_btn and not y_lock:
        shape_index = (shape_index + 1) % len(shapes)
        pen.shape(shapes[shape_index])
        y_lock = True
    if not y_btn:
        y_lock = False

    time.sleep(0.01)
