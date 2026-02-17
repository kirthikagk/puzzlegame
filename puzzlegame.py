import tkinter as tk
from tkinter import messagebox
import random
import time

class SlidingPuzzle(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧩 Sliding Puzzle Game")
        self.configure(bg="#0A0F1E")
        self.geometry("500x550")
        self.resizable(False, False)

        # Puzzle state
        self.tiles = list(range(1, 16)) + [None]
        random.shuffle(self.tiles)

        self.buttons = []
        self.moves = 0
        self.start_time = None
        self.timer_running = False

        # UI setup
        self.create_board()
        self.create_info_panel()

    def create_board(self):
        self.frame = tk.Frame(self, bg="#0A0F1E")
        self.frame.pack(pady=20)

        for i in range(16):
            value = self.tiles[i]
            btn = tk.Button(
                self.frame,
                text=str(value) if value else "",
                font=("Consolas", 20, "bold"),
                width=4,
                height=2,
                bg="#121826",
                fg="#E6E6E6",
                relief="ridge",
                command=lambda i=i: self.move_tile(i)
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.buttons.append(btn)

    def create_info_panel(self):
        panel = tk.Frame(self, bg="#0A0F1E")
        panel.pack(pady=10)

        self.move_label = tk.Label(panel, text="Moves: 0", font=("Segoe UI", 14, "bold"), fg="#FF4081", bg="#0A0F1E")
        self.move_label.grid(row=0, column=0, padx=20)

        self.timer_label = tk.Label(panel, text="Time: 0s", font=("Segoe UI", 14, "bold"), fg="#00E676", bg="#0A0F1E")
        self.timer_label.grid(row=0, column=1, padx=20)

        shuffle_btn = tk.Button(panel, text="🔄 Shuffle", font=("Segoe UI", 12, "bold"),
                                bg="#FF1744", fg="white", command=self.shuffle)
        shuffle_btn.grid(row=0, column=2, padx=20)

    def move_tile(self, index):
        empty_index = self.tiles.index(None)
        if (abs(empty_index - index) == 1 and empty_index//4 == index//4) or \
           (abs(empty_index - index) == 4):
            # Swap tiles
            self.tiles[empty_index], self.tiles[index] = self.tiles[index], self.tiles[empty_index]
            self.update_board()

            self.moves += 1
            self.move_label.config(text=f"Moves: {self.moves}")

            if not self.timer_running:
                self.start_time = time.time()
                self.timer_running = True
                self.update_timer()

            if self.is_solved():
                elapsed = int(time.time() - self.start_time)
                messagebox.showinfo("🎉 Congratulations!",
                                    f"You solved the puzzle!\nMoves: {self.moves}\nTime: {elapsed}s")
                self.timer_running = False

    def update_board(self):
        for i in range(16):
            value = self.tiles[i]
            self.buttons[i].config(text=str(value) if value else "")

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.after(1000, self.update_timer)

    def shuffle(self):
        random.shuffle(self.tiles)
        self.update_board()
        self.moves = 0
        self.move_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 0s")
        self.timer_running = False

    def is_solved(self):
        return self.tiles == list(range(1, 16)) + [None]


if __name__ == "__main__":
    game = SlidingPuzzle()
    game.mainloop()
