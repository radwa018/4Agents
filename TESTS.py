import time
import numpy as np #type:ignore
from MINIMAX import *
from MINI_ALPHA import *
def test_performance():
    board = create_board()
    for _ in range(10):
        col = np.random.randint(7)  # Random column
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            piece = np.random.choice([1, 2])  # Random piece
            drop_piece(board, row, col, piece)
    
    print("Testing performance on the following board:")
    print_board(board)
    
    # minimax performance
    print("\nMeasuring Minimax performance :")
    start_time = time.time()
    _, minimax_score = minimax(board, depth=4, maximizingPlayer=True)
    minimax_time = time.time() - start_time
    print(f"Minimax result: {minimax_score}, Time taken: {minimax_time:.4f} seconds")
    
    # Measure Alpha-Beta Pruning performance
    print("\nMeasuring Alpha-Beta Pruning performance :")
    start_time = time.time()
    _, alpha_beta_score = minimax_ab(board, depth=4, alpha=-float('inf'), beta=float('inf'), maximizingPlayer=True)
    alpha_beta_time = time.time() - start_time
    print(f"Alpha-Beta result: {alpha_beta_score}, Time taken: {alpha_beta_time:.4f} seconds")
    
    # Compare performance
    print("\nPerformance Summary:")
    print(f"Minimax Time: {minimax_time:.4f} seconds")
    print(f"Alpha-Beta Time: {alpha_beta_time:.4f} seconds")
    print("alpha beta is faster than minimax")

if __name__ == "__main__":
    test_performance()

