import tkinter as tk
from tkinter import messagebox
import platform

# Dark Theme Colors
BG_COLOR = "#1e1e2e"
FG_COLOR = "#cdd6f4"
PEG_COLOR = "#6c7086"
DISC_COLORS = [
    "#f38ba8", "#fab387", "#f9e2af", "#a6e3a1", "#94e2d5",
    "#89dceb", "#74c7ec", "#89b4fa", "#b4befe", "#cba6f7"
]

class TowerOfHanoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi")
        self.root.geometry("800x600")
        self.root.configure(bg=BG_COLOR)
        
        self.num_discs = 5
        self.pegs = [[], [], []]
        self.moves = []
        self.auto_solve_id = None
        self.speed = 400 # ms
        
        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        # Top Control Frame
        control_frame = tk.Frame(self.root, bg=BG_COLOR)
        control_frame.pack(pady=20)
        
        tk.Label(control_frame, text="Discs:", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 14)).grid(row=0, column=0, padx=10)
        
        self.disc_var = tk.StringVar(value=str(self.num_discs))
        
        # Mac standard tkinter buttons and entries have some quirks with background colors
        # using a basic Entry and Button
        self.disc_entry = tk.Entry(
            control_frame, 
            textvariable=self.disc_var, 
            width=5, 
            font=("Helvetica", 14), 
            justify="center"
        )
        self.disc_entry.grid(row=0, column=1, padx=10)
        
        self.reset_btn = tk.Button(control_frame, text="Reset", command=self.reset_game, font=("Helvetica", 12), width=8)
        self.reset_btn.grid(row=0, column=2, padx=10)
        
        self.next_btn = tk.Button(control_frame, text="Next Step", command=self.next_step, font=("Helvetica", 12), width=10)
        self.next_btn.grid(row=0, column=3, padx=10)
        
        self.auto_btn = tk.Button(control_frame, text="Auto Solve", command=self.toggle_auto_solve, font=("Helvetica", 12), width=10)
        self.auto_btn.grid(row=0, column=4, padx=10)
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self.root, width=700, height=400, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, bg=BG_COLOR, fg=PEG_COLOR, font=("Helvetica", 14)).pack()

    def reset_game(self):
        if self.auto_solve_id:
            self.root.after_cancel(self.auto_solve_id)
            self.auto_solve_id = None
            self.auto_btn.config(text="Auto Solve")
            
        try:
            self.num_discs = int(self.disc_var.get())
            if self.num_discs < 1 or self.num_discs > 15:
                messagebox.showerror("Error", "Please enter a number between 1 and 15")
                self.num_discs = 5
                self.disc_var.set("5")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
            self.num_discs = 5
            self.disc_var.set("5")
            
        self.pegs = [list(range(self.num_discs, 0, -1)), [], []]
        self.moves = self.generate_moves(self.num_discs, 0, 2, 1)
        self.status_var.set("Ready")
        
        self.next_btn.config(state=tk.NORMAL)
        self.auto_btn.config(state=tk.NORMAL)
        
        self.draw()

    def generate_moves(self, n, source, target, auxiliary):
        moves = []
        def hanoi(n, source, target, auxiliary):
            if n > 0:
                hanoi(n - 1, source, auxiliary, target)
                moves.append((source, target))
                hanoi(n - 1, auxiliary, target, source)
        hanoi(n, source, target, auxiliary)
        return moves

    def draw(self):
        self.canvas.delete("all")
        
        # Draw Pegs
        peg_width = 12
        peg_height = 250
        peg_y = 350
        
        for i in range(3):
            x = 150 + i * 200
            # Vertical peg
            self.canvas.create_rectangle(
                x - peg_width/2, peg_y - peg_height, 
                x + peg_width/2, peg_y, 
                fill=PEG_COLOR, outline=""
            )
            # Base
            self.canvas.create_rectangle(
                x - 80, peg_y, 
                x + 80, peg_y + 15, 
                fill=PEG_COLOR, outline=""
            )
            
        # Draw Discs
        disc_height = 20
        max_disc_width = 140
        min_disc_width = 40
        
        for peg_index, peg in enumerate(self.pegs):
            x = 150 + peg_index * 200
            for i, disc in enumerate(peg):
                # Calculate width based on max disc size to keep relative proportions
                width = min_disc_width + (max_disc_width - min_disc_width) * (disc / max(1, self.num_discs))
                y = peg_y - (i * disc_height) - disc_height
                # Pick a color from the palette, loop if necessary
                color = DISC_COLORS[disc % len(DISC_COLORS)]
                
                # Draw disc with rounded appearance (using an oval instead of rectangle)
                self.canvas.create_oval(
                    x - width/2, y, 
                    x + width/2, y + disc_height, 
                    fill=color, outline=BG_COLOR, width=2
                )
                
    def next_step(self):
        if not self.moves:
            self.status_var.set("Solved!")
            self.next_btn.config(state=tk.DISABLED)
            self.auto_btn.config(state=tk.DISABLED)
            if self.auto_solve_id:
                self.root.after_cancel(self.auto_solve_id)
                self.auto_solve_id = None
                self.auto_btn.config(text="Auto Solve")
            return False
            
        source, target = self.moves.pop(0)
        disc = self.pegs[source].pop()
        self.pegs[target].append(disc)
        self.draw()
        self.status_var.set(f"Moved disc from Peg {source + 1} to Peg {target + 1}")
        return True
        
    def toggle_auto_solve(self):
        if self.auto_solve_id:
            # Stop auto solve
            self.root.after_cancel(self.auto_solve_id)
            self.auto_solve_id = None
            self.auto_btn.config(text="Auto Solve")
            self.next_btn.config(state=tk.NORMAL)
        else:
            # Start auto solve
            self.auto_btn.config(text="Stop Auto")
            self.next_btn.config(state=tk.DISABLED)
            self.auto_solve_step()
            
    def auto_solve_step(self):
        if self.next_step():
            self.auto_solve_id = self.root.after(self.speed, self.auto_solve_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoi(root)
    root.mainloop()
