import heapq
from moves import get_neighbors


def a_star(start_state, max_states=100000):
    """
    A* Search with progress monitoring
    """
    counter = 0
    start_h = start_state.get_heuristic()
    heap = [(start_h, counter, start_state)]
    
    g_scores = {start_state: 0}
    
    states_explored = 0
    max_heap_size = 1
    total_branches = 0
    nodes_expanded = 0
    
    print("  Progress: ", end="", flush=True)
    
    while heap:
        max_heap_size = max(max_heap_size, len(heap))
        f_score, _, current = heapq.heappop(heap)
        
        current_g = g_scores.get(current, float('inf'))
        states_explored += 1
        
        # Progress indicator
        if states_explored % 1000 == 0:
            print(f"{states_explored}...", end="", flush=True)
        
        # Safety limit
        if states_explored > max_states:
            print(f"\n   Reached exploration limit ({max_states} states)")
            avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
            return None, states_explored, max_heap_size, avg_branching
        
        if current.is_goal():
            print(f"{states_explored} ")
            avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
            return current, states_explored, max_heap_size, avg_branching
        
        if current_g < current.depth:
            continue
        
        neighbors = get_neighbors(current)
        nodes_expanded += 1
        total_branches += len(neighbors)
        
        for neighbor in neighbors:
            tentative_g = neighbor.depth
            
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                h_score = neighbor.get_heuristic()
                f_score = tentative_g + h_score
                counter += 1
                heapq.heappush(heap, (f_score, counter, neighbor))
    
    print(f"{states_explored} ✗")
    avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
    return None, states_explored, max_heap_size, avg_branching
