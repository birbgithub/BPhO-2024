import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math
from math import sin
from math import cos

# TASK 7


U, deltaT, G, H, Angle = 10, 0.01, 9.81, 11, 70.5

maxT = 3


def DisplacementTime(u, angle):
    tValues = []
    sValues = []

    t = 0
    while True:
        t += deltaT
        if t > maxT:
            break

        s = calcDisplacement(u, angle, t)

        tValues.append(t)
        sValues.append(s)

    return tValues, sValues


def calcDisplacement(u, angle, t):
    return ((u*t) ** 2 - (G * t ** 3 * u * math.sin(angle)) + (G ** 2 * t ** 4) / 4) ** 0.5


def StationaryPoints(u, angle):
    Sin = sin(angle)
    a = Sin**2 - (8/9)
    if a > 0:
        b = (3*u)/(2 * G)
        t1 = b*(Sin + a**0.5)
        t2 = b*(Sin - a**0.5)

        s1 = calcDisplacement(u, angle, t1)
        s2 = calcDisplacement(u, angle, t2)

        ax.plot(t1, s1, marker='x', ls='None', markersize=4, color='black')
        ax.plot(t2, s2, marker='x', ls='None', markersize=4, color='black')

    elif round(a, 1) == 0:
        t = u * (2**0.5) / G
        r = calcDisplacement(u, angle, t)

        ax.plot(t, r, marker='x', ls='None', markersize=4, color='black')
    else:
        print("no max or min")


# Calculate horizontal and vertical displacement (x and y)
def Physics(u, angle, h, g):

    t = 0
    x = 0
    y = h

    xValues = [0]
    yValues = [h]

    verticalV = u * sin(angle)
    horizontalV = u * cos(angle)

    sValues = [0]
    tValues = [0]

    while True:
        # x and y
        verticalV += -g * deltaT
        # Changing position
        x += horizontalV * deltaT
        y += verticalV * deltaT
        # Adding x and y values to array
        xValues.append(x)
        yValues.append(y)

        # time and displacement
        t += deltaT
        s = pythagoras(x, y, 0, h)
        # Add t and s values to array
        tValues.append(t)
        sValues.append(s)

        if y < 0:
            break

    return xValues, yValues, tValues, sValues


def pythagoras(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Graphs

plt.style.use('bmh')  # 4, 9, 16, 26

# fig, ax = plt.subplots(figsize=(9, 7))
fig, ax = plt.subplots(figsize=(7.3, 6))
fig.canvas.manager.set_window_title('Task 7')
ax.set_xlabel('t /s')
ax.set_ylabel('y /m')

plt.subplots_adjust(right=0.7)


def UpdateGraph():
    for line in ax.lines:
        line.remove()

    # Displacement-Time Graph

    #t, s = DisplacementTime(U, math.radians(Angle))
    xArr, yArr, t, s = Physics(U, math.radians(Angle), H, G)

    l, = ax.plot(t, s, lw=1.5, label=f'θ = {Angle}°')
    #l, = ax.plot(t, yArr, lw=1.5, label=f'θ = {Angle}°')

    StationaryPoints(U, math.radians(Angle))

    theta = 45
    for j in range(5):
        #t, s = DisplacementTime(U, math.radians(theta))
        xArr, yArr, t, s = Physics(U, math.radians(theta), H, G)
        l, = ax.plot(t, s, lw=1.5, label=f'θ = {theta}°')
        StationaryPoints(U, math.radians(theta))

        theta += 10

    # set axis boundaries to positive
    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 17)

    # ax.set_title(f'Displacement-Time Graph')
    ax.set_title(f'Displacement-Time Graph')

    ax.legend()  # key/legend
    plt.show()


def UpdateGraph2():
    for line in ax.lines:
        line.remove()

    xArr, yArr, tArr, sArr = Physics(U, Angle, H, G)
    l, = ax.plot(xArr, yArr, lw=1.5, label='Trajectory')

    # formatting
    ax.set_xlim(0, max(xArr[-1]*1.1, 1))
    ax.set_ylim(0, max(yArr)*1.1)
    ax.legend()

    plt.show()


# -- Input fields --


def setU(n):
    global U
    U = float(n)
    UpdateGraph()


def setG(n):
    global G
    G = float(n)
    UpdateGraph()


def setHeight(n):
    global H
    H = float(n)
    UpdateGraph()


def setDeltaT(n):
    global deltaT
    deltaT = float(n)
    UpdateGraph()


def setAngle(n):
    global Angle
    Angle = float(n)
    UpdateGraph()


inputs = []
for i in range(4):
    inputs.append(plt.axes([0.9, 0.7 - i*0.09, 0.08, 0.065]))


uInput = TextBox(inputs[0], 'u (ms^-1) ', initial='10')
uInput.on_submit(setU)
gInput = TextBox(inputs[1], 'g (ms^-2) ', initial='9.81')
gInput.on_submit(setG)
dxInput = TextBox(inputs[2], 'Delta t (s) ', initial='0.01')
dxInput.on_submit(setDeltaT)
aInput = TextBox(inputs[3], 'Angle (°) ', initial='70.5')
aInput.on_submit(setAngle)

UpdateGraph()
