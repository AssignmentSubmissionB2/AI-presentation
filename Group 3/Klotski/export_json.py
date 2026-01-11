import json


def export_solution(states, moves, algorithm, filename, runtime=None, 
                   states_explored=None, max_space=None, branching_factor=None):
    """Export solution to JSON for visualization"""
    
    # Calculate complexity notation
    if algorithm == "BFS":
        time_complex = "O(b^d)"
        space_complex = "O(b^d)"
    elif algorithm == "A*":
        time_complex = "O(b^d)"
        space_complex = "O(b^d)"
    else:
        time_complex = "O(n)"
        space_complex = "O(n)"
    
    data = {
        "algorithm": algorithm,
        "num_moves": len(moves),
        "moves": moves,
        "runtime": round(runtime, 4) if runtime else None,
        "states_explored": states_explored,
        "max_space_used": max_space,
        "branching_factor": round(branching_factor, 2) if branching_factor else None,
        "time_complexity": time_complex,
        "space_complexity": space_complex,
        "states": []
    }
    
    # Serialize each state's blocks
    for state in states:
        state_blocks = []
        for b in state.blocks:
            state_blocks.append({
                "id": b.id,
                "row": b.row,
                "col": b.col,
                "width": b.width,
                "height": b.height
            })
        data["states"].append(state_blocks)
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Exported to {filename}")
