from tkinter import *
import random
import os
from PIL import Image, ImageTk

# Initializing screen dimensions, speed, snake size, and colors
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE = "#75ab22"
FOOD = "#fc5d18"
BACKGROUND = "#010103"
EYE_COLOR = "#000000"
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

# Confetti class to manage the confetti effect
class Confetti:
    def __init__(self):
        self.pieces = []
        for _ in range(100):  # Create 100 confetti pieces
            x = random.randint(0, WIDTH)
            y = random.randint(-HEIGHT, -20)  # Start above the canvas
            color = random_color()
            piece = canvas.create_oval(x, y, x + 5, y + 5, fill=color, outline="")
            self.pieces.append([piece, x, y])  # Store piece ID and its position

    def fall(self):
        for piece in self.pieces:
            canvas.move(piece[0], 0, 2)  # Move down
            piece[2] += 2  # Update Y position

            # Reset the piece if it falls off the bottom of the canvas
            if piece[2] > HEIGHT:
                x = random.randint(0, WIDTH)
                canvas.move(piece[0], x - piece[1], -HEIGHT)  # Move it back to the top
                piece[1] = x  # Update X position

        window.after(30, self.fall)  # Repeat the falling effect

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

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE)

    snake.squares.insert(0, square)

    draw_eye(x, y, direction)

    global score

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
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
    global max_score

    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 - 70,
        font=('consolas', 70),
        text="GAME OVER",
        fill="#fc5d18",
        tag="gameover"
    )

    # Check if the score exceeds max_score and update if necessary
    if score > max_score:
        max_score = score
        save_max_score(max_score)
    
    window.after(2000, display_scores)  # Display scores after 2 seconds

def display_scores():
    canvas.delete(ALL)  # Clear the canvas

    # Display your score
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 - 30,
        font=('consolas', 25),
        text=f"Your Score: {score}",
        fill="white",
        tag="your_score",
    )

    # Display maximum score
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 + 30,
        font=('consolas', 25),
        text=f"Maximum Score: {max_score}",
        fill="white",
        tag="max_score",
    )

    # Check if the player has achieved or exceeded the maximum score
    if score >= max_score:
        # Display congratulations message
        canvas.create_text(
            canvas.winfo_width()/2,
            canvas.winfo_height()/2 + 120,
            font=('consolas', 20),
            text="Congratulations on setting \n a new high score!",
            fill="#bcd70c",
            tag="congratulations"
        )

        # Trigger confetti effect
        confetti = Confetti()
        confetti.fall()

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

# Function to display a separate "Get Ready" screen
def show_get_ready_screen():
    canvas.delete(ALL)  # Clear the canvas

    # Display "Get Ready" text
    canvas.create_text(
        canvas.winfo_width()/2 -5,
        canvas.winfo_height()/2 + 70,
        font=('consolas', 50),
        text="Get Ready",
        fill="#bcd70c",
        tag="get_ready"
    )

    # Load the logo image using Pillow, resize it, and convert it to Tkinter format
    original_logo = Image.open("snakelogo.png")
    resized_logo = original_logo.resize((120, 120))  # Resize the image to 100x100 pixels
    logo_image = ImageTk.PhotoImage(resized_logo)

    # Display the resized logo image
    canvas.create_image(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2,
        image=logo_image,
        anchor=CENTER,
        tag="logo_image"
    )

    # Keep the image reference to avoid garbage collection
    canvas.image = logo_image
    window.after(2000, start_game)

# Function to start the game screen after "Get Ready"
def start_game():
    canvas.delete("get_ready")  # Remove the "Get Ready" message
    global snake, food
    snake = Snake()  # Initialize the snake
    food = Food()  # Initialize the food
    next_turn(snake, food)  

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
