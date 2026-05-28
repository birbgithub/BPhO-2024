import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math
from math import sin
from math import cos

# TASK 9

plt.style.use('bmh')  # 4, 9, 16, 26

fig, ax = plt.subplots(figsize=(12, 7))

fig.canvas.manager.set_window_title('Task 9')
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

plt.subplots_adjust(right=7/12)


# (when an input is changed)
def UpdateGraph():
    for line in ax.lines:
        line.remove()

    x1, y1, totalT1 = Physics(U, math.radians(Angle), H, E, Bounces)

    l, = ax.plot(x1, y1, lw=1.5, label='Drag-free')
    p, = ax.plot(x1[-1], 0, marker='x', color='black', ls='None', label=f'R = {round(x1[-1], 1)}m')

    x2, y2, totalT2 = AirResistancePhysics(U, math.radians(Angle), H, E, Bounces, M, Drag, AirDensity, Area, G)

    l, = ax.plot(x2, y2, lw=1.5, label='Air resistance')
    p, = ax.plot(x2[-1], 0, marker='x', color='grey', ls='None', label=f'R = {round(x2[-1], 1)}m')

    ax.set_xlim(0, max(x1[-1]*1.1, 1))
    ax.set_ylim(0, max(y1)*1.1)

    ax.set_title(f'Drag-Free vs Air resistance: t(no air)={totalT1}s, t(air)={totalT2}s')
    ax.legend()
    plt.show()


deltaTime, U, Angle, G, H, E, Bounces, M, Drag, AirDensity, Area = 0.005, 14, 40, 9.81, 6, 0.6, 0, 1, 0.47, 1.2, 0.1


# Calculate horizontal and vertical displacement (x and y)
def Physics(u, angle, h, e, totalBounces):
    t = 0
    verticalV = u * math.sin(angle)
    horizontalV = u * math.cos(angle)
    x = 0
    y = h

    xLst = [x]
    yLst = [y]
    tLst = [t]

    bounces = 0
    inAir = True

    while True:
        verticalV += -G * deltaTime
        y += verticalV * deltaTime

        x += horizontalV * deltaTime

        t += deltaTime

        xLst.append(x)
        yLst.append(y)

        if y <= 0 and inAir:
            inAir = False
            if bounces == totalBounces:
                break
            else:
                bounces += 1
                verticalV = verticalV * -e
                print(verticalV)
        elif y > 0:
            inAir = True

    return xLst, yLst, round(t, 2)


def AirResistancePhysics(u, angle, h, e, totalBounces, mass, drag, airDensity, area, g):
    k = (drag * airDensity * area)/(2 * mass)

    t = 0
    verticalV = u * sin(angle)
    horizontalV = u * cos(angle)
    x = 0
    y = h

    xLst = [x]
    yLst = [y]

    bounces = 0
    inAir = True
    while True:
        v = (verticalV**2 + horizontalV**2)**0.5

        # acceleration
        horizontalA = k * horizontalV * v
        verticalA = (k * verticalV * v) + g

        # velocity
        horizontalV += -horizontalA * deltaTime
        verticalV += -verticalA * deltaTime

        # position
        x += horizontalV * deltaTime
        y += verticalV * deltaTime

        t += deltaTime

        xLst.append(x)
        yLst.append(y)

        if y <= 0 and inAir:
            inAir = False
            if bounces == totalBounces:
                break
            else:
                bounces += 1
                verticalV = verticalV * -e
                print(verticalV)
        elif y > 0:
            inAir = True

    return xLst, yLst, round(t, 2)


def Pythagoras(a, b):
    return (a**2 + b**2)**0.5


# -- Input fields --

def setAngle(n):
    global Angle
    Angle = float(n)
    UpdateGraph()


def setU(n):
    global U
    U = float(n)
    UpdateGraph()


def setG(n):
    global G
    g = float(n)
    UpdateGraph()


def setHeight(n):
    global H
    H = float(n)
    UpdateGraph()


def setDeltaTime(n):
    global deltaTime
    deltaTime = float(n)
    UpdateGraph()


def setE(n):
    global E
    E = float(n)
    UpdateGraph()


def setBounces(n):
    global Bounces
    Bounces = float(n)
    UpdateGraph()


# mass, drag, airDensity, area = 1, 0.47, 1, 1

def setMass(n):
    global M
    M = float(n)
    UpdateGraph()


def setDrag(n):
    global Drag
    Drag = float(n)
    UpdateGraph()


def setAirDensity(n):
    global AirDensity
    AirDensity = float(n)
    UpdateGraph()


def setArea(n):
    global Area
    Area = float(n)
    UpdateGraph()


# mass, drag, airDensity, area = 1, 0.47, 1, 1

inputs = []
for i in range(7):
    inputs.append(plt.axes([0.7, 0.8 - i*0.07, 0.05, 0.045]))

angleInput = TextBox(inputs[0], 'Angle (degrees) ', initial='40')
angleInput.on_submit(setAngle)
uInput = TextBox(inputs[1], 'u (ms^-1) ', initial='14')
uInput.on_submit(setU)
gInput = TextBox(inputs[2], 'g (ms^-2) ', initial='9.81')
gInput.on_submit(setG)
hInput = TextBox(inputs[3], 'h (m) ', initial='6')
hInput.on_submit(setHeight)
dtInput = TextBox(inputs[4], 'delta t (s) ', initial='0.005')
dtInput.on_submit(setDeltaTime)
eInput = TextBox(inputs[5], 'e (0 < x < 1) ', initial='0.6')
eInput.on_submit(setE)
bouncesInput = TextBox(inputs[6], 'Bounces ', initial='0')
bouncesInput.on_submit(setBounces)

dragInputs = []
for i in range(4):
    dragInputs.append(plt.axes([0.93, 0.8 - i*0.07, 0.05, 0.045]))

massInput = TextBox(dragInputs[0], 'Mass (kg) ', initial='1')
massInput.on_submit(setMass)
areaInput = TextBox(dragInputs[1], 'Cross-sectional area (m^2) ', initial='0.1')
areaInput.on_submit(setArea)
dragInput = TextBox(dragInputs[2], 'Drag Coefficient ', initial='0.47')
dragInput.on_submit(setDrag)
densityInput = TextBox(dragInputs[3], 'Air Density (kgm^-3) ', initial='1.2')
densityInput.on_submit(setAirDensity)

UpdateGraph()
