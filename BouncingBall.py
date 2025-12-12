import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Ball():
    def __init__(self, x, y, radius, mass, speedX, speedY):
        self.x = x
        self.y = y
        
        self.radius = radius
        self.mass = mass

        self.speedX = speedX
        self.speedY = speedY

        self.g = 15
        
    def force(self, fx, fy, dt):
        ax = fx / self.mass
        ay = fy / self.mass

        self.speedX += ax * dt
        self.speedY += ay * dt

    def update_position(self, dt):
        self.speedY -= self.g*dt
        
        self.x += self.speedX * dt
        self.y += self.speedY * dt

    def barrier_collision(self, left_wall, right_wall, roof, floor_y=0.0, restitution=0.8):
        if self.y - self.radius < floor_y:
            self.y = floor_y + self.radius
            self.speedY = - self.speedY * restitution

        if self.y + self.radius > roof:
            self.y = roof - self.radius
            self.speedY = - self.speedY * restitution

        if self.x - self.radius < left_wall:
            self.x = left_wall + self.radius
            self.speedX = -self.speedX * restitution
        
        if self.x + self.radius > right_wall:
            self.x = right_wall - self.radius
            self.speedX = - self.speedX * restitution

    def friction(self, floor, dt, mu=0.3):
        if np.isclose(self.y - self.radius, floor):

            if abs(self.speedX) < 0.05:
                self.speedX = 0
                return
            
            a_f = -mu * self.g * np.sign(self.speedX)
            self.speedX += a_f * dt

def update(frame):
    for b, c in zip(balls, circles):
        b.update_position(dt)
        b.barrier_collision(left_wall, right_wall, roof, floor)
        b.friction(floor, dt)

        c.center = (b.x, b.y)

    time = dt * frame
    time_text.set_text(f"Time: {time:.2f} s")
    return (*circles, time_text)


balls = [
    Ball(x=0.0, y=3.0, radius=0.1, mass=1.0, speedX=10.0, speedY=10.0),
    Ball(x=-2.0, y=4.0, radius=0.2, mass=2.0, speedX=5.0,  speedY=8.0),
    Ball(x=2.0,  y=2.0, radius=0.15, mass=1.5, speedX=-7.0, speedY=12.0),
]


left_wall = -5
right_wall = 5
floor = 0
roof = 5

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.set_xlim(left_wall-1, right_wall+1)
ax.set_ylim(floor-1, roof+1)

ax.plot([left_wall, right_wall], [floor, floor], "r-")   
ax.plot([left_wall, right_wall], [roof, roof], "r-")   
ax.plot([left_wall, left_wall], [floor, roof], "r-")    
ax.plot([right_wall, right_wall], [floor, roof], "r-")   

time_text = ax.text(
    0.02, 0.95, "", transform=ax.transAxes,
    ha="left", va="top"
)

circles = []
colors = ["red", "blue", "green", "orange", "purple"]
for b, col in zip (balls, colors):
    c = plt.Circle((b.x, b.y), b.radius, color=col)
    ax.add_patch(c)
    circles.append(c)


dt = 0.01
n_steps = 2000

ani = FuncAnimation(
    fig, 
    update,
    frames=n_steps,
    interval=dt*1000,
    blit=True
)

plt.show()
