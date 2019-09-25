import tkinter as tk
from tkinter import ttk
from vpython import *
import time


### Classes and Functions ###
def sleep():
    time.sleep(0.5)


class Stopping_wall:
    def __init__(self, posn, size):
        self.posn = posn
        self.size = size
        # The box
        self.object = box(pos=self.posn, size=self.size, color=color.magenta)
        # Calculating the position of the edges to be used later to check if ball collides with wall
        self.top = posn.y + 0.5 * size.y
        self.bottom = posn.y - 0.5 * size.y
        self.right = posn.x + 0.5 * size.x
        self.left = posn.x - 0.5 * size.x
        self.front = posn.z + 0.5 * size.z
        self.back = posn.z - 0.5 * size.z

    def collide(self, ball):
        if self.left <= ball.pos.x + ball.radius and self.right >= ball.pos.x - ball.radius:
            if self.top >= ball.pos.y - ball.radius and self.bottom <= ball.pos.y + ball.radius:
                if self.front >= ball.pos.z - ball.radius and self.back <= ball.pos.z + ball.radius:
                    return False
        return True


def change_color(a, b):
    # Parameters: color, object

    if a == 'red':
        b.color = color.red
        attach_trail(b, color=color.red)
    elif a == 'orange':
        b.color = color.orange
        attach_trail(b, color=color.orange)
    elif a == 'cyan':
        b.color = color.cyan
        attach_trail(b, color=color.cyan)
    elif a == 'blue':
        b.color = color.blue
        attach_trail(b, color=color.blue)
    elif a == 'yellow':
        b.color = color.yellow
        attach_trail(b, color=color.yellow)
    elif a == 'green':
        b.color = color.green
        attach_trail(b, color=color.green)
    elif a == 'magenta':
        b.color = color.magenta
        attach_trail(b, color=color.magenta)


def display():
    current = canvas.get_selected()
    current.delete()
    scene2 = canvas(width=1400, height=600)

    def down():
        global drag, lastpos
        scene2.center = scene2.mouse.pos
        drag = True
        lastpos = vector(scene2.mouse.pos.x, scene2.mouse.pos.y, 0)

    def up():
        global drag
        drag = False

    scene2.bind("mousedown", down)
    scene2.bind("mouseup", up)


def projectile_attributes(a, b, c, d, e, f):
    # Parameters: color, speed, angle, mass, height, projectile

    change_color(a, f)
    f.speed = b  # Scalar quantity
    f.angle = c * pi / 180
    f.velocity = vector(f.speed * cos(f.angle), f.speed * sin(f.angle), 0)  # changing to a vector
    f.mass = d
    f.area = pi * f.radius ** 2
    # Creating a launch wall
    if e - f.radius > 0:
        box(pos=vector(-5, e / 2 - f.radius, 0),
            size=vector(1, e - f.radius, 1),
            color=color.white)

def set_0(a):
    # Parameter: A list of variables
    for b in a:
        b.set(0)

def Place(a, b, c):
    # Parameters: a list of (entry boxes or labels, etc.),  x and y coordinates
    for d in a:
        d.place(x=b, y=c)
        c += 20

def single_projectile(a, b, c, d, e, f, g, h, i, j):
    # Parameters: launch speed, launch height, launch angle, drag coefficient, wall height, wall distance, mass, radius, ball color, point color

    sleep()
    display()
    # Labels and variables
    v0 = a
    h0 = b
    angle = c
    left_click = label(pixel_pos=True, pos=vector(120, 550, 0), height=10, text="Left click to change the center of the screen", border=False, opacity=0)
    angle_label = label(pos=vector(-8, -1, 0), text='Launch angle here', xoffset=1, line=0, box=False, opacity=0)
    height_label = label(pos=vector(-8, -4, 0), text='Launch height here', xoffset=1, line=0, box=False, opacity=0)
    speed_label = label(pos=vector(-8, -7, 0), text='Launch speed here', xoffset=1, line=0, box=False, opacity=0)
    hdistance_label = label(pos=vector(-8, -10, 0), text='Horizontal distance travelled', xoffset=1, line=0, box=False, opacity=0)
    vdistance_label = label(pos=vector(-8, -13, 0), text='Maximum height reached', xoffset=1, line=0, box=False, opacity=0)
    time_label = label(pos=vector(-8, -16, 0), text='Time spent in air', xoffset=1, line=0, box=False, opacity=0)
    mass_label = label(pos=vector(-8, -19, 0), text='Mass of ball', xoffset=1, line=0, box=False, opacity=0)
    radius_label = label(pos=vector(-8, -22, 0), text='Radius of ball', xoffset=1, line=0, box=False, opacity=0)
    drag_label = label(pos=vector(-8, -25, 0), text='Drag coefficient of ball.', xoffset=1, line=0, box=False, opacity=0)
    horizontal_velocity_arrow = arrow(pos=vector(-5, h0, 0), axis=vector(0, 0, 0))
    vertical_velocity_arrow = arrow(pos=vector(-5, h0, 0), axis=vector(0, 0, 0))
    vdistance = 0

    # Wall
    if e != 0:
        wall = Stopping_wall(posn=vector(f - 5, e / 2, 0), size=vector(0.05, e, 2))

    ball = sphere(pos=vector(-5, h0, 0), radius=h)
    gravity = -9.81
    drag_coeff = d
    air_density = 1.225
    projectile_attributes(i, v0, angle, g, h0, ball)

    # Updating labels
    angle_label.text = 'Angle of launch = ' + str(angle) + ' degrees'
    speed_label.text = 'Speed of launch = ' + str(ball.speed) + ' m/s'
    height_label.text = 'Height of launch = ' + str(h0) + ' m'
    mass_label.text = 'Mass of ball = ' + str(ball.mass) + ' kg'
    radius_label.text = 'Radius of ball = ' + str(ball.radius) + ' m'

    # Initial floor
    dx = 1  # distance between the center of two rulers
    floor_x = ball.pos.x + 0.5 * dx  # this is the x coordinate of the first floor so that the ball/projectile sits on the left edge
    floor_x_max = -floor_x
    while floor_x <= floor_x_max:
        ruler = box(pos=vector(floor_x, -0.1, 0),
                    size=vector(0.95 * dx, 0.1, 2),
                    color=color.white,
                    opacity=0.5)
        floor_x += dx

    # Animation loop

    dt = 0.001  # Time increment
    time = 0

    # Variables needed to determine the position of side labels
    c = 1  # counter for reference points
    xlabel = -40 # coordinates for the first side label
    ylabel = 15

    keep_going = True
    while (keep_going):
        # Checks if the ball is inside the wall
        if e != 0:
            keep_going = wall.collide(ball)
        # If ball reached the floor
        if ball.pos.y < 0:
            keep_going = False
        rate(500)
        g_force = vector(0, ball.mass * gravity, 0)  # Gravitational force
        drag_force = 0.5 * air_density * drag_coeff * (ball.area) * mag(ball.velocity) * ball.velocity * -1  # Drag force in opposite directions
        # Resultant force
        force = g_force + drag_force
        # Update velocity
        ball.velocity = ball.velocity + (force / ball.mass) * dt
        # Update position
        ball.pos = ball.pos + ball.velocity * dt
        # Update time
        time = time + dt

        time1 = round(time, 3)  # rounds the current time to 3 decimal places
        time_list = [t for t in range(0, 1000)]  # list of integer time intervals

        for t in time_list:
            if time1 == t:
                point = sphere(pos=vector(ball.pos.x, ball.pos.y, 0), radius=0.2)
                change_color(j, point)
                sphereNumber_label = label(height=10, pos=vector(ball.pos.x + 1, ball.pos.y + 1, 0),
                                     text=str(c), xoffset=1, line=0, box=False, opacity=0)
                number_label = label(pos=vector(xlabel, ylabel, 0), height=20, text=str(c),
                                           xoffset=1, line=0, box=False, opacity=0)
                hdtravelled_label = label(height=10, pos=vector(xlabel, ylabel - 2, 0),
                                          text='Horizontal distance travelled = ' + str(round(ball.pos.x + 5, 2)) + ' m',
                                          xoffset=1, line=0, box=False, opacity=0)
                dtravelled_label = label(height=10, pos=vector(xlabel, ylabel - 4, 0),
                                         text='Vertical distance travelled = ' + str(round(ball.pos.y, 2)) + ' m',
                                         xoffset=1, line=0, box=False, opacity=0)
                instantaneousSpeed_label = label(height=10, pos=vector(xlabel, ylabel - 6, 0),
                                                 text='Speed of ball = ' + str(round(mag(ball.velocity), 2)) + ' m/s',
                                                 xoffset=1, line=0, box=False, opacity=0)
                ylabel -= 10
                c += 1

        # Update arrows
        # The vector arrows are positioned using the ball's current position
        # The size of the arrows is proportional to the size of the forces acting on the ball
        horizontal_velocity_arrow.pos = vector(ball.pos.x, ball.pos.y, 0)
        horizontal_velocity_arrow.axis = vector(ball.velocity.x / 7, 0, 0)
        vertical_velocity_arrow.pos = vector(ball.pos.x, ball.pos.y, 0)
        vertical_velocity_arrow.axis = vector(0, ball.velocity.y / 3, 0)

        # Update distance and time labels
        # Rounding to avoid bombarding the user with a plethora of decimal places
        hdistance = round((ball.pos.x + 5), 2)
        hdistance_label.text = "Horizontal distance travelled = " + str(hdistance) + ' m'
        if ball.pos.y >= vdistance:
            vdistance = round(ball.pos.y, 2)
        vdistance_label.text = "Maximum height reached = " + str(vdistance) + ' m'
        time_label.text = "Time spent in air = " + str(round(time, 2)) + ' s'

        # Add as many rulers as necessary
        if ball.pos.x > floor_x_max:
            floor_x_max += dx
            box(pos=vector(floor_x_max, -0.1, 0),
                size=vector(0.95 * dx, 0.1, 2),
                color=color.white,
                opacity=0.5)
            
    horizontal_velocity_arrow.visible = False
    vertical_velocity_arrow.visible = False


def angle_loop(a, b, c, d, e, f, g, h, i, j, k):
    # Parameters: launch speed, launch height, min angle, angle increment, max angle, drag coefficient, wall height, wall distance, mass, radius, color

    sleep()
    display()

    # Labels and variables
    v0 = a
    h0 = b
    angle = c
    dangle = d
    angle_max = e
    left_click = label(pixel_pos=True, pos=vector(100, 520, 0), text="Left click to change the center of the screen", height=10, border=False, opacity=0)
    angle_label = label(pos=vector(-8, -1, 0), text='Launch angle here.', xoffset=1, line=0, box=False, opacity=0)
    height_label = label(pos=vector(-8, -4, 0), text='Launch height here.', xoffset=1, line=0, box=False, opacity=0)
    speed_label = label(pos=vector(-8, -7, 0), text='Launch speed here.', xoffset=1, line=0, box=False, opacity=0)
    hdistance_label = label(pos=vector(-8, -10, 0), text='Horizontal distance travelled.', xoffset=1, line=0, box=False,opacity=0)
    vdistance_label = label(pos=vector(-8, -13, 0), text='Maximum height reached.', xoffset=1, line=0, box=False, opacity=0)
    time_label = label(pos=vector(-8, -16, 0), text='Time spent in air.', xoffset=1, line=0, box=False, opacity=0)
    mass_label = label(pos=vector(-8, -19, 0), text='Mass of ball.', xoffset=1, line=0, box=False, opacity=0)
    radius_label = label(pos=vector(-8, -22, 0), text='Radius of ball.', xoffset=1, line=0, box=False, opacity=0)
    drag_label = label(pos=vector(-8, -25, 0), text='Drag coefficient of ball.', xoffset=1, line=0, box=False, opacity=0)
    horizontal_velocity_arrow = arrow(pos=vector(-5, h0, 0), axis=vector(0, 0, 0))
    vertical_velocity_arrow = arrow(pos=vector(-5, h0, 0), axis=vector(0, 0, 0), length=1)
    vdistance = 0

    # Wall
    if g != 0:
        wall = Stopping_wall(posn=vector(h - 5, g / 2, 0), size=vector(0.05, g, 2))

    ## Projectile
    while angle <= angle_max:
        ball = sphere(pos=vector(-5, h0, 0), radius=j)
        gravity = -9.81
        drag_coeff = f
        air_density = 1.225
        projectile_attributes(k, v0, angle, i, h0, ball)
        time = 0
        dt = 0.001
        # Updating labels
        angle_label.text = 'Angle of launch = ' + str(angle) + ' degrees'
        speed_label.text = 'Speed of launch = ' + str(ball.speed) + ' m/s'
        height_label.text = 'Height of launch = ' + str(h0) + ' m'
        mass_label.text = 'Mass of ball = ' + str(ball.mass) + ' kg'
        radius_label.text = 'Radius of ball = ' + str(ball.radius) + ' m'
        drag_label.text = 'Drag coefficient of ball = ' + str(drag_coeff)

        # To make an automated floor
        dx = 1
        ruler_x = ball.pos.x + 0.5 * dx
        ruler_x_max = -ruler_x
        while ruler_x <= ruler_x_max:
            ruler = box(pos=vector(ruler_x, -0.1, 0),
                        size=vector(0.95 * dx, 0.1, 2),
                        color=color.white,
                        opacity=0.5)
            ruler_x += dx

        # Animation loop
        keep_going = True
        while keep_going:
            if g != 0:
                keep_going = wall.collide(ball)
            if ball.pos.y < 0:
                keep_going = False

            rate(500)
            # Forces
            g_force = vector(0, ball.mass * gravity, 0)  # Gravitational force
            drag_force = 0.5 * air_density * drag_coeff * (ball.area) * mag(ball.velocity) * ball.velocity * -1
            force = g_force + drag_force
            # Update velocity
            ball.velocity = ball.velocity + force / ball.mass * dt
            # Update position
            ball.pos = ball.pos + ball.velocity * dt
            # Update time
            time = time + dt

            # Update arrows
            horizontal_velocity_arrow.pos = vector(ball.pos.x, ball.pos.y, 0)
            horizontal_velocity_arrow.axis = vector(ball.velocity.x / 7, 0, 0)
            vertical_velocity_arrow.pos = vector(ball.pos.x, ball.pos.y, 0)
            vertical_velocity_arrow.axis = vector(0, ball.velocity.y / 3, 0)
            # Update distance labels
            hdistance = round(ball.pos.x + 5, 2)
            hdistance_label.text = "Horizontal distance travelled = " + str(hdistance) + ' m'
            if vdistance <= ball.pos.y:
                vdistance = round(ball.pos.y, 2)
            vdistance_label.text = "Maximum height reached = " + str(vdistance) + ' m'
            time_label.text = "Time spent in air = " + str(round(time, 2)) + ' s'

            # More rulers
            if ball.pos.x > ruler_x_max:
                ruler_x_max += dx
                ruler = box(pos=vector(ruler_x_max, -0.1, 0), size=vector(0.95 * dx, 0.1, 2), color=color.white, opacity=0.5)
        angle += dangle
    horizontal_velocity_arrow.visible = False
    vertical_velocity_arrow.visible = False


def drag_loop(a, b, c, d, e, f, g, h, i, j, k):
    # Parameters: launch speed, launch height, min drag, drag increment, max drag, angle, wall height, wall distance, mass, radius, color

    sleep()
    display() # Function that allows the same canvas to be reused and allows the user to adjust the centre of the screen

    # Labels and variables
    v0 = a
    h0 = b
    dragMin = c
    dragDelta = d
    dragMax = e
    angle = f
    left_click = label(pixel_pos=True, pos=vector(100, 520, 0), text="Left click to change the center of the screen", height=10, border=False, opacity=0)
    angle_label = label(pos=vector(-8, -4, 0), text='Launch angle here.', xoffset=1, line=0, box=False, opacity=0)
    height_label = label(pos=vector(-8, -7, 0), text='Launch height here.', xoffset=1, line=0, box=False, opacity=0)
    speed_label = label(pos=vector(-8, -10, 0), text='Launch speed here.', xoffset=1, line=0, box=False, opacity=0)
    hdistance_label = label(pos=vector(-8, -13, 0), text='Horizontal distance travelled.', xoffset=1, line=0, box=False, opacity=0)
    vdistance_label = label(pos=vector(-8, -16, 0), text='Maximum height reached.', xoffset=1, line=0, box=False, opacity=0)
    time_label = label(pos=vector(-8, -19, 0), text='Time spent in air.', xoffset=1, line=0, box=False, opacity=0)
    mass_label = label(pos=vector(-8, -22, 0), text='Mass of ball.', xoffset=1, line=0, box=False, opacity=0)
    radius_label = label(pos=vector(-8, -25, 0), text='Radius of ball.', xoffset=1, line=0, box=False, opacity=0)
    drag_label = label(pos=vector(-8, -28, 0), text='Drag coefficient of ball.', xoffset=1, line=0, box=False, opacity=0)
    horizontal_velocity_arrow = arrow(pos=vector(-5, h0, 0), axis=vector(0, 0, 0))
    vertical_velocity_arrow = arrow(pos=vector(-5, h0, 0), axis=vector(0, 0, 0), length=1)
    vdistance = 0

    # Wall
    if g != 0:
        wall = Stopping_wall(posn=vector(h - 5, g / 2, 0), size=vector(0.05, g, 2))


    xlabel = -40  # Coordinates for the first side label
    ylabel = 15
    c = 1 # First number label

    ##Projectile
    while dragMin <= dragMax:
        ball = sphere(pos=vector(-5, h0, 0), radius=j)
        gravity = -9.81
        air_density = 1.225
        projectile_attributes(k, v0, angle, i, h0, ball)
        time = 0
        dt = 0.001
        # Updating labels
        angle_label.text = 'Angle of launch = ' + str(angle) + ' degrees'
        speed_label.text = 'Speed of launch = ' + str(ball.speed) + ' m/s'
        height_label.text = 'Height of launch = ' + str(h0) + ' m'
        mass_label.text = 'Mass of ball = ' + str(ball.mass) + ' kg'
        radius_label.text = 'Radius of ball = ' + str(ball.radius) + ' m'
        drag_label.text = 'Drag coefficient of ball = ' + str(dragMin)
        # To make an automated floor
        dx = 1
        ruler_x = ball.pos.x + 0.5 * dx
        ruler_x_max = -ruler_x
        while ruler_x <= ruler_x_max:
            ruler = box(pos=vector(ruler_x, -0.1, 0),
                        size=vector(0.95 * dx, 0.1, 2),
                        color=color.white,
                        opacity=0.5)
            ruler_x += dx

        # Animation loop
        keep_going = True
        while keep_going:
            if g != 0:
                keep_going = wall.collide(ball)
            if ball.pos.y < 0:
                keep_going = False
                sphereNumber_label = label(height=10, pos=vector(ball.pos.x , ball.pos.y - 2, 0),
                                     text=str(c), xoffset=1, line=0, box=False, opacity=0)
                number_label = label(pos=vector(xlabel, ylabel, 0), height=20, text=str(c),
                                           xoffset=1, line=0, box=False, opacity=0)
                hdtravelled_label = label(height=10, pos=vector(xlabel, ylabel - 2, 0),
                                          text='Horizontal distance travelled = ' + str(round(ball.pos.x + 5, 2)) + ' m',
                                          xoffset=1, line=0, box=False, opacity=0)
                dtravelled_label = label(height=10, pos=vector(xlabel, ylabel - 4, 0),
                                         text='Vertical distance travelled = ' + str(round(vdistance, 2)) + ' m',
                                         xoffset=1, line=0, box=False, opacity=0)
                instantaneousSpeed_label = label(height=10, pos=vector(xlabel, ylabel - 6, 0),
                                                 text='Speed of ball = ' + str(round(mag(ball.velocity), 2)) + ' m/s',
                                                 xoffset=1, line=0, box=False, opacity=0)
                dragCoefficient_label = label(height=10, pos=vector(xlabel, ylabel - 8, 0),
                                              text='Drag coefficient of ball = ' + str(dragMin),
                                              xoffset=1, line=0, box=False, opacity=0)
                ylabel -= 12
                c += 1

            rate(500)
            # Forces
            g_force = vector(0, ball.mass * gravity, 0)  # Gravitational force
            drag_force = 0.5 * air_density * dragMin * (ball.area) * mag(ball.velocity) * ball.velocity * -1
            force = g_force + drag_force
            # Update velocity
            ball.velocity = ball.velocity + force / ball.mass * dt
            # Update position
            ball.pos = ball.pos + ball.velocity * dt
            # Update time
            time = time + dt
            # Update arrows
            horizontal_velocity_arrow.pos = vector(ball.pos.x, ball.pos.y, 0)
            horizontal_velocity_arrow.axis = vector(ball.velocity.x / 7, 0, 0)
            vertical_velocity_arrow.pos = vector(ball.pos.x, ball.pos.y, 0)
            vertical_velocity_arrow.axis = vector(0, ball.velocity.y / 3, 0)
            # Update distance labels
            hdistance = round(ball.pos.x + 5, 2)
            hdistance_label.text = "Horizontal distance travelled = " + str(hdistance) + ' m'
            if vdistance <= ball.pos.y:
                vdistance = round(ball.pos.y, 2)
            vdistance_label.text = "Maximum height reached = " + str(vdistance) + ' m'
            time_label.text = "Time spent in air = " + str(round(time, 2)) + ' s'

            # More rulers
            if ball.pos.x > ruler_x_max:
                ruler_x_max += dx
                ruler = box(pos=vector(ruler_x_max, -0.1, 0), size=vector(0.95 * dx, 0.1, 2), color=color.white, opacity=0.5)

        dragMin += dragDelta
    horizontal_velocity_arrow.visible = False
    vertical_velocity_arrow.visible = False


### GUI ###
font = ('Verdana', 12)


# This is the window of the application. It inherits attributes from the window widget present in tkinter.
# It also acts as the controller of the application
class Foundation(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('400x400+0+0')  # Size of the window
        self.resizable(False, False)  # Size cannot be changed
        tk.Tk.wm_title(self, 'Projectile Motion Simulation')

        container = tk.Frame(self)  # Creates a frame widget that acts as a bag which is contains the frames of the GUI. The frame is placed inside the window
        # Placing the widget as the top most layer
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary which contains shared data between the pages
        self.app_data = {'mass': 1.0,
                         'radius': 0.5,
                         'ball color': 'red',
                         'point color': 'red'}

        self.frames = {}  # Dictionary that will contain the frames
        for F in (main_menu, settings_page, choose_simulation, user_manual, sp_page, angle_page, drag_page):
            frame = F(container, self)  # The foundational code acts as the controller between each page; it has the funtions that is shared between all the pages.
            # Each instant is put into the container frame
            self.frames[F] = frame  # Then save them to a dictionary
            frame.grid(row=0, column=0, sticky='nsew')  # By putting the pages in the same row and column, the pages are stacked on top of each other.
        self.show_frame(main_menu)

    # Show a frame for the given page name
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class main_menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller  # This is an instant of the foundational code

        # Title
        L1 = tk.Label(self, text='Projectile Motion Simulation', font=font)
        L1.pack(pady=10, padx=10)

        # Choose Simulation Frame Button
        B1 = ttk.Button(self, width=18, text='Choose Simulation',
                        command=lambda: controller.show_frame(choose_simulation))
        B1.pack()

        # Settings Frame Button
        B2 = ttk.Button(self, width=18, text='Settings', command=lambda: controller.show_frame(settings_page))
        B2.pack()

        # User Manual Frame Button
        B3 = ttk.Button(self, width=18, text='User Manual', command=lambda: controller.show_frame(user_manual))
        B3.pack()

        # Image
        ball_image = tk.PhotoImage(file='ball_pic.gif')
        L2 = tk.Label(self, image=ball_image)
        L2.image = ball_image
        L2.pack()


class choose_simulation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Title
        L1 = tk.Label(self, text='Choose Simulation', font=font)
        L1.pack(pady=10, padx=10)

        # Single Projectile Frame Button
        B_sp = ttk.Button(self, width=17, text='Single Projectile', command=lambda: controller.show_frame(sp_page))
        B_sp.pack()

        # Angle Loop Frame Button
        B_angleLoop = ttk.Button(self, width=17, text='Angle loop', command=lambda: controller.show_frame(angle_page))
        B_angleLoop.pack()

        # Drag Loop Frame Button
        B_dragLoop = ttk.Button(self, width=17, text='Drag loop', command=lambda: controller.show_frame(drag_page))
        B_dragLoop.pack()

        # Home Frame Button
        B_home = ttk.Button(self, width=17, text='Home', command=lambda: controller.show_frame(main_menu))
        B_home.pack()


class settings_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Title
        L_title = tk.Label(self, text='Settings', font=font)
        L_title.pack(pady=10, padx=10)

        B_choose_simulation = ttk.Button(self, width=17, text='Choose Simulation',
                                         command=lambda: controller.show_frame(choose_simulation))
        B_choose_simulation.pack()

        B_home = ttk.Button(self, width=17, text='Home', command=lambda: controller.show_frame(main_menu))
        B_home.pack()

        # Mass of ball: labels, variable and entry
        L_mass = tk.Label(self, text='Mass of ball')
        L_mass.place(x=10, y=100)
        L_m_units = tk.Label(self, text='kg')
        L_m_units.place(x=165, y=100)
        v_mass = tk.StringVar()
        v_mass.set(1)
        EB_mass = tk.Entry(self, textvariable=v_mass, width=10)
        EB_mass.place(x=100, y=102.5)

        ## Colors
        color_options = ['red', 'red', 'green', 'orange', 'yellow', 'blue', 'cyan', 'magenta']

        # Color of ball: labels, variables and drop-down menu
        L_ball_color = tk.Label(self, text='Choose ball color')
        L_ball_color.place(x=10, y=130)
        ball_color = tk.StringVar()
        ball_color.set(color_options[0])
        ball_color_menu = ttk.OptionMenu(self, ball_color, *color_options)
        ball_color_menu.place(x=110, y=130)

        # Color of reference point: labels, variables and drop-down menu
        L_point_color = tk.Label(self, text='Choose point color')
        L_point_color.place(x=10, y=190)
        point_color = tk.StringVar()
        point_color_menu = ttk.OptionMenu(self, point_color, *color_options)
        point_color.set(color_options[0])
        point_color_menu.place(x=120, y=190)

        # Radius of ball: labels, variable and entry
        L_radius = tk.Label(self, text='Enter ball radius')
        L_radius.place(x=10, y=160)
        L_r_units = tk.Label(self, text='m')
        L_r_units.place(x=165, y=160)
        v_radius = tk.StringVar()
        v_radius.set(0.5)
        EB_radius = tk.Entry(self, textvariable=v_radius, width=10)
        EB_radius.place(x=100, y=162.5)

        # Changing information stored in the dictionary of the Foundation class
        def change():
            self.controller.app_data['mass'] = eval(v_mass.get())
            self.controller.app_data['radius'] = eval(v_radius.get())
            self.controller.app_data['ball color'] = str(ball_color.get())
            self.controller.app_data['point color'] = str(point_color.get())

        # Change button binded to the change function
        B_change = ttk.Button(self, text='Change', width=10, command=change)
        B_change.place(x=200, y=220)


class sp_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Title
        L_title = tk.Label(self, text='Single Projectile', font=font)
        L_title.pack(pady=10, padx=10)

        ## Entries, values and labels for the parameters of the single projectile function

        # Labels
        L_velocity = ttk.Label(self, text='Enter launch velocity: ').place(x=10, y=100)
        L_velocity_units = ttk.Label(self, text='m/s').place(x=220, y=100)
        L_height = ttk.Label(self, text='Enter launch height: ').place(x=10, y=120)
        L_height_units = ttk.Label(self, text='m').place(x=220, y=120)
        L_theta = ttk.Label(self, text='Enter launch angle: ').place(x=10, y=140)
        L_theta_units = ttk.Label(self, text='degrees').place(x=220, y=140)
        L_drag = ttk.Label(self, text='Enter drag coefficient: ').place(x=10, y=160)
        L_wall_height = ttk.Label(self, text='Enter wall height: ')
        L_wall_distance = ttk.Label(self, text='Enter distance between ball and object: ')
        L_wall_units1 = ttk.Label(self, text='m')
        L_wall_units2 = ttk.Label(self, text='m')

        # Value variables
        v_value = tk.StringVar()
        h_value = tk.StringVar()
        theta_value = tk.StringVar()
        drag_value = tk.StringVar()
        wall_height = tk.StringVar()
        wall_distance = tk.StringVar()
        list_of_variables = [v_value, h_value, theta_value, drag_value, wall_height, wall_distance]
        set_0(list_of_variables)

        # Value Entry boxes
        EB_velocity = tk.Entry(self, textvariable=v_value, width=10)
        EB_velocity.place(x=150, y=102.5)
        EB_height = tk.Entry(self, textvariable=h_value, width=10)
        EB_height.place(x=150, y=122.5)
        EB_theta = tk.Entry(self, textvariable=theta_value, width=10)
        EB_theta.place(x=150, y=142.5)
        EB_drag = tk.Entry(self, textvariable=drag_value, width=10)
        EB_drag.place(x=150, y=162.5)
        EB_wall_height = tk.Entry(self, textvariable=wall_height, width=10)
        EB_wall_distance = tk.Entry(self, textvariable=wall_distance, width=10)

        # Binding the single projectile function to the 'run' button
        B_run = ttk.Button(self, width=15, text='Run',
                           command=lambda: single_projectile(eval(v_value.get()), eval(h_value.get()),
                                                             eval(theta_value.get()),
                                                             eval(drag_value.get()), 0, 0,
                                                             self.controller.app_data['mass'],
                                                             self.controller.app_data['radius'],
                                                             self.controller.app_data['ball color'],
                                                             self.controller.app_data['point color']))
        B_run.place(x=280, y=250)

        # Function that checks the value of the checkbox and creates buttons that correspond to its value
        def check_value():
            B_run.place_forget()

            if var.get() == 1:  # A value of 1 means that the check box is checked, thus a wall is wanted
                L_wall_height.place(x=10, y=200)
                L_wall_distance.place(x=10, y=220)
                EB_wall_height.place(x=150, y=202.5)
                EB_wall_distance.place(x=220, y=222.5)
                L_wall_units1.place(x=220, y=200)
                L_wall_units2.place(x=290, y=220)

                B_run_wall = ttk.Button(self, width=15, text='Run',
                                        command=lambda: single_projectile(eval(v_value.get()), eval(h_value.get()),
                                                                          eval(theta_value.get()),
                                                                          eval(drag_value.get()),
                                                                          eval(wall_height.get()),
                                                                          eval(wall_distance.get()),
                                                                          self.controller.app_data['mass'],
                                                                          self.controller.app_data['radius'],
                                                                          self.controller.app_data['ball color'],
                                                                          self.controller.app_data['point color']))
                B_run_wall.place(x=280, y=250)

            else:
                L_wall_height.place_forget()
                L_wall_distance.place_forget()
                EB_wall_height.place_forget()
                EB_wall_distance.place_forget()
                L_wall_units1.place_forget()
                L_wall_units2.place_forget()

                B_run_no_wall = ttk.Button(self, width=15, text='Run',
                                           command=lambda: single_projectile(eval(v_value.get()), eval(h_value.get()),
                                                                             eval(theta_value.get()),
                                                                             eval(drag_value.get()), 0, 0,
                                                                             self.controller.app_data['mass'],
                                                                             self.controller.app_data['radius'],
                                                                             self.controller.app_data['ball color'],
                                                                             self.controller.app_data['point color']))
                B_run_no_wall.place(x=280, y=250)

        var = tk.IntVar()  # variable linked to the checkbox
        C1 = tk.Checkbutton(self, text='Create a wall', command=check_value, variable=var)
        C1.place(x=10, y=180)

        ## Buttons
        B_settings = ttk.Button(self, width=15, text='Settings', command=lambda: controller.show_frame(settings_page))
        B_settings.pack()
        B_home = ttk.Button(self, width=15, text='Home', command=lambda: controller.show_frame(main_menu))
        B_home.pack()


class angle_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        L_title = tk.Label(self, text='Angle loop', font=font)
        L_title.pack(pady=10, padx=10)

        ## Entries and labels
        L_velocity = ttk.Label(self, text='Enter launch velocity: ')
        L_height = ttk.Label(self, text='Enter launch height: ')
        L_mintheta = ttk.Label(self, text='Enter minimum launch angle: ')
        L_maxtheta = ttk.Label(self, text='Enter maximum launch angle: ')
        L_dtheta = ttk.Label(self, text='Enter delta angle: ')
        L_drag = ttk.Label(self, text='Enter drag coefficient: ')
        list_of_labels = [L_velocity, L_height, L_mintheta, L_dtheta, L_maxtheta, L_drag]
        Place(list_of_labels, 10, 100)
        L_wall_height = ttk.Label(self, text='Enter wall height: ')
        L_wall_distance = ttk.Label(self, text='Enter distance between ball and object: ')
        L_velocity_units = ttk.Label(self, text='m/s').place(x=270, y=100)
        L_height_units = ttk.Label(self, text='m').place(x=270, y=120)

        # Loop for angle units. The Place function cannot be used because the SAME object is being placed multiple times.
        y = 140
        for x in range(3):
            ttk.Label(self, text='degrees').place(x=270, y=y)
            y += 20

        # Labels that are initially not placed
        L_wall_units1 = ttk.Label(self, text='m')
        L_wall_units2 = ttk.Label(self, text='m')

        # Value variables
        v_value = tk.StringVar()
        h_value = tk.StringVar()
        mintheta_value = tk.StringVar()
        drag_value = tk.StringVar()
        maxtheta_value = tk.StringVar()
        dtheta_value = tk.StringVar()
        wall_height = tk.StringVar()
        wall_distance = tk.StringVar()
        list_of_variables = [v_value, h_value, mintheta_value, dtheta_value, maxtheta_value, drag_value, wall_height, wall_distance]
        set_0(list_of_variables)

        # Value Entry boxes
        EB_velocity = tk.Entry(self, textvariable=v_value, width=10)
        EB_height = tk.Entry(self, textvariable=h_value, width=10)
        EB_mintheta = tk.Entry(self, textvariable=mintheta_value, width=10)
        EB_drag = tk.Entry(self, textvariable=drag_value, width=10)
        EB_maxtheta = tk.Entry(self, textvariable=maxtheta_value, width=10)
        EB_dtheta = tk.Entry(self, textvariable=dtheta_value, width=10)
        list_of_entries = [EB_velocity, EB_height, EB_mintheta, EB_dtheta, EB_maxtheta, EB_drag]
        Place(list_of_entries, 200, 102.5)
        EB_wall_height = tk.Entry(self, textvariable=wall_height, width=10)
        EB_wall_distance = tk.Entry(self, textvariable=wall_distance, width=10)

        B_run = ttk.Button(self, width=15, text='Run', command=lambda: angle_loop(eval(v_value.get()), eval(h_value.get()), eval(mintheta_value.get()),
                                                                                  eval(dtheta_value.get()), eval(maxtheta_value.get()), eval(drag_value.get()), 0, 0,
                                                                                  self.controller.app_data['mass'], self.controller.app_data['radius'],
                                                                                  self.controller.app_data['ball color']))
        B_run.place(x=240, y=290)

        # Checkbox
        def check_value():
            B_run.place_forget()
            if var.get():
                L_wall_height.place(x=10, y=240)
                L_wall_distance.place(x=10, y=260)
                EB_wall_height.place(x=120, y=242.5)
                EB_wall_distance.place(x=220, y=262.5)
                L_wall_units1.place(x=190, y=240)
                L_wall_units2.place(x=285, y=260)

                B_run1 = ttk.Button(self, width=15, text='Run', command=lambda: angle_loop(eval(v_value.get()), eval(h_value.get()), eval(mintheta_value.get()),
                                                                                           eval(dtheta_value.get()), eval(maxtheta_value.get()), eval(drag_value.get()),
                                                                                           eval(wall_height.get()), eval(wall_distance.get()),
                                                                                           self.controller.app_data['mass'], self.controller.app_data['radius'],
                                                                                           self.controller.app_data['ball color']))
                B_run1.place(x=240, y=290)

            else:
                L_wall_height.place_forget()
                L_wall_distance.place_forget()
                EB_wall_height.place_forget()
                EB_wall_distance.place_forget()
                L_wall_units1.place_forget()
                L_wall_units2.place_forget()

                B_run2 = ttk.Button(self, width=15, text='Run', command=lambda: angle_loop(eval(v_value.get()), eval(h_value.get()), eval(mintheta_value.get()),
                                                                                           eval(dtheta_value.get()), eval(maxtheta_value.get()), eval(drag_value.get()), 0, 0,
                                                                                           self.controller.app_data['mass'], self.controller.app_data['radius'],
                                                                                           self.controller.app_data['ball color']))
                B_run2.place(x=240, y=290)

        var = tk.IntVar()
        C1 = tk.Checkbutton(self, text='Create a wall', command=check_value, variable=var)
        C1.place(x=10, y=220)

        ##Buttons
        B_settings = ttk.Button(self, width=15, text='Settings', command=lambda: controller.show_frame(settings_page))
        B_settings.pack()
        B_home = ttk.Button(self, width=15, text='Home', command=lambda: controller.show_frame(main_menu))
        B_home.pack()


class drag_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        L_title = tk.Label(self, text='Drag loop', font=font)
        L_title.pack(pady=10, padx=10)

        ## Entries and labels
        # To the left of the entry boxes
        L_velocity = ttk.Label(self, text='Enter launch velocity: ')
        L_height = ttk.Label(self, text='Enter launch height: ')
        L_angle = ttk.Label(self, text='Enter launch angle: ')
        L_dragMin = ttk.Label(self, text='Enter minimum drag coefficient: ')
        L_dragDelta = ttk.Label(self, text='Enter delta drag coefficient: ')
        L_dragMax = ttk.Label(self, text='Enter maximum drag coefficient: ')
        list_of_labels = [L_velocity, L_height, L_angle, L_dragMin, L_dragDelta, L_dragMax]
        Place(list_of_labels, 10, 100)

        # To the right of the entry boxes
        L_wall_height = ttk.Label(self, text='Enter wall height: ')
        L_wall_distance = ttk.Label(self, text='Enter distance between ball and object: ')
        L_velocity_units = ttk.Label(self, text='m/s')
        L_height_units = ttk.Label(self, text='m')
        L_angle_units = ttk.Label(self, text='degrees')
        list_of_units = [L_velocity_units, L_height_units, L_angle_units]
        Place(list_of_units, 270, 100)
        L_wall_units1 = ttk.Label(self, text='m')
        L_wall_units2 = ttk.Label(self, text='m')

        # Value variables
        v_value = tk.StringVar()
        h_value = tk.StringVar()
        angle_value = tk.StringVar()
        dragMin_value = tk.StringVar()
        dragDelta_value = tk.StringVar()
        dragMax_value = tk.StringVar()
        wall_height = tk.StringVar()
        wall_distance = tk.StringVar()
        list_of_variables = [v_value, h_value, angle_value, dragMin_value, dragDelta_value, dragMax_value, wall_height,
                             wall_distance]
        set_0(list_of_variables)

        # Entry boxes
        EB_velocity = tk.Entry(self, textvariable=v_value, width=10)
        EB_height = tk.Entry(self, textvariable=h_value, width=10)
        EB_angle = tk.Entry(self, textvariable=angle_value, width=10)
        EB_dragMin = tk.Entry(self, textvariable=dragMin_value, width=10)
        EB_dragDelta = tk.Entry(self, textvariable=dragDelta_value, width=10)
        EB_dragMax = tk.Entry(self, textvariable=dragMax_value, width=10)
        list_of_EB = [EB_velocity, EB_height, EB_angle, EB_dragMin, EB_dragDelta, EB_dragMax]
        Place(list_of_EB, 200, 102.5)
        EB_wall_height = tk.Entry(self, textvariable=wall_height, width=10)
        EB_wall_distance = tk.Entry(self, textvariable=wall_distance, width=10)

        B_run = ttk.Button(self, width=15, text='Run', command=lambda: drag_loop(eval(v_value.get()), eval(h_value.get()), eval(dragMin_value.get()),
                                                                                 eval(dragDelta_value.get()),eval(dragMax_value.get()), eval(angle_value.get()), 0, 0,
                                                                                 self.controller.app_data['mass'], self.controller.app_data['radius'],
                                                                                 self.controller.app_data['ball color']))
        B_run.place(x=240, y=290)

        # Checkbox
        def check_value():
            B_run.place_forget()
            if var.get():
                L_wall_height.place(x=10, y=240)
                L_wall_distance.place(x=10, y=260)
                EB_wall_height.place(x=120, y=242.5)
                EB_wall_distance.place(x=220, y=262.5)
                L_wall_units1.place(x=190, y=240)
                L_wall_units2.place(x=285, y=260)

                B_run1 = ttk.Button(self, width=15, text='Run', command=lambda: drag_loop(eval(v_value.get()), eval(h_value.get()), eval(dragMin_value.get()),
                                                                                          eval(dragDelta_value.get()), eval(dragMax_value.get()), eval(angle_value.get()),
                                                                                          eval(wall_height.get()), eval(wall_distance.get(())), self.controller.app_data['mass'],
                                                                                          self.controller.app_data['radius'], self.controller.app_data['ball color']))
                B_run1.place(x=240, y=290)

            else:
                L_wall_height.place_forget()
                L_wall_distance.place_forget()
                EB_wall_height.place_forget()
                EB_wall_distance.place_forget()
                L_wall_units1.place_forget()
                L_wall_units2.place_forget()

                B_run2 = ttk.Button(self, width=15, text='Run', command=lambda: drag_loop(eval(v_value.get()), eval(h_value.get()),
                                                                                          eval(dragMin_value.get()), eval(dragDelta_value.get()), eval(dragMax_value.get()),
                                                                                          eval(angle_value.get()), 0, 0,
                                                                                          self.controller.app_data['mass'], self.controller.app_data['radius'],
                                                                                          self.controller.app_data['ball color']))
                B_run2.place(x=240, y=290)

        var = tk.IntVar()
        C1 = tk.Checkbutton(self, text='Create a wall', command=check_value, variable=var)
        C1.place(x=10, y=220)

        ## Buttons
        B_settings = ttk.Button(self, width=15, text='Settings', command=lambda: controller.show_frame(settings_page))
        B_settings.pack()
        B_home = ttk.Button(self, width=15, text='Home', command=lambda: controller.show_frame(main_menu))
        B_home.pack()


class user_manual(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        L_title = tk.Label(self, text='User Manual', font=font)
        L_title.pack(pady=10, padx=10)
        B_choose_simulation = ttk.Button(self, width=17, text='Choose Simulation', command=lambda: controller.show_frame(choose_simulation))
        B_choose_simulation.pack()
        B_home = ttk.Button(self, width=17, text='Home', command=lambda: controller.show_frame(main_menu))
        B_home.pack()
        S = tk.Scrollbar(self)
        T = tk.Text(self, height=200, width=400)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack()
        S.config(command=T.yview)
        with open('user_manual.txt', 'r') as user_manual:
            data = user_manual.read()
        T.insert(tk.END, data)
        T.config(state='disabled')

app = Foundation()
app.mainloop()
