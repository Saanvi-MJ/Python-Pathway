from tkinter import *
import random
import os
from PIL import Image, ImageTk

# Initializing screen dimensions, speed, snake size, and colors
WIDTH = 100
HEIGHT = 100
SPACE_SIZE = 20
BODY_SIZE = 3
SNAKE = "#75ab22"
FOOD = "#fc5d18"
BACKGROUND = "#010103"
EYE_COLOR = "#000000"
SCORE_FILE = "max_score.txt"  # File to store the maximum score

# Default speed (in milliseconds)
SPEED = 170  # Will be updated based on difficulty selection

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

    global score, max_score

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Points: {}".format(score))

        # Update max score label if a new high score is achieved
        if score > max_score:
            max_score = score
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
        canvas.winfo_height()/2 - 20,
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
        canvas.winfo_height()/2 - 90,
        font=('consolas', 25),
        text=f"Your Score: {score}",
        fill="#0193e9",
        tag="your_score",
    )

    # Display maximum score
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 - 30,
        font=('consolas', 25),
        text=f"Maximum Score: {max_score}",
        fill="#0193e9",
        tag="max_score",
    )

    # Check if the player has achieved or exceeded the maximum score
    if score >= max_score and max_score!=0:
        # Display congratulations message
        canvas.create_text(
            canvas.winfo_width()/2,
            canvas.winfo_height()/2 -220,
            font=('consolas', 20),
            text="Congratulations on setting \n a new high score!",
            fill="#75ab22",
            tag="congratulations"
        )

        # Trigger confetti effect 
        confetti = Confetti()
        confetti.fall()

    # Add a "Play Again" button
    play_again_button = Button(window, text="Play Again", font=('consolas', 20),bg="#fc5d18",fg="white", command=restart_game)
    play_again_button_window = canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 120, window=play_again_button)

# Function to restart the game
def restart_game():
    global score
    score = 0
    label.config(text="Points: {}".format(score))
    canvas.delete(ALL)  # Clear the canvas
    show_get_ready_screen()  # Show the "Get Ready" screen
    
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
# Function to display a separate "Get Ready" screen
def show_get_ready_screen():
    canvas.delete(ALL)  # Clear the canvas

    # Display the "Get Ready" text
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 - 200,
        font=('consolas', 50),
        text="Python Pathway",
        fill="#fc5d18",
        tag="get_ready"
    )

    # Load and display the logo
    original_logo = Image.open("snakelogo.png")
    resized_logo = original_logo.resize((200, 200))
    logo = ImageTk.PhotoImage(resized_logo)

    # Display the logo at the center of the canvas
    canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2 - 90, image=logo)

    # Keep a reference to the logo image
    canvas.logo_image = logo

    # Add a "Start Game" button below the "Get Ready" text
    start_button = Button(window, text="Start Game", font=('consolas', 20), bg="#75ab22", fg="white", command=start_game)
    start_button_window = canvas.create_window(canvas.winfo_width()/2 - 120, canvas.winfo_height()/2 + 10, window=start_button)

    # Add a "Leaderboard" button beside the "Start Game" button
    leaderboard_button = Button(window, text="Leaderboard", font=('consolas', 20), bg="#0193e9", fg="white", command=show_leaderboard)
    leaderboard_button_window = canvas.create_window(canvas.winfo_width()/2 + 130, canvas.winfo_height()/2 + 10, window=leaderboard_button)

    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 + 100,
        font=('consolas', 20),
        text="Difficulty Level",
        fill="#0193e9",
        tag="difficulty_level"
    )

    difficulty = StringVar(window)
    difficulty.set("Select")  # Default selection

    difficulty_dropdown = OptionMenu(window, difficulty, "Easy", "Medium", "Hard")
    difficulty_dropdown.config(font=('consolas', 15), bg="#0193e9", fg="white")  # Set background and foreground colors
    difficulty_dropdown_window = canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 150, window=difficulty_dropdown)

    def start_game_with_difficulty():
        global SPEED
        difficulty_level = difficulty.get()

        if difficulty_level == "Easy":
            SPEED = 300  # Slower speed for easy mode
        elif difficulty_level == "Medium":
            SPEED = 170  # Default speed for medium mode
        else:
            SPEED = 70  # Faster speed for hard mode

        start_game()

    # Update the Start button command to include difficulty selection
    start_button.config(command=start_game_with_difficulty)

# Function to show the leaderboard
def show_leaderboard():
    canvas.delete(ALL)
    
    # Display leaderboard message
    canvas.create_text(
        canvas.winfo_width()/2,
        canvas.winfo_height()/2 - 50,
        font=('consolas', 50),
        text="Leaderboard Coming Soon!",
        fill="#0193e9",
        tag="leaderboard"
    )

    # Add a "Back" button to return to the initial screen
    back_button = Button(window, text="Back", font=('consolas', 20), bg="#fc5d18", fg="white", command=show_get_ready_screen)
    back_button_window = canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 50, window=back_button)


def start_game():
    global snake, food, direction, score, max_score

    # Load the max score from the file
    max_score = load_max_score()

    direction = 'down'
    score = 0

    label.config(text="Points: {}".format(score))
    max_score_label.config(text="Max Score: {}".format(max_score))

    canvas.delete(ALL)

    snake = Snake()
    food = Food()

    next_turn(snake, food)

# Function to resize the canvas based on the window size
def resize_canvas(event):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = event.width, event.height
    canvas.config(width=WIDTH, height=HEIGHT)

# Main Window Initialization
window = Tk()
window.title("Snake Game")

score = 0  # Initialize score
max_score = load_max_score()  # Load the maximum score

label = Label(window, text="Points: {}".format(score), font=('consolas', 10))
label.pack()

max_score_label = Label(window, text="Max Score: {}".format(max_score), font=('consolas', 10))
max_score_label.pack()

canvas = Canvas(window, bg=BACKGROUND, height=HEIGHT, width=WIDTH)
canvas.pack(fill=BOTH, expand=True)

# Bind the window resize event to adjust canvas size
canvas.bind("<Configure>", resize_canvas)

window.update()

# Center the game window on the screen
x = (window.winfo_screenwidth() // 2) - (WIDTH // 2)
y = (window.winfo_screenheight() // 2) - (HEIGHT // 2)
window.geometry(f"{WIDTH}x{HEIGHT+50}+{x}+{y}")

# Display the "Get Ready" screen with difficulty selection
show_get_ready_screen()

# Bind the arrow keys to change direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.mainloop()             