import tkinter as tk
import random
from PIL import ImageTk, Image

class Ball:
    def __init__(self, canvas, platform, color):
        self.canvas = canvas
        self.platform = platform
        self.oval = canvas.create_oval(200, 200, 215, 215, fill=color)
        self.dir = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(self.dir)
        self.y = -5
        self.touch_bottom = False
        self.speed = 5  

    def touch_platform(self, ball_pos):
        platform_pos = self.canvas.coords(self.platform.rect)
        if ball_pos[2] >= platform_pos[0] and ball_pos[0] <= platform_pos[2]:
            if ball_pos[3] >= platform_pos[1] and ball_pos[3] <= platform_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.oval, self.x, self.y)
        pos = self.canvas.coords(self.oval)
        if pos[1] <= 0:
            self.y = self.speed
        if pos[3] >= 400:
            self.touch_bottom = True
        if self.touch_platform(pos):
            self.y = -self.speed
            self.increase_speed()  
        if pos[0] <= 0:
            self.x = self.speed
        if pos[2] >= 500:
            self.x = -self.speed

    def increase_speed(self):
        self.speed += 0.5  

class Platform:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(230, 300, 330, 310, fill=color)
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)
        self.speed = 5  

    def left(self, event):
        self.x = -self.speed
        print(self.speed)

    def right(self, event):
        self.x = self.speed

    def draw(self):
        self.canvas.move(self.rect, self.x, 0)
        pos = self.canvas.coords(self.rect)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= 500:
            self.x = 0
    
    def increase_speed(self):
        self.speed += 5

class GameCanvas:
    def __init__(self, parent, width, height, background_image_path):
        self.canvas = tk.Canvas(parent, width=width, height=height)
        self.canvas.pack()

        self.background_image = ImageTk.PhotoImage(Image.open(background_image_path))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

class Game:
    def __init__(self, window):
        self.window = window
        self.canvas = GameCanvas(self.window, 500, 400, "E:/projects/platform/background.jpg")

        self.platform = Platform(self.canvas.canvas, 'green')
        self.ball = Ball(self.canvas.canvas, self.platform, 'red')

        self.game_over = False
        self.restart_button = tk.Button(window, text="Restart Game", command=self.restart_game)
        self.start_button = tk.Button(window, text="Почати Гру", command=self.start_game)

        self.label = None  # Додано атрибут 'label' зі значенням None

        self.canvas.canvas.focus_set()
        self.canvas.canvas.bind('<Left>', lambda _: self.platform.left(None))
        self.canvas.canvas.bind('<Right>', lambda _: self.platform.right(None))

        self.start_button.pack()

    def start_game(self):
        self.start_button.pack_forget()
        self.countdown(3)

    def countdown(self, seconds):
        if seconds > 0:
            if self.label:
                self.label.destroy()  # Видаляємо попередній label, якщо він існує
            self.label = tk.Label(self.window, text=str(seconds), font=('Arial', 30))
            self.label.place(x=250, y=200, anchor=tk.CENTER)
            self.window.after(1000, self.countdown, seconds - 1)
        else:
            self.start_new_game()

    def start_new_game(self):
        self.canvas.canvas.delete(tk.ALL)
        self.platform = Platform(self.canvas.canvas, 'green')
        self.ball = Ball(self.canvas.canvas, self.platform, 'red')

        self.game_loop()

    def restart_game(self):
        self.game_over = False
        self.ball.touch_bottom = False

        self.canvas.canvas.delete(tk.ALL)

        self.platform = Platform(self.canvas.canvas, 'green')
        self.ball = Ball(self.canvas.canvas, self.platform, 'red')

        self.game_loop()

    def game_loop(self):
        if not self.game_over:
            self.ball.draw()
            self.platform.draw()
            if not self.ball.touch_bottom:
                self.window.after(10, self.game_loop)
            else:
                self.game_over = True
                self.restart_button.pack()

window = tk.Tk()
window.title("Stack Ball")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)

game = Game(window)

window.mainloop()