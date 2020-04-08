#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>


import time
from concurrent import futures
import logging
import grpc
import backend_pb2
import backend_pb2_grpc
import optparse
from core import Core
from crypto_utils import RSACipher
from constants import PRIVATE_KEY, PUBLIC_KEY


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
decrypt_rsa = RSACipher("", PRIVATE_KEY)
encrypt_rsa = RSACipher(PUBLIC_KEY, "")


class Verification(backend_pb2_grpc.VerificationServicer):

    def __init__(self):
        self.core = Core()

    def verification(self, request, context):
        resp = {"success": False, "message": "failure"}
        print(request.key)
        try:
            params = self.core.decode(request.key)
            status, msg = self.core.verify(params)
            print(params)
            resp = {"success": status, "message": msg}
            return backend_pb2.VerificationResult(
                result=self.core.encode(resp)
            )
        except Exception as e:
            print(e)
            return backend_pb2.VerificationResult(
                result=self.core.encode(resp)
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_VerificationServicer_to_server(Verification(), server)
    server.add_insecure_port('[::]:{}'.format(server_port))
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', type="int", default=19969, dest="port")
    opt, args = parser.parse_args()
    server_port = opt.port

    server_host = "0.0.0.0"
    auth_logger = logging.getLogger(__name__ + "__auth__")
    auth_logger.setLevel(level=logging.INFO)
    auth_handler = logging.FileHandler("auth_log.txt")
    auth_stream_handler = logging.StreamHandler()
    auth_handler.setLevel(logging.INFO)
    auth_logger.addHandler(auth_handler)
    auth_logger.addHandler(auth_stream_handler)

    print('Running on http://{}:{}/ <Press CTRL + C to quit>'.format(server_host, server_port))
    serve()
