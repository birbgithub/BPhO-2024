import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math
from math import sin
from math import cos

# TASK 1


# - graph setup -

plt.style.use('bmh')  # 4, 9, 16, 26

fig, ax = plt.subplots()

fig.canvas.manager.set_window_title('Task 1')
ax.set_title('Drag-free projectile (Numerical)')
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

plt.subplots_adjust(right=0.7)


# (when an input is changed)
def UpdateGraph():
    for line in ax.lines:
        line.remove()

    xArr, yArr = Physics(U, Angle, H, G)
    l, = ax.plot(xArr, yArr, lw=1.5, label='Trajectory')

    # formatting
    ax.set_xlim(0, max(xArr[-1]*1.1, 1))
    ax.set_ylim(0, max(yArr)*1.1)
    ax.legend()

    plt.show()


deltaTime, U, Angle, G, H = 0.01, 24, math.radians(30), 9.81, 20


# Calculate horizontal and vertical displacement (x and y)
def Physics(u, angle, h, g):
    x = 0
    y = h

    xValues = [0]
    yValues = [H]

    verticalV = u * sin(angle)
    horizontalV = u * cos(angle)

    while True:

        # Changing velocity
        verticalV += -g * deltaTime

        # Changing position
        x += horizontalV * deltaTime
        y += verticalV * deltaTime

        # Adding x and y values to array
        xValues.append(x)
        yValues.append(y)

        if y < 0:
            break

    return xValues, yValues


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
    G = float(n)
    UpdateGraph()


def setHeight(n):
    global H
    H = float(n)
    UpdateGraph()


def setDeltaTime(n):
    global deltaTime
    deltaTime = float(n)
    UpdateGraph()


inputs = []
for i in range(5):
    inputs.append(plt.axes([0.9, 0.7 - i*0.09, 0.08, 0.065]))

angleInput = TextBox(inputs[0], 'angle (degrees) ', initial='30')
angleInput.on_submit(setAngle)
uInput = TextBox(inputs[1], 'u (ms^-1) ', initial='24')
uInput.on_submit(setU)
gInput = TextBox(inputs[2], 'g (ms^-2) ', initial='9.81')
gInput.on_submit(setG)
hInput = TextBox(inputs[3], 'h (m) ', initial='20')
hInput.on_submit(setHeight)
dtInput = TextBox(inputs[4], 'delta time (s) ', initial='0.01')
dtInput.on_submit(setDeltaTime)

UpdateGraph()
