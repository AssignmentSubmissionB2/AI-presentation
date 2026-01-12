import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

doors = ["Closed", "Closed", "Closed"]
player_choice = random.randint(0, 2)
car = random.randint(0, 2)
host_opens = random.choice([i for i in range(3) if i != player_choice and i != car])

fig, ax = plt.subplots()
ax.set_title("Monty Hall Simulation")
bars = ax.bar(["Door 1", "Door 2", "Door 3"], [1, 1, 1], color='gray')

def update(frame):
    if frame == 0:
        # Player picks door
        bars[player_choice].set_color('blue')
        ax.set_title("Player picks a door")
    elif frame == 1:
        # Host opens goat
        bars[host_opens].set_color('red')
        ax.set_title("Host opens a goat door")
    elif frame == 2:
        # Show winning door
        bars[car].set_color('green')
        ax.set_title("Car is behind this door!")

ani = FuncAnimation(fig, update, frames=3, repeat=False)
plt.show()