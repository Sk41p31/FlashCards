from tkinter import *
import pandas as pd
import random
BACKGROUND_COLOR = "#B1DDC6"
flip_timer_ID = None
current_card = None

# ============== DATA SETUP ============== #

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
finally:
    data_dict = data.to_dict(orient="records")


# ============== FLIP CARD ============== #


def flip(eng_word):
    card_canvas.itemconfig(canvas_img, image=english_img)
    card_canvas.itemconfig(language, text="English", fill="white")
    card_canvas.itemconfig(word, text=eng_word, fill="white")


# ============== PICK RANDOM WORD ============== #


def pick_card():
    global flip_timer_ID, current_card
    try:
        card_canvas.after_cancel(flip_timer_ID)
    except ValueError:
        pass
    card_canvas.itemconfig(canvas_img, image=french_img)

    current_card = random.choice(data_dict)
    to_print = current_card["French"]
    card_canvas.itemconfig(word, text=to_print, fill="black")
    card_canvas.itemconfig(language, text="French", fill="black")

    flip_timer_ID = card_canvas.after(3000, flip, current_card["English"])


# ============== PICK RANDOM WORD ============== #


def remove_card():
    global current_card, data_dict
    data_dict.pop(data_dict.index(current_card))

    df = pd.DataFrame(data_dict)
    df.to_csv("data/words_to_learn.csv", index=False)

    pick_card()


# ============== UI SETUP ============== #

window = Tk()
window.title("FlashCards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

card_canvas = Canvas(bg=BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)

french_img = PhotoImage(file="images/card_front.png")
english_img = PhotoImage(file="images/card_back.png")
canvas_img = card_canvas.create_image(400, 263, image=french_img)

language = card_canvas.create_text(400, 150, text="Language", font=("Ariel", 40, "italic"))
word = card_canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))

card_canvas.grid(row=0, column=0, columnspan=2)

btn_wrong_img = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=btn_wrong_img, highlightthickness=0, command=pick_card)
button_wrong.grid(row=1, column=0)

btn_right_img = PhotoImage(file="images/right.png")
button_right = Button(image=btn_right_img, highlightthickness=0, command=remove_card)
button_right.grid(row=1, column=1)

pick_card()

window.mainloop()
