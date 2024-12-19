import time
import matplotlib.pyplot as plt #type:ignore
import numpy as np #type:ignore
from MINIMAX import *
from MINI_ALPHA import *


def performance_test_with_plots():
    board = create_board()
    for _ in range(10):
        col = np.random.randint(7)  # Random column
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            piece = np.random.choice([1, 2])  # Random piece
            drop_piece(board, row, col, piece)

    print("Testing performance on the following board:")
    print_board(board)

    depths = range(1, 6)  # Depths from 1 to 5
    minimax_times = []
    alpha_beta_times = []
    minimax_scores = []
    alpha_beta_scores = []

    for depth in depths:
        print(f"\nTesting depth {depth}...")

        # minimax performance
        start_time = time.time()
        _, minimax_score = minimax(board, depth=depth, maximizingPlayer=True)
        minimax_time = time.time() - start_time
        minimax_times.append(minimax_time)
        minimax_scores.append(minimax_score)

        # alpha performance
        start_time = time.time()
        _, alpha_beta_score = minimax_ab(board, depth=depth, alpha=-float('inf'), beta=float('inf'), maximizingPlayer=True)
        alpha_beta_time = time.time() - start_time
        alpha_beta_times.append(alpha_beta_time)
        alpha_beta_scores.append(alpha_beta_score)

    # Plotting results
    plt.figure(figsize=(12, 6))

    # Time comparison
    plt.subplot(1, 2, 1)
    plt.plot(depths, minimax_times, label="Minimax Time", marker="o", color="blue")
    plt.plot(depths, alpha_beta_times, label="Alpha-Beta Time", marker="o", color="green")
    plt.title("Runtime Comparison")
    plt.xlabel("Depth")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)

    # Heuristic score comparison
    plt.subplot(1, 2, 2)
    plt.plot(depths, minimax_scores, label="Minimax Score", marker="o", color="red")
    plt.plot(depths, alpha_beta_scores, label="Alpha-Beta Score", marker="o", color="orange")
    plt.title("Heuristic Score Comparison")
    plt.xlabel("Depth")
    plt.ylabel("Heuristic Score")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance_test_with_plots()
