import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math

# TASK 2


plt.style.use('bmh')  # 4, 9, 16, 26

fig, ax = plt.subplots()
fig.canvas.manager.set_window_title('Task 2')
ax.set_title('Drag-Free Projectile (Analytical model)')
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

plt.subplots_adjust(right=0.7)


# (when an input is changed)
def UpdateGraph():
    x, y, maxX, maxY = Physics(U, Angle, H, G)

    for line in ax.lines:
        line.remove()

    l, = ax.plot(x, y, lw=1.5, label='y = ax^2 + bx + c')  # trajectory

    p, = ax.plot(maxX, maxY, color='black', marker='x', markersize=4)  # apogee

    # set axis boundaries to positive
    ax.set_xlim(0, max(x[-1]*1.1, 1))
    ax.set_ylim(0, max(y)*1.1)

    ax.legend()  # key/legend
    plt.show()


deltaX, U, Angle, G, H = 0.01, 24, math.radians(30), 9.81, 20


# Calculate horizontal and vertical displacement (x and y)
def Physics(u, angle, h, g):
    xValues = []
    yValues = []

    # Apogee
    maxX = (u ** 2 * math.sin(angle) * math.cos(angle)) / g
    maxY = (u ** 2 * math.sin(angle) ** 2) / (2 * g) + h

    # Analytical variables
    a = (-g * (1 + math.tan(angle) ** 2)) / (2 * u ** 2)
    b = math.tan(angle)
    c = h

    x = 0
    while True:
        x += deltaX
        y = (a * x**2) + (b * x) + c  # Analytical equation

        xValues.append(x)
        yValues.append(y)

        if y < 0:
            # range = x
            break

    return xValues, yValues, maxX, maxY


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
    global g
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

angleInput = TextBox(inputs[0], 'Angle (degrees) ', initial='30')
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
