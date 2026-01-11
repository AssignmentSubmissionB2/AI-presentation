class Block:
    """Represents a block in the Red Donkey puzzle"""
    __slots__ = ['id', 'row', 'col', 'width', 'height']  # Memory optimization
    
    def __init__(self, id, row, col, width, height):
        self.id = id
        self.row = row
        self.col = col
        self.width = width
        self.height = height
    
    def __repr__(self):
        return f"Block({self.id}, r={self.row}, c={self.col}, {self.width}x{self.height})"


class State:
    """Represents a board state in the puzzle"""
    __slots__ = ['board', 'blocks', 'parent', 'move', 'depth', '_hash']
    
    def __init__(self, board, blocks, parent=None, move=None, depth=0):
        self.board = board
        self.blocks = blocks
        self.parent = parent
        self.move = move
        self.depth = depth
        self._hash = None  # Cache hash for efficiency
    
    def __eq__(self, other):
        """States are equal if their boards are identical"""
        if not isinstance(other, State):
            return False
        return self.board == other.board
    
    def __hash__(self):
        """Hash based on board configuration - cached for efficiency"""
        if self._hash is None:
            self._hash = hash(tuple(tuple(row) for row in self.board))
        return self._hash
    
    def copy(self):
        """Create a deep copy of the state"""
        new_board = [row[:] for row in self.board]
        new_blocks = [Block(b.id, b.row, b.col, b.width, b.height) for b in self.blocks]
        return State(new_board, new_blocks, self.parent, self.move, self.depth)
    
    def is_goal(self):
        """Check if red block (id=1) reached the goal: row 3, col 1"""
        red_block = next((b for b in self.blocks if b.id == 1), None)
        return red_block and red_block.row == 3 and red_block.col == 1
    
    def display(self):
        """Pretty print the board state"""
        for row in self.board:
            print(' '.join(f'{cell:2}' for cell in row))
        print()
    
    def get_heuristic(self):
        """
        Heuristic for A*: Manhattan distance + blocking penalty.
        Lower is better - guides search toward goal.
        """
        red_block = next((b for b in self.blocks if b.id == 1), None)
        if not red_block:
            return float('inf')
        
        # Goal: row 3, col 1
        goal_row, goal_col = 3, 1
        
        # Manhattan distance of red block to goal
        distance = abs(red_block.row - goal_row) + abs(red_block.col - goal_col)
        
        # Penalty for blocks blocking the path
        blocking_penalty = 0
        for b in self.blocks:
            if b.id != 1:
                # Check if block is between red block and goal
                if b.row >= red_block.row + red_block.height:
                    if b.col < red_block.col + red_block.width and b.col + b.width > red_block.col:
                        blocking_penalty += 1
        
        return distance + blocking_penalty * 0.5