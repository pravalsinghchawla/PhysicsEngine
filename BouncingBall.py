import matplotlib.pyplot as plt

class Ball():
    def __init__(self, x, y, radius, mass, speedX, speedY):
        self.x = x
        self.y = y
        
        self.radius = radius
        self.mass = mass

        self.speedX = speedX
        self.speedY = speedY
        
    def force(self, fx, fy, dt):
        ax = fx / self.mass
        ay = fy / self.mass

        self.speedX += ax * dt
        self.speedY += ay * dt

    def update(self, dt, gravity=9.81):
        self.speedY -= gravity*dt
        
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

ball = Ball(x=0.0, y=3.0, speedX=-2.0, speedY=1.0, radius=0.1, mass=1.0)

left_wall = -5
right_wall = 5
floor = 0
roof = 5

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.set_xlim(left_wall, right_wall)
ax.set_ylim(floor-1, roof)

ax.axhline(0.0, linestyle="--")

# Tegn ball (circle-patch som vi oppdaterer)
circle = plt.Circle((ball.x, ball.y), ball.radius)
ax.add_patch(circle)

dt = 0.01
n_steps = 1000

for step in range(n_steps):
    # Fysikk
    ball.update(dt)
    ball.barrier_collision(left_wall, right_wall, roof, floor)

    # Oppdater grafikken
    circle.center = (ball.x, ball.y)

    if ball.speedX == 0 or ball.speedY == 0:
        break

    # Oppdater tegningen på skjerm
    plt.pause(dt)  # liten pause så du ser animasjonen

plt.show()