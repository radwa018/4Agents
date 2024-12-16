import tkinter as tk
from MAIN import MainGame  # Import the main class


class Connect4GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4 - Choose Difficulty")

        # Label for difficulty level
        self.label = tk.Label(self.root, text="Choose Difficulty Level:", font=("Time New Roman", 14,"bold italic"))
        self.label.pack(pady=10)

        # Variable to store selected level
        self.level_var = tk.StringVar()
        self.level_var.set("Heuristic1")  # Default level

        # Radio buttons for difficulty levels
        levels = ["Heuristic1", "Heuristic2", "Minimax", "Minimax_alpha-beta"]
        for level in levels:
            tk.Radiobutton(
                self.root, text=level, variable=self.level_var, value=level, font=("Times New Roman", 12,"bold italic")
            ).pack(anchor="w", padx=20)

        # Play button
        self.play_button = tk.Button(
            self.root, text="Play", font=("Times New Roman", 14,"bold italic"), command=self.start_game
        )
        self.play_button.pack(pady=20)

    def start_game(self):
        """Start the main game with the selected difficulty level."""
        difficulty = self.level_var.get()
        self.root.withdraw()  # Hide the difficulty selection window
        main_game = MainGame(difficulty)  # Start the game with the selected difficulty
        main_game.root.mainloop()  # Run the game
        self.root.destroy()  # Close the GUI after the game ends


if __name__ == "__main__":
    intro_gui = Connect4GUI()
    intro_gui.root.mainloop()

