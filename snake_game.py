# Snake Game (เกมงู) ด้วย Tkinter
import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game (งู)")
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.direction = 'Right'
        self.running = True
        self.score = 0
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.place_food()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        self.root.bind('<KeyPress>', self.on_key_press)
        self.update()

    def place_food(self):
        while True:
            x = random.randrange(0, self.width, self.cell_size)
            y = random.randrange(0, self.height, self.cell_size)
            if (x, y) not in self.snake:
                return (x, y)

    def on_key_press(self, event):
        key = event.keysym
        if key in ['Up', 'Down', 'Left', 'Right']:
            # Prevent snake from reversing
            opposites = {'Up':'Down', 'Down':'Up', 'Left':'Right', 'Right':'Left'}
            if opposites.get(key) != self.direction:
                self.direction = key

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Up':
            new_head = (head_x, head_y - self.cell_size)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + self.cell_size)
        elif self.direction == 'Left':
            new_head = (head_x - self.cell_size, head_y)
        else:
            new_head = (head_x + self.cell_size, head_y)
        self.snake = [new_head] + self.snake[:-1]

    def grow_snake(self):
        self.snake.append(self.snake[-1])

    def check_collisions(self):
        head = self.snake[0]
        # Wall collision
        if not (0 <= head[0] < self.width and 0 <= head[1] < self.height):
            return True
        # Self collision
        if head in self.snake[1:]:
            return True
        return False

    def update(self):
        if not self.running:
            return
        self.move_snake()
        if self.snake[0] == self.food:
            self.grow_snake()
            self.food = self.place_food()
            self.score += 1
        if self.check_collisions():
            self.running = False
            self.canvas.create_text(self.width//2, self.height//2, fill='red', font=('Arial', 24), text='Game Over')
            return
        self.draw()
        self.root.after(100, self.update)

    def draw(self):
        self.canvas.delete('all')
        # Draw snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+self.cell_size, y+self.cell_size, fill='green', outline='')
        # Draw food
        fx, fy = self.food
        self.canvas.create_oval(fx, fy, fx+self.cell_size, fy+self.cell_size, fill='red', outline='')
        # Draw score
        self.canvas.create_text(40, 10, fill='white', font=('Arial', 12), text=f'Score: {self.score}')

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
