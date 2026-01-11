goal_state = (
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 0
)

def successors(state):
    index = state.index(0)
    r, c = divmod(index, 4)
    result = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 4 and 0 <= nc < 4:
            new_index = nr * 4 + nc
            new_state = list(state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            result.append(tuple(new_state))
    return result

def dfs(state, visited, path):
    if state == goal_state:
        return path + [state]
    visited.add(state)
    for next_state in successors(state):
        if next_state not in visited:
            result = dfs(next_state, visited, path + [state])
            if result is not None:
                return result
    return None

initial_state = (
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 0, 14, 15
)

solution = dfs(initial_state, set(), [])

if solution:
    print("Solution found in", len(solution) - 1, "moves")
else:
    print("No solution found")
