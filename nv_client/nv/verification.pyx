#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import sys
import grpc
import nv.backend_pb2
import nv.backend_pb2_grpc
from nv.config import BACKEND_SERVER
from nv.utils import read_license
from nv.core import Core
from tkinter import messagebox


class GoogleRPC(object):

    def __init__(self, host):
        self.host = host
        self.core = Core()
        self.channel = grpc.insecure_channel(self.host)
        self.stub = nv.backend_pb2_grpc.VerificationStub(self.channel)

    def request(self, params: dict):

        response = self.stub.verification(nv.backend_pb2.VerificationRequest(
            key=self.core.encode(params)
        ))
        return response.result

    def verify(self):
        if self.core.auth_code() != read_license():
            return False, "LOCAL-AUTH:INVALID AUTH_CODE"
        resp = self.request({"is_available": "?"})
        params = self.core.decode(encrypted_text=resp)
        print(params)
        if params.get("success"):
            return True, ""
        return False, params.get("message")


def validate(func):
    def wrapper(*args, **kwargs):
        try:
            _license = read_license()
            _v, msg = GoogleRPC(BACKEND_SERVER).verify()
            if _v:
                return func(*args, **kwargs)
            else:
                tk = kwargs.get("parent")
                if tk:
                    tk.withdraw()
                messagebox.showinfo(title='错误', message='此版本已过期或未授权, 错误码: {}'.format(msg))
                sys.exit(-999)
        except Exception:
            messagebox.showinfo(title='错误', message='此版本已过期或未授权, 错误码: no connection!')
            sys.exit(-990)
    return wrapper


if __name__ == '__main__':
    import os
    os.chdir("../")
    _v, _msg = GoogleRPC(BACKEND_SERVER).verify()
    print(_v, _msg)

