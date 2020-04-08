#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

import base64
import wmi
import random
import json
import time
import win32api
import hashlib
from nv.crypto_utils import AESCipher, RSACipher, TripleDES
from nv.constants import SPLIT_FLAG, AES_KEY, PUBLIC_KEY, PRIVATE_KEY, DES3_KEY
from nv.utils import read_license
from psutil import net_if_addrs


w = wmi.WMI()
encrypt_rsa = RSACipher(PUBLIC_KEY, "")
decrypt_rsa = RSACipher("", PRIVATE_KEY)
aes_utils = AESCipher(DES3_KEY)


class Core(object):

    split_flag = SPLIT_FLAG.encode("utf8")

    def __init__(self):
        self.aes = AESCipher(AES_KEY)
        self.secret_key = "..``…………····-`''':'''"

    @classmethod
    def gen_tag(cls):
        r = str(random.random()).encode("ascii")
        tag = hashlib.md5(r).hexdigest()
        return tag

    def switch_aes(self, index):
        index = int(index)
        if index % 2 == 0:
            return aes_utils
        else:
            return self.aes

    @classmethod
    def new_des3(cls):
        key = cls.gen_tag()
        enc_key = encrypt_rsa.encrypt(key)
        des3 = TripleDES(key)
        return enc_key, des3

    @classmethod
    def get_user_name(cls):
        return win32api.GetUserName()

    @classmethod
    def mac_addr(cls, text):
        group = [v[0][1] for v in net_if_addrs().values() if len(v[0][1]) == 17]
        return base64.b64encode((group[0] + str(text)).encode("utf8")).decode()

    @classmethod
    def board_id(cls):
        for board in w.Win32_BaseBoard():
            return board.SerialNumber

    @classmethod
    def bios_id(cls):
        for bios in w.Win32_BIOS():
            return bios.SerialNumber.strip()

    @classmethod
    def origin_code(cls):
        return base64.b64encode("{}{}{}".format(
            Core.board_id(), Core.split_flag.decode(), Core.bios_id()
        ).encode("utf8")).decode()

    def machine_code(self):
        encrypted: str = self.aes.encrypt("{}{}".format(Core.origin_code(), self.secret_key))
        return encrypted.replace("1", ")").replace("9", "{").replace("E", "&").replace("b", "%").replace("=", "\\")[::-1]

    def extract(self, machine_code):
        first_step = machine_code.replace(")", "1").replace("{", "9").replace("&", "E").replace("%", "b").replace("\\", "=")[::-1]
        try:
            second_step: bytes = base64.b64decode(self.aes.decrypt(first_step)[:-21])
        except Exception as e:
            return "FAKE_{}".format(e)
        if Core.split_flag not in second_step:
            return "FAKE_{}".format("VER ERROR")
        board_id, bios_id = second_step.split(Core.split_flag)
        return board_id.decode(), bios_id.decode()

    @classmethod
    def auth_code(cls):
        auth_code = base64.b64encode(
            hashlib.md5("\u0000\u9999\0||{}||{}||\n\r\0\u8888".format(
                cls.board_id(), cls.bios_id()
            ).encode('utf8')).hexdigest().encode("utf8")
        ).decode()
        return auth_code[:6] + auth_code[-10:]

    def encode(self, params: dict):
        try:
            params.update({
                "timestamp": time.time(),
                "auth_code": self.auth_code(),
                "board_id": self.board_id(),
                "bios_id": self.bios_id()
            })
            plain_text = json.dumps(params, ensure_ascii=False)
            enc_key, des3 = self.new_des3()
            encrypted_first = des3.encrypt(plain_text)
            rand_index = random.randint(0, 9)
            aes = self.switch_aes(rand_index)
            encrypted_second = aes.encrypt("{}&{}".format(encrypted_first, enc_key))
            return "{}{}".format(rand_index, encrypted_second)
        except Exception as e:
            print(e)
            return e

    def decode(self, encrypted_text: str):
        try:
            encrypted_aes = encrypted_text[1:]
            _aes = self.switch_aes(encrypted_text[0:1])
            encrypted_des3_group: str = _aes.decrypt(encrypted_aes)
            encrypted_des3_list = encrypted_des3_group.split("&")
            encrypted_des3_key, encrypted_des3_text = encrypted_des3_list[1], encrypted_des3_list[0]
            des3_key = decrypt_rsa.decrypt(encrypted_des3_key)
            plain_text = TripleDES(des3_key).decrypt(encrypted_des3_text)
            params = json.loads(plain_text)
        except Exception as e:
            return {"success": False, "message": e}
        return params

    @classmethod
    def verify(cls):
        if read_license() != cls.auth_code():
            return False
        return True


if __name__ == '__main__':
    a = Core().machine_code()
    print(a)
    b = Core().extract(a)
    print(b)
    c = Core.auth_code()
    print(c)
    timestamp = int(time.time() * 1000)
