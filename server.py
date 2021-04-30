import grpc
import snake_pb2_grpc
import snake_pb2
from snake_pb2 import Snake, Point
from concurrent import futures
import random


class SnakeGame(snake_pb2_grpc.SnakeServiceServicer):
    SNAKES = {}
    FOODS = []
    AVAILABLE_COLORS = ['Purple', 'Maroon1', 'Cyan2', 'Orange', 'Green', 'Yellow', 'Blue', 'Red']
    DIRECTIONS = {
        'Right': 1,
        'Left': -1,
        'Down': 1,
        'Up': -1
    }

    def addSnake(self, request, context):
        #  Possible directions:
        directions = ['Up', 'Down', 'Left', 'Right']

        x, y = random.randint(6, 24), random.randint(6, 27)
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
            color=self.AVAILABLE_COLORS.pop(),
            direction=random.choice(directions),
            body=body
        )
        self.SNAKES.update({snake.color: snake})
        return snake

    def removeSnake(self, request, context):
        snake = self.SNAKES.pop(request.color, None)
        if snake is not None:
            self.AVAILABLE_COLORS.append(snake.color)
        return request

    def moveSnake(self, request, context):
        # MoveRequest(color= ... , direction=...)
        new_direction = request.direction
        snake = self.SNAKES.get(request.color, None)

        opposite_direction = [{'Up', 'Down'}, {'Left', 'Right'}]
        if {snake.direction, new_direction} in opposite_direction:
            new_direction = snake.direction
        # [Point(x=2, y=0), Point(x=1, y=0), Point(x=0, y=0)]
        new_head = Point(x=snake.body[0].x, y=snake.body[0].y)

        if new_direction == "Right" or new_direction == 'Left':
            new_head.x = (snake.body[0].x + self.DIRECTIONS.get(new_direction, 0)) % 30
        else:
            new_head.y = (snake.body[0].y + self.DIRECTIONS.get(new_direction, 0)) % 31

        if new_head in self.FOODS:
            self.FOODS.remove(new_head)
            if len(self.FOODS) == 0:
                self.add_food()
        else:
            snake.body.pop()

        snake.body.insert(0, new_head)
        snake.direction = new_direction

        return snake

    def checkCollision(self, request, context):
        snake = self.SNAKES.get(request.color, None)
        head_x, head_y = snake.body[0].x, snake.body[0].y

        # Check border and self_snake:
        if Point(x=head_x, y=head_y) in snake.body[1:]:
            self.turn_snake_to_food(snake)
            return snake_pb2.CollisionResponse(has_collided=True)  # return True

        other_snakes = self.SNAKES.copy()
        other_snakes.pop(request.color)

        # Check for other snakes
        for s in other_snakes.values():
            if Point(x=head_x, y=head_y) in s.body:
                self.turn_snake_to_food(snake)
                return snake_pb2.CollisionResponse(has_collided=True)

        return snake_pb2.CollisionResponse(has_collided=False)  # Return False

    def getSnakes(self, request, context):
        for snake in self.SNAKES.values():
            yield snake

    def getFood(self, request, context):
        if len(self.FOODS) == 0:
            self.add_food()
        for food in self.FOODS:
            yield food

    def addMoreFood(self, request, context):
        self.add_food()
        return request

    def add_food(self):
        x, y = random.randint(0, 29), random.randint(0, 30)
        snakes = []
        for snake in self.SNAKES.values():
            snakes.extend(snake.body)

        p = Point(x=x, y=y)
        while p in snakes:
            x, y = random.randint(0, 29), random.randint(0, 30)
            p = Point(x=x, y=y)

        self.FOODS.append(p)

    def turn_snake_to_food(self, snake):
        self.FOODS.append(random.choice(snake.body))
        self.SNAKES.pop(snake.color, None)
        self.AVAILABLE_COLORS.append(snake.color)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    snake_pb2_grpc.add_SnakeServiceServicer_to_server(
        SnakeGame(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
