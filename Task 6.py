import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math
from math import tan

# TASK 6

# - graph setup -

plt.style.use('bmh')  # 4, 9, 16, 26

fig, ax = plt.subplots(figsize=(7.3, 6))
fig.canvas.manager.set_window_title('Task 6')
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

plt.subplots_adjust(right=0.7)


# (when an input is changed)
def UpdateGraph():
    x, y, R = Physics(Angle)

    maxAngle = calcThetaForMaxRange()
    xMax, yMax, RMax = Physics(maxAngle)

    s = calcDistanceTravelled(U, Angle, R)
    sMax = calcDistanceTravelled(U, maxAngle, RMax)

    sDifference = round(abs(sMax - s), 2)

    for line in ax.lines:
        line.remove()

    l, = ax.plot(x, y, lw=1.5, label=f'θ = {round(Angle, 2)} rad')  # trajectory
    l, = ax.plot(xMax, yMax, lw=1.5, ls='--', label=f'θ = {round(maxAngle, 2)} rad')  # trajectory

    # p, = ax.plot(xTop, yTop, color='black', marker='x', markersize=4)  # apogee
    # p, = ax.plot(xMaxTop, yMaxTop, color='black', marker='x', markersize=4)  # apogee

    # set axis boundaries to positive
    ax.set_xlim(0, max(xMax[-1]*1.1, 1))
    ax.set_ylim(0, max(max(yMax), max(y))*1.1)

    ax.set_title(f's={round(s, 2)}m, sMax={round(sMax, 2)}m, sDifference={sDifference}m')
    ax.legend()  # key/legend
    plt.show()


deltaX, U, Angle, G, H = 0.01, 24, math.radians(60), 9.81, 20


# Calculate horizontal and vertical displacement (x and y)
def Physics(angle):
    xVals = [0]
    yVals = [H]

    a = (-G * (1 + math.tan(angle) ** 2)) / (2 * U ** 2)
    b = math.tan(angle)
    c = H

    totalDistance = 0

    x = 0
    while True:
        x += deltaX
        y = (a * x**2) + (b * x) + c

        totalDistance += pythagoras(x, y, xVals[-1], yVals[-1])

        xVals.append(x)
        yVals.append(y)

        if y < 0:
            # range = x
            break

    print(totalDistance)

    Range = calcRange(U, angle, H)

    return xVals, yVals, Range


def pythagoras(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def calcThetaForMaxRange():
    theta = math.asin(1 / ((2 + (2 * G * H) / (U ** 2)) ** 0.5))
    return theta


def calcDistanceTravelled(u, angle, R):
    # Reducing duplicate code
    t = tan(angle)
    a = 1 + t**2

    b = zEvaluation(t)
    c = zEvaluation(t - ((G * R) / (u ** 2)) * a)

    # Equation for distance travelled
    s = ((u**2) / (G * a)) * (b - c)
    return s


# section in square brackets
def zEvaluation(z):
    a = (1 + z**2)**0.5
    return (math.log(abs(a + z)) + z * a)/2


def calcRange(u, angle, h):
    cos = math.cos(angle)
    sin = math.sin(angle)
    return ((u**2) / G) * (sin * cos + cos * (sin ** 2 + (2 * G * h) / (u ** 2)) ** 0.5)


    #a = (u**2)/g
    #s = a * ((math.log(1 + math.sin(angle))/math.cos(angle))*(math.cos(angle)**2) + math.sin(angle))
    #return s


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
uInput = TextBox(inputs[1], 'u (ms^-1) ', initial='24')
uInput.on_submit(setU)
gInput = TextBox(inputs[2], 'g (ms^-2) ', initial='9.81')
gInput.on_submit(setG)
hInput = TextBox(inputs[3], 'h (m) ', initial='20')
hInput.on_submit(setHeight)
dxInput = TextBox(inputs[4], 'Delta x (m) ', initial='0.01')
dxInput.on_submit(setDeltaX)

UpdateGraph()
