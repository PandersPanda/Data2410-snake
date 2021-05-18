# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import snake_pb2 as snake__pb2


class SnakeServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetGameConfigurations = channel.unary_unary(
                '/SnakeService/GetGameConfigurations',
                request_serializer=snake__pb2.GetRequest.SerializeToString,
                response_deserializer=snake__pb2.GameConfig.FromString,
                )
        self.JoinGame = channel.unary_unary(
                '/SnakeService/JoinGame',
                request_serializer=snake__pb2.JoinRequest.SerializeToString,
                response_deserializer=snake__pb2.Snake.FromString,
                )
        self.MoveSnake = channel.unary_unary(
                '/SnakeService/MoveSnake',
                request_serializer=snake__pb2.MoveRequest.SerializeToString,
                response_deserializer=snake__pb2.Snake.FromString,
                )
        self.GetAllSnakes = channel.unary_stream(
                '/SnakeService/GetAllSnakes',
                request_serializer=snake__pb2.Point.SerializeToString,
                response_deserializer=snake__pb2.SnakeSegment.FromString,
                )
        self.GetFood = channel.unary_stream(
                '/SnakeService/GetFood',
                request_serializer=snake__pb2.GetRequest.SerializeToString,
                response_deserializer=snake__pb2.Point.FromString,
                )
        self.AddMoreFood = channel.unary_unary(
                '/SnakeService/AddMoreFood',
                request_serializer=snake__pb2.GetRequest.SerializeToString,
                response_deserializer=snake__pb2.Point.FromString,
                )
        self.CheckCollision = channel.unary_unary(
                '/SnakeService/CheckCollision',
                request_serializer=snake__pb2.CollisionRequest.SerializeToString,
                response_deserializer=snake__pb2.CollisionResponse.FromString,
                )
        self.KillSnake = channel.unary_unary(
                '/SnakeService/KillSnake',
                request_serializer=snake__pb2.KillSnakeRequest.SerializeToString,
                response_deserializer=snake__pb2.Snake.FromString,
                )


class SnakeServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetGameConfigurations(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MoveSnake(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllSnakes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFood(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddMoreFood(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckCollision(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def KillSnake(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SnakeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetGameConfigurations': grpc.unary_unary_rpc_method_handler(
                    servicer.GetGameConfigurations,
                    request_deserializer=snake__pb2.GetRequest.FromString,
                    response_serializer=snake__pb2.GameConfig.SerializeToString,
            ),
            'JoinGame': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinGame,
                    request_deserializer=snake__pb2.JoinRequest.FromString,
                    response_serializer=snake__pb2.Snake.SerializeToString,
            ),
            'MoveSnake': grpc.unary_unary_rpc_method_handler(
                    servicer.MoveSnake,
                    request_deserializer=snake__pb2.MoveRequest.FromString,
                    response_serializer=snake__pb2.Snake.SerializeToString,
            ),
            'GetAllSnakes': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAllSnakes,
                    request_deserializer=snake__pb2.Point.FromString,
                    response_serializer=snake__pb2.SnakeSegment.SerializeToString,
            ),
            'GetFood': grpc.unary_stream_rpc_method_handler(
                    servicer.GetFood,
                    request_deserializer=snake__pb2.GetRequest.FromString,
                    response_serializer=snake__pb2.Point.SerializeToString,
            ),
            'AddMoreFood': grpc.unary_unary_rpc_method_handler(
                    servicer.AddMoreFood,
                    request_deserializer=snake__pb2.GetRequest.FromString,
                    response_serializer=snake__pb2.Point.SerializeToString,
            ),
            'CheckCollision': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckCollision,
                    request_deserializer=snake__pb2.CollisionRequest.FromString,
                    response_serializer=snake__pb2.CollisionResponse.SerializeToString,
            ),
            'KillSnake': grpc.unary_unary_rpc_method_handler(
                    servicer.KillSnake,
                    request_deserializer=snake__pb2.KillSnakeRequest.FromString,
                    response_serializer=snake__pb2.Snake.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SnakeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SnakeService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetGameConfigurations(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeService/GetGameConfigurations',
            snake__pb2.GetRequest.SerializeToString,
            snake__pb2.GameConfig.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def JoinGame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeService/JoinGame',
            snake__pb2.JoinRequest.SerializeToString,
            snake__pb2.Snake.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MoveSnake(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeService/MoveSnake',
            snake__pb2.MoveRequest.SerializeToString,
            snake__pb2.Snake.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllSnakes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/SnakeService/GetAllSnakes',
            snake__pb2.Point.SerializeToString,
            snake__pb2.SnakeSegment.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFood(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/SnakeService/GetFood',
            snake__pb2.GetRequest.SerializeToString,
            snake__pb2.Point.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddMoreFood(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeService/AddMoreFood',
            snake__pb2.GetRequest.SerializeToString,
            snake__pb2.Point.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckCollision(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeService/CheckCollision',
            snake__pb2.CollisionRequest.SerializeToString,
            snake__pb2.CollisionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def KillSnake(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SnakeService/KillSnake',
            snake__pb2.KillSnakeRequest.SerializeToString,
            snake__pb2.Snake.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
