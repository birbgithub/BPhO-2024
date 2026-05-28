import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math
from math import sin
from math import cos
from math import tan
from math import atan

# TASK 3
# Projectile model that passes through a fixed position (X, Y)
# Low and High Ball trajectories

# min u = (g**0.5)((Y + (X**2 + Y**2)**0.5)**0.5

# Change (x, y), g, and delta X

U, deltaX, X, Y, G, H = 24, 0.01, 30, 10, 9.81, 4


def calcMinVelocityAndAngle():
    minU = (G ** 0.5) * (((Y - H) + (X ** 2 + (Y - H) ** 2) ** 0.5) ** 0.5)
    angle = math.atan((minU ** 2) / (G * X))

    if U < minU:
        print("Speed too low to reach (X, Y)")

    return minU, angle


def calcAngles(speed):
    # High and Low Angles

    a = (G * X ** 2) / (2 * speed ** 2)
    b = -X
    c = Y - H + a

    discriminant = round(b**2 - 4*a*c, 4)

    if discriminant < 0:
        print("Velocity less than minimum")
        return 0, 0  # returns placeholder angle
    else:
        highAngle = atan((-b + discriminant ** 0.5)/(2 * a))
        lowAngle = atan((-b - discriminant ** 0.5)/(2 * a))
        return highAngle, lowAngle


# Calculate horizontal and vertical displacement (x and y)
def Physics(u, angle):
    xVals = []
    yVals = []

    a = (-G * (1 + tan(angle) ** 2)) / (2 * u ** 2)
    b = math.tan(angle)
    c = H

    x = 0
    while True:
        x += deltaX
        y = (a * x**2) + (b * x) + c

        xVals.append(x)
        yVals.append(y)

        if x >= X:
            # range = x
            break

    return xVals, yVals

# Graphs


plt.style.use('bmh')  # 4, 9, 16, 26

fig, ax = plt.subplots()
fig.canvas.manager.set_window_title('Task 3')
ax.set_title('Projectile that passes through (X, Y)')
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

plt.subplots_adjust(right=0.7)


def UpdateGraph():
    # minimum velocity
    minU, angle = calcMinVelocityAndAngle()
    xArr1, yArr1 = Physics(minU, angle)

    # high and low ball
    highAngle, lowAngle = calcAngles(U)
    xArr2, yArr2 = Physics(U, highAngle)
    xArr3, yArr3 = Physics(U, lowAngle)

    for line in ax.lines:
        line.remove()

    l, = ax.plot(xArr1, yArr1, lw=1.5, label='Min U')  # trajectory
    l, = ax.plot(xArr2, yArr2, lw=1.5, label='High ball')  # trajectory
    l, = ax.plot(xArr3, yArr3, lw=1.5, label='Low ball')  # trajectory

    p, = ax.plot(X, Y, color='black', marker='o', markersize=4)  # target

    # set axis boundaries to positive
    ax.set_xlim(0, X*1.1)
    ax.set_ylim(0, max(max(yArr2), max(yArr3))*1.1)

    ax.legend()  # key/legend
    plt.show()


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
    u = float(n)
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
hInput = TextBox(inputs[4], 'h (m) ', initial='4')
hInput.on_submit(setHeight)
dxInput = TextBox(inputs[5], 'Delta x (m) ', initial='0.01')
dxInput.on_submit(setDeltaX)

UpdateGraph()
