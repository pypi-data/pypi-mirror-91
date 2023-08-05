# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import soco_encoders.grpc.embedding_pb2 as embedding__pb2


class EncoderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.encode = channel.unary_unary(
                '/Encoder/encode',
                request_serializer=embedding__pb2.Input.SerializeToString,
                response_deserializer=embedding__pb2.Embedding.FromString,
                )


class EncoderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def encode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EncoderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'encode': grpc.unary_unary_rpc_method_handler(
                    servicer.encode,
                    request_deserializer=embedding__pb2.Input.FromString,
                    response_serializer=embedding__pb2.Embedding.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Encoder', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Encoder(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def encode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Encoder/encode',
            embedding__pb2.Input.SerializeToString,
            embedding__pb2.Embedding.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
