import tkinter as tk


class MainGame:
    def __init__(self, ai_level):
        """Initialize the main game based on the chosen AI difficulty level."""
        self.root = tk.Tk()
        self.root.title(f"Connect 4 - {ai_level} Mode")
        self.ai_algorithm = None
        #ai levels
        try:
            if ai_level == "Heuristic1":
                from HEURISTIC1 import find_best_move_heur1,evaluate_board_score
                self.ai_algorithm = (find_best_move_heur1, evaluate_board_score)
            elif ai_level == "heuristic2":
                from HEURISTIC2 import valid_moves
                self.ai_algorithm = valid_moves
            elif ai_level == "Minimax":
                from MINIMAX import minimax
                self.ai_algorithm = minimax
            elif ai_level == "Minimax_alph-beta":
                from MINI_ALPHA import minimax_ab
                self.ai_algorithm = minimax_ab
            else:
                raise ValueError("Invalid difficulty level!")
        except ImportError as e:
            print(f"Error importing AI module: {e}")
            self.root.destroy()

        # Display AI level (for testing purposes)
        self.label = tk.Label(self.root, text=f"AI Level: {ai_level}", font=("Time New Roman", 16 ,"bold italic"))
        self.label.pack(pady=20)

        # Start Button (Placeholder)
        self.start_button = tk.Button(
            self.root, text="Start Game", font=("Time New Roman", 12,"bold italic"), command=self.play
        )
        self.start_button.pack(pady=10)

    def play(self):
        """Start the Connect 4 gameplay (game logic placeholder)."""
        print(f"Playing Connect 4 with AI difficulty: {self.root.title().split('-')[-1].strip()}")
        print(f"Using AI Algorithm: {self.ai_algorithm}")
        # Placeholder for actual game implementation
        self.label.config(text="Game Started! (Implement your game logic here)")

if __name__ == "__main__":
    # Example for testing the MainGame class directly
    main_game = MainGame("Beginner")
    main_game.root.mainloop()
