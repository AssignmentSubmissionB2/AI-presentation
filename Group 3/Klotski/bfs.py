from collections import deque
from moves import get_neighbors


def bfs(start_state, max_states=200000):
    """
    Breadth-First Search with progress monitoring and safety limits
    """
    queue = deque([start_state])
    visited = {start_state}
    
    states_explored = 0
    max_queue_size = 1
    total_branches = 0
    nodes_expanded = 0
    
    print("  Progress: ", end="", flush=True)
    
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        
        current = queue.popleft()
        states_explored += 1
        
        # Progress indicator every 1000 states
        if states_explored % 1000 == 0:
            print(f"{states_explored}...", end="", flush=True)
        
        # Safety limit to prevent infinite loops
        if states_explored > max_states:
            print(f"\n  ⚠️  Reached exploration limit ({max_states} states)")
            print(f"  ⚠️  No solution found within limit")
            avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
            return None, states_explored, max_queue_size, avg_branching
        
        # Check if goal reached
        if current.is_goal():
            print(f"{states_explored} ✓")
            avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
            return current, states_explored, max_queue_size, avg_branching
        
        # Generate neighbors
        neighbors = get_neighbors(current)
        nodes_expanded += 1
        total_branches += len(neighbors)
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    # No solution found
    print(f"{states_explored} ✗")
    avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
    return None, states_explored, max_queue_size, avg_branching
