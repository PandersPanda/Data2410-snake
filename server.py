import snake_pb2_grpc
from snake_pb2 import GameConfig, Point, Snake, SnakeSegment, CollisionResponse
import grpc
from concurrent import futures
import random
import mysql.connector


class SnakeService(snake_pb2_grpc.SnakeServiceServicer):
    GAME_CONFIGURATION = GameConfig()
    AVAILABLE_COLORS = ['Purple', 'Maroon1', 'Cyan2', 'Orange', 'Green', 'Yellow', 'Blue', 'Red']
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
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()

    def GetGameConfigurations(self, request, context):
        window_width = 600
        window_height = 600
        board_width = 2 * window_width
        board_height = 2 * window_height
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

        snake = Snake(
            name=request.name,
            color=self.AVAILABLE_COLORS.pop(),
            direction=random.choice(directions),
            body=body
        )

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

        snake.body.pop()
        snake.body.insert(0, new_head)
        snake.direction = direction
        return snake

    def GetAllSnakes(self, request, context):
        x, y = request.x, request.y

        list_of_points = []
        for snake in self.SNAKES.values():
            snake_segment = map(lambda p: SnakeSegment(point=p, color=snake.color), snake.body)
            list_of_points.extend(snake_segment)

        for segment in list_of_points:
            if abs(segment.point.x - x) < 30 and abs(segment.point.y - y) < 30:
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

    def KillSnake(self, request, context):
        snake = self.SNAKES.get(request.name, None)
        self.turn_snake_to_food(snake)
        return snake

    def turn_snake_to_food(self, snake):
        self.FOODS.extend(random.sample(snake.body, len(snake.body) // 3))
        snake = self.SNAKES.pop(snake.name, None)
        self.update_highscore(snake)
        self.AVAILABLE_COLORS.append(snake.color)

    def add_food(self):
        x = random.randint(0, self.GAME_CONFIGURATION.max_x - 1)
        y = random.randint(0, self.GAME_CONFIGURATION.max_y - 1)
        snakes = []
        for snake in self.SNAKES.values():
            snakes.extend(snake.body)

        p = Point(x=x, y=y)
        while p in snakes:
            p = Point(
                x=random.randint(0, self.GAME_CONFIGURATION.max_x - 1),
                y=random.randint(0, self.GAME_CONFIGURATION.max_y - 1)
            )

        self.FOODS.append(p)

    def update_highscore(self, snake):
        self.cursor.execute("USE snake_highscores")
        data = (snake.name, len(snake.body) - 3)
        insert_command = (
            "INSERT INTO highscores(username, score) "
            "VALUES (%s, %s)"
        )
        self.cursor.execute(insert_command, data)

        self.cnxn.commit()
        self.cursor.close()
        self.cnxn.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    snake_pb2_grpc.add_SnakeServiceServicer_to_server(
        SnakeService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Snake server is running...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
