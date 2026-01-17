import pygame
import turtle
import time

# ---------- PYGAME SETUP ----------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller detected")
    quit()

js = pygame.joystick.Joystick(0)
js.init()

# ---------- TURTLE SETUP ----------
screen = turtle.Screen()
screen.title("Xbox Controller Turtle Draw")
screen.setup(800, 600)

pen = turtle.Turtle()
pen.speed(0)
pen.pendown()

# ---------- CURSOR SHAPES ----------
shapes = ["classic", "arrow", "turtle", "circle", "square", "triangle"]
shape_index = 0
pen.shape(shapes[shape_index])

# ---------- COLORS ----------
colors = ["black", "red", "blue", "green", "purple", "yellow"]
color_index = 0
pen.color(colors[color_index])

# ---------- PEN WIDTH ----------
pen_width = 3
MIN_WIDTH = 1
MAX_WIDTH = 20
pen.width(pen_width)

# ---------- SETTINGS ----------
DEADZONE = 0.15
SPEED = 6

fullscreen = False
pen_is_down = True

# ---------- LOCKS ----------
a_lock = b_lock = x_lock = y_lock = False
lb_lock = rb_lock = False
hat_lock = False
lt_lock = False

# ---------- TRIGGER EXIT ----------
rt_hold_start = None
RT_THRESHOLD = 0.5

# ---------- SHAPE FUNCTIONS ----------
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

# ---------- MAIN LOOP ----------
while True:
    pygame.event.pump()

    # ----- JOYSTICKS -----
    lx = js.get_axis(0)
    ly = js.get_axis(1)
    rx = js.get_axis(2)
    ry = js.get_axis(3)

    if abs(lx) < DEADZONE: lx = 0
    if abs(ly) < DEADZONE: ly = 0
    if abs(rx) < DEADZONE: rx = 0
    if abs(ry) < DEADZONE: ry = 0

    dx = (lx + rx) * SPEED
    dy = (ly + ry) * SPEED

    pen.goto(pen.xcor() + dx, pen.ycor() - dy)

    # ----- A: CHANGE COLOR -----
    a = js.get_button(0)
    if a and not a_lock:
        color_index = (color_index + 1) % len(colors)
        pen.color(colors[color_index])
        a_lock = True
    if not a:
        a_lock = False

    # ----- X: PEN UP / DOWN -----
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

    # ----- B: CLEAR -----
    b = js.get_button(1)
    if b and not b_lock:
        pen.clear()
        b_lock = True
    if not b:
        b_lock = False

    # ----- Y: CURSOR SHAPE -----
    y = js.get_button(3)
    if y and not y_lock:
        shape_index = (shape_index + 1) % len(shapes)
        pen.shape(shapes[shape_index])
        y_lock = True
    if not y:
        y_lock = False

    # ----- D-PAD SHAPES -----
    hat = js.get_hat(0)
    if hat != (0, 0) and not hat_lock:
        if hat == (0, 1):
            pen.circle(50)
        elif hat == (1, 0):
            draw_square()
        elif hat == (-1, 0):
            draw_triangle()
        elif hat == (0, -1):
            draw_hexagon()
        hat_lock = True
    if hat == (0, 0):
        hat_lock = False

    # ----- LB / RB: PEN WIDTH -----
    lb = js.get_button(4)
    rb = js.get_button(5)

    if lb and not lb_lock:
        pen_width = max(MIN_WIDTH, pen_width - 1)
        pen.width(pen_width)
        lb_lock = True
    if not lb:
        lb_lock = False

    if rb and not rb_lock:
        pen_width = min(MAX_WIDTH, pen_width + 1)
        pen.width(pen_width)
        rb_lock = True
    if not rb:
        rb_lock = False

    # ----- LT: FULLSCREEN TOGGLE -----
    lt = js.get_axis(4)
    if lt > 0.5 and not lt_lock:
        fullscreen = not fullscreen
        if fullscreen:
            screen.setup(width=1.0, height=1.0)
        else:
            screen.setup(800, 600)
        lt_lock = True
    if lt <= 0.5:
        lt_lock = False

    # ----- RT: HOLD 3s TO EXIT -----
    rt = js.get_axis(5)
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
