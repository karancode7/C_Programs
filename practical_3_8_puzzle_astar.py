import heapq
import sys

class PuzzleState:
    def __init__(self, board, goal_board, g_cost=0, parent=None, move=""):
        self.board = board          
        self.goal_board = goal_board 
        self.g_cost = g_cost        
        self.parent = parent        
        self.move = move            
        self.h_cost = self.calculate_manhattan() 
        self.f_cost = self.g_cost + self.h_cost  

    def calculate_manhattan(self):
        distance = 0
        for i, val in enumerate(self.board):  # i= position & val = number
            if val != 0:
                target_idx = self.goal_board.index(val)
                curr_row, curr_col = divmod(i, 3)
                target_row, target_col = divmod(target_idx, 3)
                distance += abs(curr_row - target_row) + abs(curr_col - target_col)
        return distance

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def get_neighbors(state):
    neighbors = []
    board = list(state.board)
    blank_idx = board.index(0)
    row, col = divmod(blank_idx, 3)

    moves = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]

    for dr, dc, move_name in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_board = board[:]
            new_board[blank_idx], new_board[new_idx] = new_board[new_idx], new_board[blank_idx]
            neighbors.append(PuzzleState(tuple(new_board), state.goal_board, state.g_cost + 1, state, move_name))
            
    return neighbors

def count_inversions(board_tuple):
    arr = [x for x in board_tuple if x != 0]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions

def is_solvable(start, goal):
    return (count_inversions(start) % 2) == (count_inversions(goal) % 2)

def solve_a_star(start_board, goal_board):
    if not is_solvable(start_board, goal_board):
        return "UNSOLVABLE"

    start_state = PuzzleState(tuple(start_board), tuple(goal_board))
    open_list = []
    heapq.heappush(open_list, start_state)
    visited = {} 

    while open_list:
        current_state = heapq.heappop(open_list)

        if current_state.board == goal_board:
            path = []
            node = current_state
            while node.parent is not None:
                path.append((node.move, list(node.board)))
                node = node.parent
            return path[::-1] 

        if current_state.board in visited and visited[current_state.board] <= current_state.g_cost:
            continue
        visited[current_state.board] = current_state.g_cost

        for neighbor in get_neighbors(current_state):
            if neighbor.board not in visited or neighbor.g_cost < visited[neighbor.board]:
                heapq.heappush(open_list, neighbor)

    return None 

def print_board(board):
    """Renders the board inside a clean terminal grid layout"""
    print("")
    for i in range(3):
        row_str = "│"
        for j in range(3):
            val = board[i * 3 + j]
            tile = " █ " if val == 0 else f" {val} "
            row_str += f"{tile}│"
        print(row_str)
        if i < 2:
            print("")
    print("")

def get_row_wise_input(prompt_title):
    """Gets row-wise inputs using the precise format from your reference image"""
    print(f"\n{prompt_title}")
    print("Enter the puzzle row-wise (use 0 for blank).")
    while True:
        board = []
        try:
            for r in range(1, 4):
                row_input = input(f"Row {r}: ").strip().split()
                if len(row_input) != 3:
                    raise ValueError(f"Row {r} must contain exactly 3 numbers.")
                board.extend([int(x) for x in row_input])
            
            if sorted(board) != list(range(9)):
                raise ValueError("The full board must contain unique numbers from 0 to 8.")
            return tuple(board)
        except ValueError as e:
            print(f"Invalid input: {e} Please re-enter the full puzzle state.\n")

# --- Main Interface Loop ---
if __name__ == "__main__":
    # Standard target layout sequence
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    
    while True:
        print("\n1. Automatic Example")
        print("2. User Input")
        print("3. Exit")
        
        choice = input("Enter Choice : ").strip()
        
        if choice == '1':
            # Predefined standard state
            initial_state = (2, 8, 3, 1, 6, 4, 7, 0, 5)
            print("\nUsing Automatic Initial State:")
            print_board(initial_state)
            break
            
        elif choice == '2':
            initial_state = get_row_wise_input("--- INITIAL STATE ---")
            # Ask if the user wants custom goal or default goal configuration
            use_default_goal = input("Use standard goal state (1 2 3 4 5 6 7 8 0)? [y/n]: ").strip().lower()
            if use_default_goal != 'n':
                goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
            else:
                goal_state = get_row_wise_input("--- TARGET GOAL STATE ---")
            break
            
        elif choice == '3':
            print("Exiting program.")
            sys.exit()
        else:
            print("Invalid Choice! Please enter 1, 2, or 3.")

    # Execute and output grid sequence results
    print("\n Running A* Search Solver...\n")
    solution_path = solve_a_star(initial_state, goal_state)
    
    if solution_path == "UNSOLVABLE":
        print(" This specific puzzle layout state configuration is mathematically UNSOLVABLE!")
    elif solution_path:
        print(f" Success! Goal reached in {len(solution_path)} steps:\n")
        print("Initial State Layout:")
        print_board(initial_state)
        
        for step, (move, board) in enumerate(solution_path, 1):
            print(f"Step {step}: Moved Blank [ {move} ]")
            print_board(board)



        print(f"Total Number of Moves: {len(solution_path)}")
    else:
        print(" Could not find a valid execution path.")

# Propose next steps to enhance implementation
if __name__ == "__main__":
    pass # Hook point for follow up query execution
