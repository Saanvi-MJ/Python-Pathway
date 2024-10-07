from tkinter import *
import random

# Initialising width of the screen 
WIDTH = 500
# Initialising height of the screen 
HEIGHT = 500
# Initialising speed of the snake 
SPEED = 200
# Initialising space of the screen 
SPACE_SIZE = 20
# Initialising body's length of the snake 
BODY_SIZE = 2
# Initialising color of the snake 
SNAKE = "#00FF00"
# Initialising colour of the food 
FOOD = "#FFFFFF"
# Initialising colour of the background 
BACKGROUND = "#000000"
# Color of snake's eye
EYE_COLOR = "#000000"
# Color of the grid lines
GRID_COLOR = "#444444"

#create the snake in game
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

#creating the food

class Food: 

	def __init__(self): 

		x = random.randint(0, 
			(WIDTH // SPACE_SIZE)-1) * SPACE_SIZE 
		y = random.randint(0, 
			(HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE 

		self.coordinates = [x, y] 

		canvas.create_oval(x, y, x + SPACE_SIZE, y +
						SPACE_SIZE, fill=FOOD, 
						tag="food") 

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
	canvas.create_text(canvas.winfo_width()/2, 
					canvas.winfo_height()/2, 
					font=('consolas', 70), 
					text="GAME OVER", 
					fill="white", tag="gameover") 



window = Tk() 
 

score = 0
direction = 'down'
 

label = Label(window, 
			text="Points:{}".format(score), 
			font=('consolas', 20)) 
label.pack() 

canvas = Canvas(window, bg=BACKGROUND, 
				height=HEIGHT, width=WIDTH) 
canvas.pack() 

window.update() 

window_width = window.winfo_width() 
window_height = window.winfo_height() 
screen_width = window.winfo_screenwidth() 
screen_height = window.winfo_screenheight() 

x = int((screen_width/2) - (window_width/2)) 
y = int((screen_height/2) - (window_height/2)) 

window.geometry(f"{window_width}x{window_height}+{x}+{y}") 

window.bind('<Left>', 
			lambda event: change_direction('left')) 
window.bind('<Right>', 
			lambda event: change_direction('right')) 
window.bind('<Up>', 
			lambda event: change_direction('up')) 
window.bind('<Down>', 
			lambda event: change_direction('down')) 

snake = Snake() 
food = Food() 



next_turn(snake, food) 

window.mainloop()
