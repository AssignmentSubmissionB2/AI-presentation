DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}


def can_move(block, board, dx, dy):
    """Check if block can move in direction (dx, dy) without collision"""
    rows, cols = len(board), len(board[0])
    
    # Check all cells the block will occupy after moving
    for r in range(block.row, block.row + block.height):
        for c in range(block.col, block.col + block.width):
            nr, nc = r + dx, c + dy
            
            # Check bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                return False
            
            # Check if destination is occupied by another block
            cell_value = board[nr][nc]
            if cell_value != 0 and cell_value != block.id:
                return False
    
    return True


def apply_move(state, block_id, dx, dy):
    """
    Apply move in-place (mutates state).
    More efficient than creating new state for validation.
    """
    block = next(b for b in state.blocks if b.id == block_id)
    
    # Clear old position
    for r in range(block.row, block.row + block.height):
        for c in range(block.col, block.col + block.width):
            state.board[r][c] = 0
    
    # Update position
    block.row += dx
    block.col += dy
    
    # Place in new position
    for r in range(block.row, block.row + block.height):
        for c in range(block.col, block.col + block.width):
            state.board[r][c] = block.id


def undo_move(state, block_id, dx, dy):
    """Undo a move (reverse operation)"""
    apply_move(state, block_id, -dx, -dy)


def get_neighbors(state):
    """
    Generate all valid neighboring states.
    Each neighbor represents a single block move.
    """
    neighbors = []
    
    for block in state.blocks:
        for dir_name, (dx, dy) in DIRECTIONS.items():
            if can_move(block, state.board, dx, dy):
                # Create new state by copying current
                new_state = state.copy()
                new_state.depth = state.depth + 1
                new_state.parent = state
                
                # Apply the move
                apply_move(new_state, block.id, dx, dy)
                new_state.move = f"{block.id} {dir_name}"
                
                neighbors.append(new_state)
    
    return neighbors

