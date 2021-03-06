# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from nv import backend_pb2 as nv_dot_backend__pb2


class VerificationStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.verification = channel.unary_unary(
                '/Verification/verification',
                request_serializer=nv_dot_backend__pb2.VerificationRequest.SerializeToString,
                response_deserializer=nv_dot_backend__pb2.VerificationResult.FromString,
                )


class VerificationServicer(object):
    """Missing associated documentation comment in .proto file"""

    def verification(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VerificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'verification': grpc.unary_unary_rpc_method_handler(
                    servicer.verification,
                    request_deserializer=nv_dot_backend__pb2.VerificationRequest.FromString,
                    response_serializer=nv_dot_backend__pb2.VerificationResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Verification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Verification(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def verification(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Verification/verification',
            nv_dot_backend__pb2.VerificationRequest.SerializeToString,
            nv_dot_backend__pb2.VerificationResult.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
