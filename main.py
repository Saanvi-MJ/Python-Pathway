from tkinter import *
import random
import os

# Initializing screen dimensions, speed, snake size, and colors
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE = "#f0ece0"
FOOD = "#FFFFFF"
BACKGROUND = "#000000"
EYE_COLOR = "#000000"
GRID_COLOR = "#444444"
SCORE_FILE = "max_score.txt"  

# Function to load the maximum score from a file
def load_max_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0  

# Function to save the maximum score to a file
def save_max_score(max_score):
    with open(SCORE_FILE, "w") as file:
        file.write(str(max_score))

# Creating the snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE, tag="snake")
            self.squares.append(square)

# Creating the food class
class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y +
                           SPACE_SIZE, fill=FOOD, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    # Create snake's head and add one eye
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE)

    snake.squares.insert(0, square)

    # Add a single eye to the snake's head
    draw_eye(x, y, direction)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score, max_score

        score += 1

        # Update maximum score if the current score exceeds it
        if score > max_score:
            max_score = score
            save_max_score(max_score)  # Save the new high score

        label.config(text="Points: {}".format(score))
        max_score_label.config(text="Max Score: {}".format(max_score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH:
        return True
    elif y < 0 or y >= HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 - 40,
        font=('consolas', 70),
        text="GAME OVER",
        fill="white",
        tag="gameover"
    )

    # Display the final score below the "GAME OVER" message
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 + 40,
        font=('consolas', 30),
        text=f"Your Score is: {score}",
        fill="white",
        tag="score"
    )

    # Clear the points label
    label.config(text="")
    max_score_label.config(text="Max Score: {}".format(max_score))

# Function to draw a single eye on the snake's head
def draw_eye(x, y, direction):
    canvas.delete("eye")

    eye_offset = 5
    eye_size = 3

    if direction == 'up':
        eye_x1, eye_y1 = x + SPACE_SIZE - eye_offset, y + eye_offset
    elif direction == 'down':
        eye_x1, eye_y1 = x + eye_offset, y + SPACE_SIZE - eye_offset
    elif direction == 'left':
        eye_x1, eye_y1 = x + eye_offset, y + eye_offset
    elif direction == 'right':
        eye_x1, eye_y1 = x + SPACE_SIZE - eye_offset, y + eye_offset

    canvas.create_oval(eye_x1, eye_y1, eye_x1 + eye_size, eye_y1 + eye_size, fill=EYE_COLOR, tag="eye")

# Function to draw a grid in the background
def draw_grid():
    for x in range(0, WIDTH, SPACE_SIZE):
        canvas.create_line(x, 0, x, HEIGHT, fill=GRID_COLOR)
    for y in range(0, HEIGHT, SPACE_SIZE):
        canvas.create_line(0, y, WIDTH, y, fill=GRID_COLOR)

window = Tk()
window.title("Welcome to Snake Game")

score = 0
max_score = load_max_score()  # Load max score from file
direction = 'down'

label = Label(window, text="Points: {}".format(score), font=('consolas', 20))
label.pack()

# Add a label to display the maximum score
max_score_label = Label(window, text="Max Score: {}".format(max_score), font=('consolas', 15))
max_score_label.pack()

canvas = Canvas(window, bg=BACKGROUND, height=HEIGHT, width=WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

# Draw the grid before starting the game
draw_grid()

next_turn(snake, food)

window.mainloop()
