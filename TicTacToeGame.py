import tkinter as tk
from tkinter import messagebox
import random
import winsound
import os
import sys
from PIL import Image, ImageTk, ImageEnhance

def get_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

ICON_FILE = get_path("TicTacToe.ico")
WIN_SOUND = get_path("victory.wav")
DRAW_SOUND = get_path("draw.wav")
BG_IMAGE = get_path("bg.png")

game_mode = "PvP" 
current_player = "X"
winner = False
is_thinking = False

def play_sound(result):
    try:
        if result == "win":
            winsound.PlaySound(WIN_SOUND, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif result == "draw":
            winsound.PlaySound(DRAW_SOUND, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except:
        pass

# Visual Effect: Winning Pulse
def flash_win(combo, count=0):
    if winner and count < 10:
        color = "#00FFFF" if count % 2 == 0 else "#32CD32" 
        for index in combo:
            buttons[index].config(bg=color)
        root.after(250, lambda: flash_win(combo, count + 1))

def reset_game():
    global current_player, winner, is_thinking
    current_player = "X"
    winner = False
    is_thinking = False
    status_label.config(text=f"Player {current_player}'s turn", fg="#00FFFF")
    for button in buttons:
        button.config(text="", bg="#333333")

def check_winner_silent():
    win_combinations = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    for combo in win_combinations:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            return buttons[combo[0]]["text"]
    if all(button["text"] != "" for button in buttons):
        return "Tie"
    return None

def check_winner():
    global winner
    res = check_winner_silent()
    if res and res != "Tie":
        winner = True
        play_sound("win")
        win_combinations = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for combo in win_combinations:
            if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
                flash_win(combo)
        if messagebox.askyesno("Victory!", f"Player {res} wins!\n\nPlay again?"):
            reset_game()
        else:
            root.destroy()
        return True
    if res == "Tie":
        winner = True
        play_sound("draw")
        if messagebox.askyesno("Tie!", "It's a draw!\n\nPlay again?"):
            reset_game()
        else:
            root.destroy()
        return True
    return False

def computer_move():
    global current_player, is_thinking
    if winner: 
        is_thinking = False
        return
    
    move_made = False
    for i in range(9):
        if buttons[i]["text"] == "":
            buttons[i]["text"] = "O"
            if check_winner_silent() == "O":
                buttons[i].config(text="O", fg="#FF3131")
                move_made = True
                break
            buttons[i]["text"] = ""
    
    if not move_made:
        for i in range(9):
            if buttons[i]["text"] == "":
                buttons[i]["text"] = "X"
                if check_winner_silent() == "X":
                    buttons[i].config(text="O", fg="#FF3131")
                    move_made = True
                    break
                buttons[i]["text"] = ""
                
    if not move_made:
        if buttons[4]["text"] == "":
            buttons[4].config(text="O", fg="#FF3131")
        else:
            empty = [i for i, b in enumerate(buttons) if b["text"] == ""]
            if empty:
                idx = random.choice(empty)
                buttons[idx].config(text="O", fg="#FF3131")

    is_thinking = False
    if not check_winner():
        current_player = "X"
        status_label.config(text=f"Player {current_player}'s turn", fg="#00FFFF")

def button_click(index):
    global current_player, is_thinking
    if is_thinking or winner or buttons[index]["text"] != "":
        return

    color = "#00FFFF" if current_player == "X" else "#FF3131"
    buttons[index].config(text=current_player, fg=color)
    
    if not check_winner():
        if game_mode == "PvC":
            current_player = "O"
            is_thinking = True
            status_label.config(text="Computer is thinking...", fg="yellow")
            root.after(1000, computer_move)
        else:
            current_player = "O" if current_player == "X" else "X"
            next_color = "#00FFFF" if current_player == "X" else "#FF3131"
            status_label.config(text=f"Player {current_player}'s turn", fg=next_color)

def show_menu():
    menu_frame.tkraise()

def start_game(mode):
    global game_mode
    game_mode = mode
    reset_game()
    game_frame.tkraise()

root = tk.Tk()
root.title("Tic-Tac-Toe Pro")
root.geometry("400x650")
root.configure(bg="black")
root.resizable(True, True) 

if os.path.exists(ICON_FILE):
    try:
        root.iconbitmap(ICON_FILE)
    except:
        pass

bg_photo = None
if os.path.exists(BG_IMAGE):
    try:
        img = Image.open(BG_IMAGE).convert("RGB")
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        img = ImageEnhance.Brightness(img).enhance(0.45)
        bg_photo = ImageTk.PhotoImage(img)
    except:
        pass

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

menu_frame = tk.Frame(root, bg="black")
game_frame = tk.Frame(root, bg="black")

for frame in (menu_frame, game_frame):
    frame.grid(row=0, column=0, sticky="nsew")
    if bg_photo:
        bg_lbl = tk.Label(frame, image=bg_photo, bg="black")
        bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

menu_header = tk.Frame(menu_frame, bg="black")
menu_header.pack(pady=50)
tk.Label(menu_header, text="TIC", font=("Arial", 36, "bold"), fg="red", bg="black").pack(side="left")
tk.Label(menu_header, text=" TAC ", font=("Arial", 36, "bold"), fg="yellow", bg="black").pack(side="left")
tk.Label(menu_header, text="TOE", font=("Arial", 36, "bold"), fg="blue", bg="black").pack(side="left")
tk.Button(menu_frame, text="Player vs Player", font=("Arial", 18), bg="#333333", fg="white", width=20, command=lambda: start_game("PvP")).pack(pady=10)
tk.Button(menu_frame, text="Player vs Computer", font=("Arial", 18), bg="#333333", fg="white", width=20, command=lambda: start_game("PvC")).pack(pady=10)
tk.Label(menu_frame, text="By Yekxy (Shivang)", font=("Verdana", 18, "bold"), fg="orange", bg="black", wraplength=380).pack(side="bottom", pady=20)

for i in range(3):
    game_frame.grid_columnconfigure(i, weight=1)
for i in range(1, 4): 
    game_frame.grid_rowconfigure(i, weight=1)

header = tk.Frame(game_frame, bg="black")
header.grid(row=0, column=0, columnspan=3, pady=10)
tk.Label(header, text="TIC", font=("Arial", 24, "bold"), fg="red", bg="black").pack(side="left")
tk.Label(header, text=" TAC ", font=("Arial", 24, "bold"), fg="orange", bg="black").pack(side="left")
tk.Label(header, text="TOE", font=("Arial", 24, "bold"), fg="blue", bg="black").pack(side="left")

buttons = []
for i in range(9):
    btn = tk.Button(game_frame, text="", font=("Arial", 24, "bold"), bg="#333333", fg="white", activebackground="Grey", command=lambda i=i: button_click(i))
    btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5, sticky="nsew") 
    buttons.append(btn)

status_label = tk.Label(game_frame, text="Player X's turn", font=("Arial", 18), fg="#00FFFF", bg="black")
status_label.grid(row=4, column=0, columnspan=3, pady=10)

ctrls = tk.Frame(game_frame, bg="black")
ctrls.grid(row=5, column=0, columnspan=3, pady=5)
tk.Button(ctrls, text="Restart", font=("Impact", 18), bg="#ffcccc", command=reset_game).pack(side="left", padx=10)
tk.Button(ctrls, text="Main Menu", font=("Impact", 18), bg="#ccffcc", command=show_menu).pack(side="left", padx=10)

footer = tk.Label(game_frame, text="By Yekxy (Shivang)", font=("Verdana", 16, "bold italic"), fg="red", bg="black", wraplength=380)
footer.grid(row=6, column=0, columnspan=3, pady=15)

show_menu()
root.mainloop()