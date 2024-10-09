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
SCORE_FILE = "max_score.txt"  # File to store the maximum score

# Function to load the maximum score from a file
def load_max_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0  # Default max score if file doesn't exist

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

    global score, max_score

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1

        if score > max_score:
            max_score = score
            save_max_score(max_score)
            max_score_label.config(text="Max Score: {}".format(max_score))

        label.config(text="Points: {}".format(score))

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

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 - 70,
        font=('consolas', 70),
        text="GAME OVER",
        fill="white",
        tag="gameover"
    )

    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 + 40,
        font=('consolas', 25),
        text=f"Your Score: {score}",
        fill="white",
        tag="score",
    )
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 + 5,
        font=('consolas', 25),
        text=f"Maximum Score: {max_score}",
        fill="white",
        tag="score",
    )

    # Clear the points label
    label.config(text="")
    max_score_label.config(text="")

    # If the player beats the maximum score, trigger congratulations and confetti
    if score > max_score and max_score!=0:
        window.after(500, show_congratulations)  # Delay before showing congratulations
        window.after(500, trigger_confetti)      # Start the confetti effect

# Function to trigger a confetti effect with motion
def trigger_confetti():
    confetti_pieces = []

    # Create 100 pieces of confetti at random positions with random colors
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(5, 10)  # Random size for the confetti pieces
        confetti = canvas.create_oval(x, y, x + size, y + size, fill=random_color(), tag="confetti")
        confetti_pieces.append(confetti)

    # Animate the confetti falling downwards
    def move_confetti():
        for confetti in confetti_pieces:
            x1, y1, x2, y2 = canvas.coords(confetti)
            canvas.move(confetti, 0, random.randint(5, 10))  # Move downwards

            # Reset confetti to top if it goes off-screen
            if y2 > HEIGHT:
                canvas.coords(confetti, x1, 0, x2, size)

        # Continue moving the confetti pieces
        window.after(50, move_confetti)

    move_confetti()

# Function to show congratulations message after game over
def show_congratulations():
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 + 100,
        font=('consolas', 17),
        text="Congratulations on setting a \n new high score!",
        anchor='center', 
        fill="yellow",
        tag="congratulations"
    )

# Function to generate random colors for the confetti effect
def random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

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

# Function to display a separate "Get Ready" screen
def show_get_ready_screen():
    canvas.delete(ALL)  # Clear the canvas
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 +70,
        font=('consolas', 50),
        text="Get Ready",
        fill="white",
        tag="get_ready"
    )
    window.after(2000, start_game)  # Start game after 2 seconds
    # canvas.delete(ALL)  # Clear the canvas
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2,
        font=('consolas', 50),
        text="GO",
        fill="white",
        tag="go_lang"
    )
# Function to start the game screen after "Get Ready"
def start_game():
    canvas.delete("get_ready")  # Remove the "Get Ready" message
    draw_grid()  # Draw the grid
    global snake, food
    snake = Snake()  # Initialize the snake
    food = Food()  # Initialize the food
    next_turn(snake, food)  #
# Main Game Setup
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
max_score = load_max_score()

direction = 'down'

label = Label(window, text="Points: {}".format(score), font=('consolas', 15))
label.pack()

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

# Show the "Get Ready" screen first
show_get_ready_screen()

window.mainloop()