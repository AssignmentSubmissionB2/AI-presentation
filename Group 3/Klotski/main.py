from state import State, Block
from bfs import bfs
from astar import a_star
from reconstruct import reconstruct_path
from export_json import export_solution
import time


def create_initial_state():
    """
    Classic Klotski (Hua Rong Dao) puzzle configuration.
    Goal: Move block 1 (2x2 Cao Cao/red block) to the bottom center (row=3, col=1)
    This is the standard configuration with 81-move optimal solution.
    
    Board layout (5 rows x 4 columns):
    [1][1][2][2]   Row 0
    [1][1][2][2]   Row 1
    [3][3][4][4]   Row 2
    [5][6][6][7]   Row 3
    [5][8][_][_]   Row 4 (_=empty)
    """
    start_board = [
        [1, 1, 2, 2],
        [1, 1, 2, 2],
        [3, 3, 4, 4],
        [5, 6, 6, 7],
        [5, 8, 0, 0]
    ]
    
    blocks = [
        Block(1, 0, 0, 2, 2),   # Cao Cao (2x2 red block) - goal block
        Block(2, 0, 2, 1, 2),   # Vertical block (right)
        Block(3, 2, 0, 2, 1),   # Horizontal block
        Block(4, 2, 2, 2, 1),   # Horizontal block
        Block(5, 3, 0, 1, 2),   # Vertical block (left)
        Block(6, 3, 1, 2, 1),   # Horizontal block
        Block(7, 3, 3, 1, 1),   # Small block
        Block(8, 4, 1, 1, 1),   # Small block
    ]
    
    return State(start_board, blocks)


def print_algorithm_header(algorithm):
    """Print algorithm section header"""
    print(f"\n{'=' * 70}")
    print(f"  {algorithm}")
    print(f"{'=' * 70}")


def print_solution_summary(algorithm, moves, states_explored, max_space, 
                          branching_factor, runtime):
    """Print concise solution summary"""
    if algorithm == "BFS":
        time_complex = "O(b^d)"
        space_complex = "O(b^d)"
    elif algorithm == "DFS":
        time_complex = "O(b^m)"
        space_complex = "O(bm)"
    else:  # A*
        time_complex = "O(b^d)"
        space_complex = "O(b^d)"
    
    print(f"\n  Solution Found: {len(moves)} moves")
    print(f"  States Explored: {states_explored:,}")
    print(f"  Max Space Used: {max_space:,} states")
    print(f"  Avg Branching Factor: {branching_factor:.2f}")
    print(f"  Runtime: {runtime:.4f} seconds")
    print(f"  Time Complexity: {time_complex}")
    print(f"  Space Complexity: {space_complex}")


def print_comparison_table(results):
    """Print comparison table of all algorithms"""
    print("\n" + "=" * 85)
    print("  ALGORITHM COMPARISON")
    print("=" * 85)
    
    # Header
    print(f"  {'Algorithm':<12} {'Moves':<8} {'States':<12} {'Space':<10} {'Branch':<10} {'Time (s)':<10}")
    print("  " + "-" * 83)
    
    # Data rows
    for algo, data in results.items():
        if data['goal']:
            print(f"  {algo:<12} {len(data['moves']):<8} {data['states']:<12,} "
                  f"{data['space']:<10,} {data['branching']:<10.2f} {data['runtime']:<10.4f}")
    
    print("=" * 85)
    
    # Analysis
    valid_results = {k: v for k, v in results.items() if v['goal']}
    
    if len(valid_results) > 1:
        print("\nAnalysis:")
        
        best_moves = min(valid_results.items(), key=lambda x: len(x[1]['moves']))
        best_speed = min(valid_results.items(), key=lambda x: x[1]['runtime'])
        best_space = min(valid_results.items(), key=lambda x: x[1]['space'])
        
        print(f"  - Optimal Solution: {best_moves[0]} ({len(best_moves[1]['moves'])} moves)")
        print(f"  - Fastest Runtime:  {best_speed[0]} ({best_speed[1]['runtime']:.4f}s)")
        print(f"  - Space Efficient:  {best_space[0]} ({best_space[1]['space']:,} states)")
        print()


def main():
    """Main solver - runs BFS, DFS, and A* on classic Klotski puzzle"""
    
    print("\n" + "=" * 70)
    print("  KLOTSKI PUZZLE SOLVER")
    print("=" * 70)
    print("  Classic Hua Rong Dao Configuration")
    print("  Goal: Move red block (ID 1) to row 3, column 1")
    print("  Expected optimal solution: 81 moves")
    print("=" * 70 + "\n")
    
    start_state = create_initial_state()
    
    print("Initial Board State:")
    start_state.display()
    
    results = {}
    
    # --------- BFS ---------
    print_algorithm_header("BREADTH-FIRST SEARCH (BFS)")
    print("  Strategy: Explore level-by-level, guarantees shortest path")
    print("  Note: This will find the optimal 81-move solution")
    print("  Running...")
    
    start_time = time.time()
    goal_bfs, states_bfs, space_bfs, branch_bfs = bfs(start_state, max_states=500000)
    runtime_bfs = time.time() - start_time
    
    if goal_bfs:
        states_list_bfs, moves_bfs = reconstruct_path(goal_bfs)
        results['BFS'] = {
            'goal': goal_bfs,
            'moves': moves_bfs,
            'states': states_bfs,
            'space': space_bfs,
            'branching': branch_bfs,
            'runtime': runtime_bfs
        }
        print_solution_summary("BFS", moves_bfs, states_bfs, space_bfs, branch_bfs, runtime_bfs)
        export_solution(states_list_bfs, moves_bfs, "BFS", "bfs_solution.json",
                       runtime=runtime_bfs, states_explored=states_bfs,
                       max_space=space_bfs, branching_factor=branch_bfs)
    else:
        print("\n  No solution found")
    

    # --------- A* ---------
    print_algorithm_header("A* SEARCH (A-STAR)")
    print("  Strategy: Use heuristic to guide search toward goal")
    print("  Note: Should find optimal solution efficiently")
    print("  Running...")
    
    start_time = time.time()
    goal_astar, states_astar, space_astar, branch_astar = a_star(start_state, max_states=500000)
    runtime_astar = time.time() - start_time
    
    if goal_astar:
        states_list_astar, moves_astar = reconstruct_path(goal_astar)
        results['A*'] = {
            'goal': goal_astar,
            'moves': moves_astar,
            'states': states_astar,
            'space': space_astar,
            'branching': branch_astar,
            'runtime': runtime_astar
        }
        print_solution_summary("A*", moves_astar, states_astar, space_astar, branch_astar, runtime_astar)
        export_solution(states_list_astar, moves_astar, "A*", "astar_solution.json",
                       runtime=runtime_astar, states_explored=states_astar,
                       max_space=space_astar, branching_factor=branch_astar)
    else:
        print("\n  No solution found")
    
    # --------- COMPARISON ---------
    if len(results) > 1:
        print_comparison_table(results)
    
    print("\nSolver complete! JSON files generated for visualization.\n")


if __name__ == "__main__":
    main()