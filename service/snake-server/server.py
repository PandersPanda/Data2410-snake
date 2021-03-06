import sys

import snake_pb2_grpc
from snake_pb2 import GameConfig, Point, Snake, SnakeSegment, CollisionResponse, Score, ScoreResponse
import grpc
from concurrent import futures
import random
import json
import signal


class SnakeService(snake_pb2_grpc.SnakeServiceServicer):
    GAME_CONFIGURATION = GameConfig()
    AVAILABLE_COLORS = []
    BOT_NAMES = []
    SNAKES = {}
    DIRECTIONS = {
        'Right': Point(x=1, y=0),
        'Down': Point(x=0, y=1),
        'Left': Point(x=-1, y=0),
        'Up': Point(x=0, y=-1)
    }
    OPPOSITE_DIRECTIONS = [{'Up', 'Down'}, {'Left', 'Right'}]
    FOODS = []

    # HS database:
    config = {
        'user': 'app_user',
        'password': 'k2znHSJnNlmi5znh',
        'host': '35.228.86.138',
    }

    def GetGameConfigurations(self, request, context):
        window_width = 600
        window_height = 600
        board_width = 4 * window_width
        board_height = 4 * window_height
        snake_size = 20
        game_speed = 50
        max_x = board_width // snake_size
        max_y = board_height // snake_size
        scroll_response_x = 1 / (2 * board_width / window_width)
        scroll_response_y = 1 / (2 * board_height / window_height)
        scroll_fraction_x = 1 / max_x
        scroll_fraction_y = 1 / max_y
        background_color = 'grey6'
        border_color = 'red4'

        with open('tkinter-colors.json', 'r') as f:
            self.AVAILABLE_COLORS.extend(json.load(f))
        with open('bot-names.json', 'r') as f:
            self.BOT_NAMES.extend(random.sample(json.load(f), 377))

        self.GAME_CONFIGURATION.window_width = window_width
        self.GAME_CONFIGURATION.window_height = window_height
        self.GAME_CONFIGURATION.board_width = board_width
        self.GAME_CONFIGURATION.board_height = board_height
        self.GAME_CONFIGURATION.snake_size = snake_size
        self.GAME_CONFIGURATION.game_speed = game_speed
        self.GAME_CONFIGURATION.max_x = max_x
        self.GAME_CONFIGURATION.max_y = max_y
        self.GAME_CONFIGURATION.scroll_response_x = scroll_response_x
        self.GAME_CONFIGURATION.scroll_response_y = scroll_response_y
        self.GAME_CONFIGURATION.scroll_fraction_x = scroll_fraction_x
        self.GAME_CONFIGURATION.scroll_fraction_y = scroll_fraction_y
        self.GAME_CONFIGURATION.background_color = background_color
        self.GAME_CONFIGURATION.border_color = border_color

        return self.GAME_CONFIGURATION

    def JoinGame(self, request, context):
        #  Possible directions:
        directions = ['Up', 'Down', 'Left', 'Right']

        x = random.randint(10, self.GAME_CONFIGURATION.max_x - 10)
        y = random.randint(10, self.GAME_CONFIGURATION.max_y - 10)

        body = [Point(x=x, y=y)]  # Random head
        if random.randint(0, 1):
            r = random.choice([-1, 1])
            x += r
            if r < 0:
                directions.remove('Left')
            else:
                directions.remove('Right')
        else:
            r = random.choice([-1, 1])
            y += r
            if r < 0:
                directions.remove('Up')
            else:
                directions.remove('Down')

        body.append(Point(x=x, y=y))

        if random.randint(0, 1):
            x += random.choice([-1, 1])
        else:
            y += random.choice([-1, 1])
        body.append(Point(x=x, y=y))

        color = random.choice(self.AVAILABLE_COLORS)
        self.AVAILABLE_COLORS.remove(color)

        snake = Snake(
            is_bot=request.is_bot,
            color=color,
            direction=random.choice(directions),
            body=body
        )

        if snake.is_bot:
            snake.name = random.choice(self.BOT_NAMES)
            self.BOT_NAMES.remove(snake.name)
        else:
            snake.name = request.name

        self.SNAKES.update({snake.name: snake})
        return snake

    def MoveSnake(self, request, context):
        snake = self.SNAKES.get(request.name, None)
        direction = request.direction

        if {snake.direction, direction} in self.OPPOSITE_DIRECTIONS:
            direction = snake.direction

        new_head = Point(x=snake.body[0].x, y=snake.body[0].y)
        new_head.x += self.DIRECTIONS[direction].x
        new_head.y += self.DIRECTIONS[direction].y

        if new_head in self.FOODS:
            self.FOODS.remove(new_head)
            if len(self.FOODS) == 0:
                self.add_food()
        else:
            snake.body.pop()

        snake.body.insert(0, new_head)
        snake.direction = direction
        return snake

    def GetAllSnakes(self, request, context):
        x, y = request.x, request.y
        x_scroll = x * self.GAME_CONFIGURATION.scroll_fraction_x - self.GAME_CONFIGURATION.scroll_response_x
        y_scroll = y * self.GAME_CONFIGURATION.scroll_fraction_y - self.GAME_CONFIGURATION.scroll_response_y

        x_vision = 1 if 0 < x_scroll < 0.7 else 0
        y_vision = 1 if 0 < y_scroll < 0.7 else 0

        list_of_points = []
        for snake in self.SNAKES.values():
            snake_segment = map(lambda p: SnakeSegment(point=p, color=snake.color), snake.body)
            list_of_points.extend(snake_segment)

        for segment in list_of_points:
            if abs(segment.point.x - x) < 30 - 14 * x_vision and abs(segment.point.y - y) < 30 - 14 * y_vision:
                yield segment

    def CheckCollision(self, request, context):
        snake = self.SNAKES.get(request.name, None)
        head_x, head_y = snake.body[0].x, snake.body[0].y

        # Self_snake:
        if Point(x=head_x, y=head_y) in snake.body[1:] or \
                head_x in (0, self.GAME_CONFIGURATION.max_x - 1) or \
                head_y in (0, self.GAME_CONFIGURATION.max_y - 1):
            return CollisionResponse(has_collided=True)  # return True

        other_snakes = self.SNAKES.copy()
        other_snakes.pop(request.name)

        # Check for other snakes
        for s in other_snakes.values():
            if Point(x=head_x, y=head_y) in s.body:
                return CollisionResponse(has_collided=True)

        return CollisionResponse(has_collided=False)

    def GetFood(self, request, context):
        x, y = request.x, request.y
        x_scroll = x * self.GAME_CONFIGURATION.scroll_fraction_x - self.GAME_CONFIGURATION.scroll_response_x
        y_scroll = y * self.GAME_CONFIGURATION.scroll_fraction_y - self.GAME_CONFIGURATION.scroll_response_y
        x_vision = 1 if 0 < x_scroll < 0.7 else 0
        y_vision = 1 if 0 < y_scroll < 0.7 else 0

        if len(self.FOODS) == 0:
            self.add_food()
        for food in self.FOODS:
            if abs(food.x - x) < 30 - 14 * x_vision and abs(food.y - y) < 30 - 14 * y_vision:
                yield food

    def GetAllFood(self, request, context):
        if len(self.FOODS) == 0:
            self.add_food()
        for food in self.FOODS:
            yield food

    def AddMoreFood(self, request, context):
        return self.add_food()

    def KillSnake(self, request, context):
        snake = self.SNAKES.get(request.name, None)
        self.turn_snake_to_food(snake)
        if len(self.SNAKES) == 0:
            self.FOODS.clear()
        return snake

    def GetCurrentPlayerScores(self, request, context):
        scores = []
        for s in self.SNAKES.values():
            scores.append(Score(name=s.name, color=s.color, score=len(s.body) - 3))
        scores.sort(key=lambda x: x.score, reverse=True)  # Sort list in descending order
        return ScoreResponse(scores=scores)

    def turn_snake_to_food(self, snake):
        self.FOODS.extend(random.sample(snake.body, len(snake.body) // 3))
        snake = self.SNAKES.pop(snake.name, None)
        self.AVAILABLE_COLORS.append(snake.color)
        if snake.is_bot:
            self.BOT_NAMES.append(snake.name)

    def add_food(self):
        x = random.randint(2, self.GAME_CONFIGURATION.max_x - 2)
        y = random.randint(2, self.GAME_CONFIGURATION.max_y - 2)
        snakes = []
        for snake in self.SNAKES.values():
            snakes.extend(snake.body)

        p = Point(x=x, y=y)
        while p in snakes:
            p = Point(
                x=random.randint(2, self.GAME_CONFIGURATION.max_x - 2),
                y=random.randint(2, self.GAME_CONFIGURATION.max_y - 2)
            )

        self.FOODS.append(p)
        return p


def serve():
    with open('key.pem', 'rb') as f:
        private_key = f.read()
    with open('crt.pem', 'rb') as f:
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    snake_pb2_grpc.add_SnakeServiceServicer_to_server(
        SnakeService(), server
    )
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    print("Server is listening...")
    signal.signal(signal.SIGTERM, lambda: server.stop(30).wait(30))
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        sys.exit("Closing the server!")


if __name__ == '__main__':
    serve()
