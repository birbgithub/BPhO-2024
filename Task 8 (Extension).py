import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import math
from matplotlib.animation import FuncAnimation

# TASK 8 (Extension)


plt.style.use('bmh')

fig, ax = plt.subplots(figsize=(10, 7))

fig.canvas.manager.set_window_title('Task 8 (Extension)')
ax.set_xlabel('x /m')
ax.set_ylabel('y /m')

plt.subplots_adjust(right=0.65)

xArr, yArr = [], []
l, = ax.plot(xArr, yArr, lw=1.5, label='Trajectory')
p, = ax.plot(0, 0, marker='.', color='black', ls='None', label=f'(0, 0)')


# (when an input is changed)
def UpdateGraph():
    global xArr, yArr
    global l
    global p
    for line in ax.lines:
        line.remove()

    xArr, yArr, totalT = Physics(U, math.radians(Angle), H, E, Bounces)
    l, = ax.plot(xArr, yArr, lw=1.5, label='Trajectory')
    p, = ax.plot(xArr[-1], 0, marker='x', color='black', ls='None', label=f'({round(xArr[-1], 1)}, 0)')

    aniLine = FuncAnimation(fig, animateLine,
                            interval=deltaTime, blit=True)

    # l, = ax.plot(x, y, lw=1.5, label='Trajectory')

    #aniPoint = animation.FuncAnimation(
        #fig, animatePoint, interval=1, blit=False, save_count=50)

    #p, = ax.plot(x[-1], 0, marker='x', color='black', ls='None', label=f'({round(x[-1], 1)}, 0)')

    ax.set_xlim(0, max(xArr[-1] * 1.1, 1))
    ax.set_ylim(0, max(yArr) * 1.1)

    ax.set_title(f'Projectile: u={U}ms^-1, e={E}, θ={Angle}°, total time={totalT}s, {Bounces} bounces')
    #ax.legend()
    plt.show()


deltaTime, U, Angle, G, H, E, Bounces = 0.005, 14, 20, 9.81, 10, 0.5, 4


def animateLine(j):
    j = j % len(xArr)
    l.set_xdata(xArr[:j + 1])  # update the data.
    l.set_ydata(yArr[:j + 1])
    return l,


def animatePoint(j):
    j = j % len(xArr)
    p.set_xdata(xArr[j])  # update the data.
    p.set_ydata(yArr[j])
    return p,


# Calculate horizontal and vertical displacement (x and y)
def Physics(u, angle, h, e, totalBounces):
    t = 0
    verticalV = u * math.sin(angle)
    horizontalV = u * math.cos(angle)
    x = 0
    y = h

    xVals = [x]
    yVals = [y]

    bounces = 0
    inAir = True

    while True:
        verticalV += -G * deltaTime
        y += verticalV * deltaTime

        x += horizontalV * deltaTime

        t += deltaTime

        xVals.append(x)
        yVals.append(y)

        if y <= 0 and inAir:
            inAir = False
            if bounces == totalBounces:
                break
            else:
                verticalV = verticalV * -e
                bounces += 1
        elif y > 0:
            inAir = True

    return xVals, yVals, round(t, 2)


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


inputs = []
for i in range(7):
    inputs.append(plt.axes([0.9, 0.7 - i*0.09, 0.08, 0.065]))

angleInput = TextBox(inputs[0], 'Angle (degrees) ', initial='20')
angleInput.on_submit(setAngle)
uInput = TextBox(inputs[1], 'u (ms^-1) ', initial='14')
uInput.on_submit(setU)
gInput = TextBox(inputs[2], 'g (ms^-2) ', initial='9.81')
gInput.on_submit(setG)
hInput = TextBox(inputs[3], 'h (m) ', initial='10')
hInput.on_submit(setHeight)
dtInput = TextBox(inputs[4], 'delta t (s) ', initial='0.005')
dtInput.on_submit(setDeltaTime)
eInput = TextBox(inputs[5], 'e (0 < x < 1) ', initial='0.5')
eInput.on_submit(setE)
bouncesInput = TextBox(inputs[6], 'Bounces ', initial='4')
bouncesInput.on_submit(setBounces)

UpdateGraph()
