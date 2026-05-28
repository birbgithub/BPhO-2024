import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math

# TASK 5


U, deltaX, X, Y, G, H = 24, 0.01, 30, 10, 9.81, 0

# Calculate horizontal and vertical displacement (x and y)
def Physics(u, angle, h):
    xVals = []
    yVals = []

    a = (-G * (1 + math.tan(angle) ** 2)) / (2 * u ** 2)
    b = math.tan(angle)
    c = h

    x = 0
    while True:
        x += deltaX

        y = (a * x**2) + (b * x) + c
        if y < 0:
            break

        xVals.append(x)
        yVals.append(y)

    return xVals, yVals


# Graphs


plt.style.use('bmh')  # 4, 9, 16, 26

fig, ax = plt.subplots(figsize=(9, 7))
fig.canvas.manager.set_window_title('Task 5')
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

plt.subplots_adjust(right=0.7)


def UpdateGraph():
    for line in ax.lines:
        line.remove()

    minU, minUAngle = calcMinVelocityAndAngle()
    highAngle, lowAngle = calcAngles(U)
    maxRAngle = calcThetaForMaxRange()
    boundingHeight = calcBoundingHeight()

    # Trajectories
    x1, y1 = Physics(minU, minUAngle, H)  # Minimum u to reach (X, Y)
    x2, y2 = Physics(U, highAngle, H)  # High ball to reach (X, Y)
    x3, y3 = Physics(U, lowAngle, H)  # Low ball to reach (X, Y)
    x4, y4 = Physics(U, maxRAngle, H)  # Max range with u, g, and h
    x5, y5 = boundingParabola(U, H, G) # Bounding parabola

    l, = ax.plot(x5, y5, lw=1.5, ls=':', label='Bounding')  # trajectory
    l, = ax.plot(x1, y1, lw=1.5, label='Min U')  # trajectory
    l, = ax.plot(x2, y2, lw=1.5, label='High ball')  # trajectory
    l, = ax.plot(x3, y3, lw=1.5, label='Low ball')  # trajectory
    l, = ax.plot(x4, y4, lw=1.5, ls='--', label='Max range')  # trajectory

    p, = ax.plot(0, H, color='blue', marker='x', ls='None', markersize=4, label=f'(0, {H})')  # launch
    p, = ax.plot(X, Y, color='black', marker='x', ls='None', markersize=4, label=f'({X}, {Y})')  # target

    # set axis boundaries to positive
    ax.set_xlim(0, x5[-1] * 1.1)
    ax.set_ylim(0, boundingHeight * 1.1)

    ax.set_title(f'Projectile through ({X}, {Y}), R max={round(x5[-1], 1)}m, U min={round(minU, 1)}ms^-1')

    ax.legend()  # key/legend
    plt.show()


def calcThetaForMaxRange():
    theta = math.asin(1 / ((2 + (2 * G * H) / (U ** 2)) ** 0.5))
    return theta


def calcMinVelocityAndAngle():
    y = Y - H
    minU = (G ** 0.5) * ((y + (X ** 2 + y ** 2) ** 0.5) ** 0.5)
    angle = math.atan((minU ** 2) / (G * X))

    if U < minU:
        print("Speed too low to reach (X, Y)")

    return minU, angle


def calcAngles(u):

    # High and Low Angles
    a = (G * X ** 2) / (2 * u ** 2)
    b = -X
    c = Y + a - H

    discriminant = round(b**2 - 4*a*c, 4)
    # print(round(discriminant, 4))

    highAngle = math.atan((-b + discriminant ** 0.5)/(2 * a))
    lowAngle = math.atan((-b - discriminant ** 0.5)/(2 * a))

    return highAngle, lowAngle


def calcBoundingHeight():
    h = (U**2) / (2 * G) + H
    return h


def boundingParabola(u, h, g):
    xValues = []
    yValues = []

    a = (u**2)/(2*g) + h
    b = (g)/(2 * u**2)

    x = 0
    while True:
        x += deltaX
        y = a - b*(x**2)

        xValues.append(x)
        yValues.append(y)

        if y < 0:
            break

    return xValues, yValues


# -- Input fields --

def setX(n):
    global X
    X = float(n)
    UpdateGraph()


def setY(n):
    global Y
    Y = float(n)
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
for i in range(6):
    inputs.append(plt.axes([0.9, 0.7 - i*0.09, 0.08, 0.065]))

xInput = TextBox(inputs[0], 'X ', initial='30')
xInput.on_submit(setX)
yInput = TextBox(inputs[1], 'Y ', initial='10')
yInput.on_submit(setY)
uInput = TextBox(inputs[2], 'u (ms^-1) ', initial='24')
uInput.on_submit(setU)
gInput = TextBox(inputs[3], 'g (ms^-2) ', initial='9.81')
gInput.on_submit(setG)
hInput = TextBox(inputs[4], 'h (m) ', initial='0')
hInput.on_submit(setHeight)
dxInput = TextBox(inputs[5], 'Delta x (m) ', initial='0.01')
dxInput.on_submit(setDeltaX)

UpdateGraph()
