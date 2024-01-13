from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

flip_timer = None
to_learn = {}
current_card = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ---------------------------- Generate Random Card ------------------------------- #


def next_card():
    global current_card, flip_timer
    if flip_timer is not None:
        # Cancelling previous timer
        window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    french_word = current_card["French"]
    english_word = current_card["English"]
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=french_word, fill="black")
    flip_timer = window.after(3000, flip_card, english_word)


# ---------------------------- Remove known word from list ------------------------ #

def correct_card():
    to_learn.remove(current_card)
    print(f"removing {current_card}")
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("./data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- Flip card to English ------------------------------- #


def flip_card(word):
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=word, fill="white")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Row 0
canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Row 1
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_btn.grid(row=1, column=0)

right_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, command=correct_card)
right_btn.grid(row=1, column=1)

next_card()

window.mainloop()
