import random

stay_wins = 0
switch_wins = 0

def monty_hall_recursive(trials):
    global stay_wins, switch_wins
    if trials == 0:
        return

    doors = [0, 0, 0]
    car = random.randint(0, 2)
    doors[car] = 1

    choice = random.randint(0, 2)

    host_options = [i for i in range(3) if i != choice and doors[i] == 0]
    host_opens = random.choice(host_options)

    # Stay
    if doors[choice] == 1:
        stay_wins += 1

    # Switch
    switch_choice = next(i for i in range(3) if i != choice and i != host_opens)
    if doors[switch_choice] == 1:
        switch_wins += 1

    monty_hall_recursive(trials - 1)

if __name__ == "__main__":
    trials = 500
    monty_hall_recursive(trials)
    print("Recursive Simulation Results:")
    print(f"Stay wins: {stay_wins} ({stay_wins/trials:.2%})")
    print(f"Switch wins: {switch_wins} ({switch_wins/trials:.2%})")