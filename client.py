import random
import tkinter
import grpc
import snake_pb2
import snake_pb2_grpc
import time
import threading
import sys

SNAKE_SIZE = 20
GAME_SPEED = 50

GAME_WIDTH = 600
GAME_HEIGHT = 620

root = tkinter.Tk()
root.geometry(f'{GAME_WIDTH}x{GAME_HEIGHT}')
root.resizable(False, False)
root.title("Snake Game")

canvas = tkinter.Canvas(width=GAME_WIDTH, height=GAME_HEIGHT, highlightthickness=0, background='grey6')

channel = grpc.insecure_channel('localhost:50051')

stub = snake_pb2_grpc.SnakeServiceStub(channel)
try:
    snake = stub.addSnake(snake_pb2.JoinRequest())
except grpc.RpcError:
    print("This room is full of snakes!")
    sys.exit()
direction = snake.direction


def draw_snake(s):
    for p in s.body:
        canvas.create_rectangle(
            p.x * SNAKE_SIZE,
            p.y * SNAKE_SIZE,
            (p.x + 1) * SNAKE_SIZE,
            (p.y + 1) * SNAKE_SIZE,
            fill=s.color,
            tag='snake'
        )


def draw_food(food, r, color):
    assert 0 < r <= 1
    assert 0 <= food.x < 30
    assert 0 <= food.y < 31

    food = canvas.create_oval(
        (food.x + .5 + r / 2) * SNAKE_SIZE,
        (food.y + .5 + r / 2) * SNAKE_SIZE,
        (food.x + .5 - r / 2) * SNAKE_SIZE,
        (food.y + .5 - r / 2) * SNAKE_SIZE,
        fill=color,
        tag='food'
    )
    canvas.tag_lower(food)


def move_snake():
    global snake
    snake = stub.moveSnake(
        snake_pb2.MoveRequest(color=snake.color, direction=direction)
    )


def change_direction(event):
    global direction
    available_directions = {
        'Up': 'Up',
        'Down': 'Down',
        'Left': 'Left',
        'Right': 'Right',
        'w': 'Up',
        'a': 'Left',
        's': 'Down',
        'd': 'Right'
    }
    new_direction = available_directions.get(event.keysym, False)
    if new_direction:
        direction = new_direction


def check_collision():
    has_collided = stub.checkCollision(
        snake_pb2.CollisionRequest(color=snake.color)
    )
    return has_collided.has_collided


def draw_all_snakes():
    canvas.delete('snake')
    snakes = stub.getSnakes(snake_pb2.GetRequest())
    for s in snakes:
        draw_snake(s)


def spawn_foods():
    canvas.delete('food')
    foods = stub.getFood(snake_pb2.FoodRequest())
    for f in foods:
        draw_food(food=f, r=0.5, color='White')


def random_food():
    while True:
        stub.addMoreFood(snake_pb2.FoodRequest())
        time.sleep(random.randint(5, 10))


canvas.bind_all('<Key>', change_direction)


def game_flow():
    global snake
    move_snake()
    if check_collision():
        root.quit()
    draw_all_snakes()
    spawn_foods()
    canvas.after(GAME_SPEED, game_flow)


def start_game(event):
    start_game_button.destroy()
    canvas.pack()
    random_food_thread = threading.Thread(target=random_food, daemon=True)
    random_food_thread.start()
    game_flow()


def on_closing():
    canvas.delete('all')
    stub.removeSnake(snake)
    root.quit()


start_game_button = tkinter.Button(root, text="Start game")
start_game_button.bind('<Button-1>', start_game)
start_game_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
