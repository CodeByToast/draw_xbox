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
shapes = ["classic", "turtle", "circle", "square", "triangle"]
shape_index = 0
pen.shape(shapes[shape_index])

# Colors
colors = ["black", "red", "blue", "green", "purple", "yellow"]
color_index = 0

# ----- SETTINGS -----
DEADZONE = 0.15
SPEED = 6

a_lock = False
b_lock = False
x_lock = False
y_lock = False
hat_lock = False

pen_is_down = True

# Trigger settings
lt_lock = False
fullscreen = False

rt_hold_start = None
RT_THRESHOLD = 0.5

# ----- DRAW SHAPES -----
def draw_square(size=80):
    for _ in range(4):
        pen.forward(size)
        pen.right(90)

def draw_triangle(size=80):
    for _ in range(3):
        pen.forward(size)
        pen.right(120)

def draw_hexagon(size=60):
    for _ in range(6):
        pen.forward(size)
        pen.right(60)

# ----- MAIN LOOP -----
while True:
    pygame.event.pump()

    # LEFT joystick
    lx = js.get_axis(0)
    ly = js.get_axis(1)

    # RIGHT joystick
    rx = js.get_axis(2)
    ry = js.get_axis(3)

    # Deadzone
    if abs(lx) < DEADZONE: lx = 0
    if abs(ly) < DEADZONE: ly = 0
    if abs(rx) < DEADZONE: rx = 0
    if abs(ry) < DEADZONE: ry = 0

    dx = (lx + rx) * SPEED
    dy = (ly + ry) * SPEED

    pen.goto(pen.xcor() + dx, pen.ycor() - dy)

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

    # Y → cursor skin
    y_btn = js.get_button(3)
    if y_btn and not y_lock:
        shape_index = (shape_index + 1) % len(shapes)
        pen.shape(shapes[shape_index])
        y_lock = True
    if not y_btn:
        y_lock = False

    # D-PAD (hat)
    hat = js.get_hat(0)
    if hat != (0, 0) and not hat_lock:
        if hat == (0, 1):      # Up
            pen.circle(50)
        elif hat == (1, 0):    # Right
            draw_square()
        elif hat == (-1, 0):   # Left
            draw_triangle()
        elif hat == (0, -1):   # Down
            draw_hexagon()
        hat_lock = True
    if hat == (0, 0):
        hat_lock = False

    # ----- LEFT TRIGGER (LT) → Fullscreen toggle -----
    lt = js.get_axis(4)  # usually axis 4
    if lt > 0.5 and not lt_lock:
        fullscreen = not fullscreen
        screen.setup(width=1.0, height=1.0) if fullscreen else screen.setup(width=800, height=600)
        lt_lock = True
    if lt <= 0.5:
        lt_lock = False

    # ----- RIGHT TRIGGER (RT) → Close after 3 seconds -----
    rt = js.get_axis(5)  # usually axis 5
    if rt > RT_THRESHOLD:
        if rt_hold_start is None:
            rt_hold_start = time.time()
        elif time.time() - rt_hold_start >= 3:
            turtle.bye()
            pygame.quit()
            break
    else:
        rt_hold_start = None

    time.sleep(0.01)
