# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import snake_pb2 as snake__pb2


class SnakeGameServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.addSnake = channel.unary_unary(
                '/SnakeGameService/addSnake',
                request_serializer=snake__pb2.Snake.SerializeToString,
                response_deserializer=snake__pb2.Snake.FromString,
                )
        self.locateOtherSnakes = channel.unary_stream(
                '/SnakeGameService/locateOtherSnakes',
                request_serializer=snake__pb2.Snake.SerializeToString,
                response_deserializer=snake__pb2.Snake.FromString,
                )
        self.spawnFood = channel.unary_unary(
                '/SnakeGameService/spawnFood',
                request_serializer=snake__pb2.Point.SerializeToString,
                response_deserializer=snake__pb2.Food.FromString,
                )
        self.moveSnake = channel.unary_unary(
                '/SnakeGameService/moveSnake',
                request_serializer=snake__pb2.Snake.SerializeToString,
                response_deserializer=snake__pb2.Snake.FromString,
                )
        self.eatFood = channel.unary_unary(
                '/SnakeGameService/eatFood',
                request_serializer=snake__pb2.Snake.SerializeToString,
                response_deserializer=snake__pb2.Snake.FromString,
                )
        self.deadSnake = channel.unary_unary(
                '/SnakeGameService/deadSnake',
                request_serializer=snake__pb2.Snake.SerializeToString,
                response_deserializer=snake__pb2.Snake.FromString,
                )


class SnakeGameServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def addSnake(self, request, context):
        """Functions for the game:
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def locateOtherSnakes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def spawnFood(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def moveSnake(self, request, context):
        """Functions for controlling snakes:
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def eatFood(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deadSnake(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SnakeGameServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'addSnake': grpc.unary_unary_rpc_method_handler(
                    servicer.addSnake,
                    request_deserializer=snake__pb2.Snake.FromString,
                    response_serializer=snake__pb2.Snake.SerializeToString,
            ),
            'locateOtherSnakes': grpc.unary_stream_rpc_method_handler(
                    servicer.locateOtherSnakes,
                    request_deserializer=snake__pb2.Snake.FromString,
                    response_serializer=snake__pb2.Snake.SerializeToString,
            ),
            'spawnFood': grpc.unary_unary_rpc_method_handler(
                    servicer.spawnFood,
                    request_deserializer=snake__pb2.Point.FromString,
                    response_serializer=snake__pb2.Food.SerializeToString,
            ),
            'moveSnake': grpc.unary_unary_rpc_method_handler(
                    servicer.moveSnake,
                    request_deserializer=snake__pb2.Snake.FromString,
                    response_serializer=snake__pb2.Snake.SerializeToString,
            ),
            'eatFood': grpc.unary_unary_rpc_method_handler(
                    servicer.eatFood,
                    request_deserializer=snake__pb2.Snake.FromString,
                    response_serializer=snake__pb2.Snake.SerializeToString,
            ),
            'deadSnake': grpc.unary_unary_rpc_method_handler(
                    servicer.deadSnake,
                    request_deserializer=snake__pb2.Snake.FromString,
                    response_serializer=snake__pb2.Snake.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SnakeGameService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SnakeGameService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def addSnake(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeGameService/addSnake',
            snake__pb2.Snake.SerializeToString,
            snake__pb2.Snake.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def locateOtherSnakes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/SnakeGameService/locateOtherSnakes',
            snake__pb2.Snake.SerializeToString,
            snake__pb2.Snake.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def spawnFood(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeGameService/spawnFood',
            snake__pb2.Point.SerializeToString,
            snake__pb2.Food.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def moveSnake(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeGameService/moveSnake',
            snake__pb2.Snake.SerializeToString,
            snake__pb2.Snake.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def eatFood(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeGameService/eatFood',
            snake__pb2.Snake.SerializeToString,
            snake__pb2.Snake.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deadSnake(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeGameService/deadSnake',
            snake__pb2.Snake.SerializeToString,
            snake__pb2.Snake.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
