import tkinter as tk
import random
import os


WIDTH = 400
HEIGHT = 500
FRUIT_SIZE = 30
BASKET_WIDTH = 80
SPEED = 300

score = 0
lives = 3
highscore = 0
retry_button = None


if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())



def move_left(event):
    x = canvas.coords(basket)[0]
    if x > 0:
        canvas.move(basket, -20, 0)

def move_right(event):
    x = canvas.coords(basket)[2]
    if x < WIDTH:
        canvas.move(basket, 20, 0)

def drop_fruit():
    if lives <= 0:
        return

    x = random.randint(0, WIDTH - FRUIT_SIZE)
    fruit = canvas.create_oval(x, 0, x + FRUIT_SIZE, FRUIT_SIZE, fill=random.choice(["red", "yellow", "green", "orange"]))
    move_fruit(fruit)

def move_fruit(fruit):
    def loop():
        nonlocal fruit
        if lives <= 0:
            canvas.delete(fruit)
            return

        coords = canvas.coords(fruit)
        if coords:
            if coords[3] >= HEIGHT - 30:
                basket_coords = canvas.coords(basket)
                if coords[0] > basket_coords[0] and coords[2] < basket_coords[2]:
                    hit_fruit(fruit)
                else:
                    miss_fruit(fruit)
            else:
                canvas.move(fruit, 0, 10)
                canvas.after(50, loop)
    loop()

def hit_fruit(fruit):
    global score
    canvas.delete(fruit)
    score += 1
    score_label.config(text=f"Score: {score}")
    if score > highscore:
        update_highscore(score)
    canvas.after(SPEED, drop_fruit)

def miss_fruit(fruit):
    global lives
    canvas.delete(fruit)
    lives -= 1
    lives_label.config(text=f"Lives: {lives}")
    if lives <= 0:
        game_over()
    else:
        canvas.after(SPEED, drop_fruit)

def update_highscore(new_score):
    global highscore
    highscore = new_score
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))
    highscore_label.config(text=f"High Score: {highscore}")

def game_over():
    global retry_button
    canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over!", fill="black", font=("Comic Sans MS", 24, "bold"))
    canvas.create_text(WIDTH//2, HEIGHT//2 + 30, text=f"Final Score: {score}", fill="black", font=("Comic Sans MS", 14))

    retry_button = tk.Button(root, text="🔁 Retry", font=("Comic Sans MS", 12), bg="orange", command=retry_game)
    retry_button.place(x=WIDTH//2 - 40, y=HEIGHT//2 + 60)

def retry_game():
    global score, lives, retry_button, basket
    score = 0
    lives = 3
    score_label.config(text=f"Score: {score}")
    lives_label.config(text=f"Lives: {lives}")
    canvas.delete("all")

    
    basket = canvas.create_rectangle(WIDTH//2 - BASKET_WIDTH//2, HEIGHT - 30,
                                     WIDTH//2 + BASKET_WIDTH//2, HEIGHT - 10, fill="brown")

    if retry_button:
        retry_button.destroy()
        retry_button = None

    canvas.after(1000, drop_fruit)



root = tk.Tk()
root.title("🍓 Catch the Fruit!")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
canvas.pack()

basket = canvas.create_rectangle(WIDTH//2 - BASKET_WIDTH//2, HEIGHT - 30,
                                 WIDTH//2 + BASKET_WIDTH//2, HEIGHT - 10, fill="brown")

score_label = tk.Label(root, text=f"Score: {score}", font=("Comic Sans MS", 12), bg="lightblue")
score_label.place(x=10, y=10)

lives_label = tk.Label(root, text=f"Lives: {lives}", font=("Comic Sans MS", 12), bg="lightblue")
lives_label.place(x=150, y=10)

highscore_label = tk.Label(root, text=f"High Score: {highscore}", font=("Comic Sans MS", 12), bg="lightblue")
highscore_label.place(x=280, y=10)


root.bind("<Left>", move_left)
root.bind("<Right>", move_right)


canvas.after(1000, drop_fruit)
root.mainloop()
