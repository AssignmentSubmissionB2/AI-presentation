import random

def monty_hall_iterative(trials=10000):
    stay_wins = 0
    switch_wins = 0

    for _ in range(trials):
        doors = [0, 0, 0]
        car = random.randint(0, 2)
        doors[car] = 1

        choice = random.randint(0, 2)


        host_options = [i for i in range(3) if i != choice and doors[i] == 0]
        host_opens = random.choice(host_options)


        if doors[choice] == 1:
            stay_wins += 1

    
        switch_choice = next(i for i in range(3) if i != choice and i != host_opens)
        if doors[switch_choice] == 1:
            switch_wins += 1

    print("Iterative Simulation Results:")

    print(f"Stay wins: {stay_wins} ({stay_wins/trials:.2%})")

    print(f"Switch wins: {switch_wins} ({switch_wins/trials:.2%})")

if __name__ == "__main__":
    monty_hall_iterative()