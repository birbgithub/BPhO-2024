import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math
from math import asin
from math import sin
from math import cos

# TASK 4

plt.style.use('bmh')

fig, ax = plt.subplots(figsize=(7.3, 6))
fig.canvas.manager.set_window_title('Task 4')
ax.set_title('Max Range')
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')


plt.subplots_adjust(right=0.7)


# (when an input is changed)
def UpdateGraph():
    # input trajectory
    x, y, xApogee, yApogee = Physics(Angle)
    inputRange = calcRange(U, G, Angle, H)

    # trajectory of maximum range
    maxAngle = calcThetaForMaxRange(U, G, H)
    maxRange = calcRange(U, G, maxAngle, H)
    xMax, yMax, xMaxApogee, yMaxApogee = Physics(maxAngle)

    rDifference = maxRange - inputRange

    for line in ax.lines:
        line.remove()

    l, = ax.plot(x, y, lw=1.5, label=f'(Input) θ = {round(Angle, 2)} rad')  # trajectory
    l, = ax.plot(xMax, yMax, lw=1.5, ls='--', label=f'(Max range) θ = {round(maxAngle, 2)} rad')  # trajectory

    p, = ax.plot(xApogee, yApogee, color='black', marker='x', markersize=4)  # apogee
    p, = ax.plot(xMaxApogee, yMaxApogee, color='black', marker='x', markersize=4)  # apogee

    # set axis boundaries to positive
    ax.set_xlim(0, max(xMax[-1]*1.1, 1))
    ax.set_ylim(0, max(max(yMax), max(y))*1.1)

    ax.set_title(f'Range={inputRange}m, MaxRange={maxRange}m, Difference={round(rDifference, 2)}m')
    ax.legend()  # key/legend
    plt.show()


deltaX, U, Angle, G, H = 0.01, 15, math.radians(60), 9.81, 18


# Calculate horizontal and vertical displacement (x and y)
def Physics(angle):
    xVals = []
    yVals = []

    maxX = (U ** 2 * math.sin(angle) * math.cos(angle)) / G
    maxY = (U ** 2 * math.sin(angle) ** 2) / (2 * G) + H

    a = (-G * (1 + math.tan(angle) ** 2)) / (2 * U ** 2)
    b = math.tan(angle)
    c = H

    x = 0
    while True:
        x += deltaX
        y = (a * x**2) + (b * x) + c

        xVals.append(x)
        yVals.append(y)

        if y < 0:
            print(x)
            break

    return xVals, yVals, maxX, maxY


def calcThetaForMaxRange(u, g, h):
    theta = asin(1 / ((2 + (2 * g * h) / (u ** 2)) ** 0.5))
    return theta


def calcRange(u, g, angle, h):
    r = ((u**2)/g)*(sin(angle)*cos(angle) + cos(angle)*(sin(angle)**2 + (2*g*h)/u**2)**0.5)
    return round(r, 2)


# -- Input fields --

def setAngle(n):
    global Angle
    Angle = math.radians(float(n))
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


def setDeltaX(n):
    global deltaX
    deltaX = float(n)
    UpdateGraph()


inputs = []
for i in range(5):
    inputs.append(plt.axes([0.9, 0.7 - i*0.09, 0.08, 0.065]))

angleInput = TextBox(inputs[0], 'Angle (degrees) ', initial='60')
angleInput.on_submit(setAngle)
uInput = TextBox(inputs[1], 'u (ms^-1) ', initial='15')
uInput.on_submit(setU)
gInput = TextBox(inputs[2], 'g (ms^-2) ', initial='9.81')
gInput.on_submit(setG)
hInput = TextBox(inputs[3], 'h (m) ', initial='18')
hInput.on_submit(setHeight)
dxInput = TextBox(inputs[4], 'Delta x (m) ', initial='0.01')
dxInput.on_submit(setDeltaX)

UpdateGraph()
