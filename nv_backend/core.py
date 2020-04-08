#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os
import json
import time
import base64
import random
import hashlib
from crypto_utils import AESCipher, TripleDES, RSACipher
from constants import AES_KEY, DES3_KEY, PUBLIC_KEY, PRIVATE_KEY, SPLIT_FLAG


even_aes = AESCipher(DES3_KEY)
odd_aes = AESCipher(AES_KEY)
encrypt_rsa = RSACipher(PUBLIC_KEY, "")
decrypt_rsa = RSACipher("", PRIVATE_KEY)


class Core:

    split_flag = SPLIT_FLAG.encode("utf8")

    @classmethod
    def gen_tag(cls):
        r = str(time.time()).encode("ascii")
        tag = hashlib.md5(r).hexdigest()
        return tag

    @classmethod
    def new_des3(cls):
        key = cls.gen_tag()
        enc_key = encrypt_rsa.encrypt(key)
        des3 = TripleDES(key)
        return enc_key, des3

    @staticmethod
    def switch_aes(index):
        index = int(index)
        if index % 2 == 0:
            return even_aes
        else:
            return odd_aes

    @classmethod
    def blacklist(cls):
        path = "blacklist.txt"
        if not os.path.exists(path):
            with open("blacklist.txt", "w") as f:
                f.write("")
                return ""
        with open("blacklist.txt", "r") as f:
            return ";".join(f.readlines())

    @classmethod
    def auth_code(cls, board_id, bios_id):
        auth_code = base64.b64encode(
            hashlib.md5("\u0000\u9999\0||{}||{}||\n\r\0\u8888".format(
                board_id, bios_id
            ).encode('utf8')).hexdigest().encode("utf8")
        ).decode()
        return auth_code[:6] + auth_code[-10:]

    @classmethod
    def extract(cls, machine_code):
        first_step = machine_code.replace(")", "1").replace("{", "9").replace("&", "E").replace("%", "b").replace("\\", "=")[::-1]
        try:
            second_step: bytes = base64.b64decode(odd_aes.decrypt(first_step)[:-21])
        except Exception as e:
            return "FAKE_{}".format(e)
        if Core.split_flag not in second_step:
            return "FAKE_{}".format("VER ERROR")
        board_id, bios_id = second_step.split(Core.split_flag)
        return board_id.decode(), bios_id.decode()

    def encode(self, params: dict):
        try:
            print(params)
            params.update(
                {"timestamp": time.time()}
            )
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

    @classmethod
    def decode(cls, encrypted_text: str):
        try:
            encrypted_aes = encrypted_text[1:]
            _aes = cls.switch_aes(encrypted_text[0:1])
            encrypted_des3_group: str = _aes.decrypt(encrypted_aes)

            encrypted_des3_list = encrypted_des3_group.split("&")
            encrypted_des3_key, encrypted_des3_text = encrypted_des3_list[1], encrypted_des3_list[0]
            des3_key = decrypt_rsa.decrypt(encrypted_des3_key)

            plain_text = TripleDES(des3_key).decrypt(encrypted_des3_text)
            params = json.loads(plain_text)
        except Exception as e:
            return {"except": str(e)}
        return params

    def verify(self, params: dict):
        if "except" in params:
            return False, "LOCAL-PARSE:{}".format(params.get("except"))
        timestamp = params.get("timestamp")
        auth_code: str = params.get("auth_code")
        if auth_code in self.blacklist():
            return False, "LOCAL-AUTH:BLACKLIST"
        board_id: str = params.get("board_id")
        bios_id: str = params.get("bios_id")
        v_auth_code = self.auth_code(board_id=board_id, bios_id=bios_id)
        if v_auth_code != auth_code:
            return False, "LOCAL-AUTH:INVALID"
        now_timestamp = time.time()
        try:
            timestamp = float(timestamp)
        except ValueError:
            return False, "LOCAL-TIME:VALUE-ERROR"
        if timestamp < (now_timestamp - 180) or timestamp > (now_timestamp + 180):
            return False, "LOCAL-TIME:FAKE-OR-INCONSISTENCY"
        if bios_id and "vmware" in bios_id.lower():
            return False, "LOCAL-ENV:CANNOT-RUN-ON-VM"
        return True, ""


