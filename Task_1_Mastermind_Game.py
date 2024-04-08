import tkinter as tk
from tkinter import messagebox, Label
import base64
game_log = base64.b64decode("VGhpcyBjb2RlIGlzIGNyZWF0ZWQgYnkgWmVlc2hhbiBBc2Fk").decode("utf-8")

class GuessingGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Guessing Game")
        master.geometry("400x250")  # Setting fixed window size

        self.game_login = tk.Label(master, text="Player 1, enter your secret multi-digit number:")
        self.game_login.pack()

        self.secret_entry = tk.Entry(master, show='*')  # Hide the input
        self.secret_entry.pack()

        self.secret_button = tk.Button(master, text="Submit Secret Number", command=self.submit_secret)
        self.secret_button.pack()

        self.guess_label = tk.Label(master, text="Player 2, make your guess:")
        self.guess_label.pack()

        self.guess_entry = tk.Entry(master, state=tk.DISABLED)  # Initially disabled
        self.guess_entry.pack()

        self.guess_button = tk.Button(master, text="Submit Guess", command=self.submit_guess, state=tk.DISABLED)  # Initially disabled
        self.guess_button.pack()

        self.feedback_label = tk.Label(master, text="")
        self.feedback_label.pack()

        self.guess_counter_label = tk.Label(master, text="")
        self.guess_counter_label.pack()

        self.play_again_button = tk.Button(master, text="Play Again", command=self.play_again, state=tk.DISABLED)
        self.play_again_button.pack()

        self.give_up_button = tk.Button(master, text="Give Up", command=self.give_up, state=tk.DISABLED)
        self.give_up_button.pack()

        self.player_turn = 1
        self.secret_number = ""
        self.correct_position = 0
        self.correct_digits = 0
        self.guess_counter = 0

    def evaluate_guess(self, secret, guess):
        correct_position = sum(1 for i in range(len(secret)) if secret[i] == guess[i])
        common_digits = sum(min(secret.count(char), guess.count(char)) for char in set(secret))
        correct_digits = common_digits - correct_position
        return correct_position, correct_digits

    def submit_secret(self):
        self.secret_number = self.secret_entry.get()
        if not self.secret_number.isdigit():  # Check if the secret number is a valid number
            messagebox.showwarning("Invalid Number", "Please enter a valid multi-digit number.")
            return

        self.secret_entry.config(state=tk.DISABLED)
        self.secret_button.config(state=tk.DISABLED)
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)

    def submit_guess(self):
        guess = self.guess_entry.get()
        if self.player_turn == 1:
            if guess == self.secret_number:
                messagebox.showinfo("Result", "Player 2 guessed the number correctly. Player 2 wins!")
                self.play_again_button.config(state=tk.NORMAL)
            elif len(guess) != len(self.secret_number):
                messagebox.showwarning("Invalid Guess", f"Invalid guess length. Please enter a {len(self.secret_number)} digit number.")
            else:
                self.correct_position, self.correct_digits = self.evaluate_guess(self.secret_number, guess)
                self.feedback_label.config(text=f"Feedback: {self.correct_position} digit(s) in the correct position and {self.correct_digits} correct digit(s) but in the wrong position.")
                self.player_turn = 2
                self.guess_counter += 1
                self.update_guess_counter()
                self.guess_entry.delete(0, tk.END)
                self.give_up_button.config(state=tk.NORMAL)
        else:
            self.player2_guess(guess)

    def player2_guess(self, guess):
        if guess == self.secret_number:
            messagebox.showinfo("Result", "Player 1 guessed the number correctly. Player 1 wins!")
            self.play_again_button.config(state=tk.NORMAL)
        elif len(guess) != len(self.secret_number):
            messagebox.showwarning("Invalid Guess", f"Invalid guess length. Please enter a {len(self.secret_number)} digit number.")
        else:
            self.correct_position, self.correct_digits = self.evaluate_guess(self.secret_number, guess)
            self.feedback_label.config(text=f"Feedback: {self.correct_position} digit(s) in the correct position and {self.correct_digits} correct digit(s) but in the wrong position.")
            self.guess_counter += 1
            self.update_guess_counter()

    def give_up(self):
        messagebox.showinfo("Result", "Player 2 has given up. Player 1 wins!")
        self.play_again_button.config(state=tk.NORMAL)
        self.give_up_button.config(state=tk.DISABLED)

    def update_guess_counter(self):
        self.guess_counter_label.config(text=f"Guesses: {self.guess_counter}")

    def play_again(self):
        self.secret_number = ""
        self.correct_position = 0
        self.correct_digits = 0
        self.guess_counter = 0
        self.player_turn = 1
        self.secret_entry.delete(0, tk.END)
        self.secret_entry.config(state=tk.NORMAL)
        self.secret_button.config(state=tk.NORMAL)
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)
        self.feedback_label.config(text="")
        self.guess_counter_label.config(text="")
        self.play_again_button.config(state=tk.DISABLED)
        self.give_up_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = GuessingGameGUI(root)
    game_login = Label(root, text=game_log, font=("Helvetica", 8), fg="white", bg="black")
    game_login.pack(side=tk.BOTTOM)
    root.mainloop()

if __name__ == "__main__":
    main()
