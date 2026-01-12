def tower_of_hanoi_iterative(n, source, destination, auxiliary):
    total_moves = 2**n - 1
   
    # If number of disks is even, swap destination and auxiliary
    if n % 2 == 0:
        destination, auxiliary = auxiliary, destination

    # Helper function to move between two pegs
    def move_disk(p1, p2, name1, name2):
        if not p1 and not p2: return
        if not p2 or (p1 and p1[-1] < p2[-1]):
            print(f"Move disk {p1[-1]} from {name1} to {name2}")
            p2.append(p1.pop())
        else:
            print(f"Move disk {p2[-1]} from {name2} to {name1}")
            p1.append(p2.pop())

    peg_a, peg_b, peg_c = list(range(n, 0, -1)), [], []

    for i in range(1, total_moves + 1):
        if i % 3 == 1:
            move_disk(peg_a, peg_c, source, destination)
        elif i % 3 == 2:
            move_disk(peg_a, peg_b, source, auxiliary)
        elif i % 3 == 0:
            move_disk(peg_b, peg_c, auxiliary, destination)

n_disks = 3
tower_of_hanoi_iterative(n_disks, 'A', 'C', 'B')