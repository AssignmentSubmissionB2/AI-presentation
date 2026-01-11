def reconstruct_path(goal_state):
    """
    Reconstruct solution path from goal to start.
    Returns list of states and moves in correct order.
    """
    if goal_state is None:
        return [], []
    
    states = []
    moves = []
    current = goal_state
    
    # Trace back from goal to start
    while current is not None:
        states.append(current)
        if current.move is not None:
            moves.append(current.move)
        current = current.parent
    
    # Reverse to get start -> goal order
    states.reverse()
    moves.reverse()
    
    return states, moves

