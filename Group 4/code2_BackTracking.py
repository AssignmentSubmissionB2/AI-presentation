#code2_BackTracking
import time

letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
used_digits = [False] * 10
assignment = {}

start_time = None

def is_valid_partial():
    # Early constraint: Must be 1 (known property)
    if 'M' in assignment and assignment['M'] != 1:
        return False
    
    #Leading letters cannot be zero
    if assignment.get('S', 1) == 0:
        return False
    if assignment.get('M', 1) == 0:
        return False
    
    return True
def solve(index):
    global start_time

    if index == len(letters):
        send = (
            assignment['S'] * 1000 +
            assignment['E'] * 100 +
            assignment['N'] * 10 +
            assignment['D']
        )
        more = (
            assignment['M'] * 1000 +
            assignment['O'] * 100 +
            assignment['R'] * 10 +
            assignment['E']
        )
        money = (
            assignment['M'] * 10000 +
            assignment['O'] * 1000 +
            assignment['N'] * 100 +
            assignment['E'] * 10 +
            assignment['Y']
        )

        return send + more == money
    
    letter = letters[index]

    for digit in range(10):
        if not used_digits[digit]:
            assignment[letter] = digit
            used_digits[digit] = True

            if is_valid_partial():
                if solve(index + 1):
                    return True
                
                used_digits[digit] = False
                del assignment[letter]

    return False

def backtracking():
    global start_time
    start_time = time.time()
    solve(0)
    end_time = time.time()
    print("Backtracking Solution:", assignment)
    print("Time Taken:", end_time - start_time)

backtracking()                