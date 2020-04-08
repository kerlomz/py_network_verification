#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES3
import base64

# Padding for the input string --not
# related to encryption itself.
BS = 16


class TripleDES:
    def __init__(self, key):
        self.key = TripleDES.create_key(key)
        self.mode = DES3.MODE_ECB

    @staticmethod
    def create_key(key):
        key = key.encode("utf8")
        if len(key) >= 16:
            tmp = key[0:15]
            key = tmp + b' '
        else:
            while len(key) < 16:
                key += b" "
        return key

    def encrypt(self, raw: str) -> str:
        raw = raw.encode("utf8")
        msg = raw + b'\0' * (8 - (len(raw) % 8))
        cipher = DES3.new(self.key, self.mode)
        encode = cipher.encrypt(msg)
        return base64.b64encode(encode).decode("utf8")

    def decrypt(self, enc: str) -> str:
        enc = enc.encode("utf8")
        cipher = DES3.new(self.key, self.mode)
        return (cipher.decrypt(base64.decodebytes(enc)).decode('utf-8')).rstrip('\0')


class AESCipher:

    def __init__(self, key: str):
        self.key = AESCipher.create_key(key)

    @staticmethod
    def create_key(key):
        key = key.encode("utf8")
        if len(key) >= 16:
            tmp = key[0:15]
            key = tmp + b' '
        else:
            while len(key) < 16:
                key += b" "
        return key

    def encrypt(self, raw: str):
        raw = (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode("utf8"))(raw.encode("utf8"))
        cipher = AES.new(self.key, AES.MODE_CBC, self.key)
        return base64.b64encode(cipher.encrypt(raw)).decode('utf8')

    def decrypt(self, enc: str):
        enc = enc.encode("utf8")
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.key)
        try:
            decrypted = (lambda s: s[:-ord(s[len(s) - 1:])])(cipher.decrypt(enc)).decode('utf8')
        except Exception as e:
            print(e)
            return None
        return decrypted


class RSACipher(object):

    def __init__(self, public_key: str, private_key: str):
        self.public_key = public_key.encode("utf8")
        self.private_key = private_key.encode("utf8")

    def encrypt(self, plain_text):
        if not plain_text:
            return None
        public_key = RSA.importKey(self.public_key)
        _p = Cipher_pkcs1_v1_5.new(public_key)
        plain_text = plain_text.encode('utf-8')
        # 1024bit key
        try:
            default_encrypt_length = 117
            len_content = len(plain_text)
            if len_content < default_encrypt_length:
                return base64.b64encode(_p.encrypt(plain_text)).decode()
            offset = 0
            params_lst = []
            while len_content - offset > 0:
                if len_content - offset > default_encrypt_length:
                    params_lst.append(_p.encrypt(plain_text[offset:offset + default_encrypt_length]))
                else:
                    params_lst.append(_p.encrypt(plain_text[offset:]))
                offset += default_encrypt_length
            target = b''.join(params_lst)
            return base64.b64encode(target).decode()
        except ValueError:
            return None

    def decrypt(self, cipher_text):
        if not cipher_text:
            return None
        private_key = RSA.importKey(self.private_key)
        _pri = Cipher_pkcs1_v1_5.new(private_key)
        cipher_text = base64.b64decode(cipher_text if isinstance(cipher_text, bytes) else cipher_text.encode('utf-8'))
        # 1024bit key
        try:
            default_length = 128
            len_content = len(cipher_text)
            if len_content < default_length:
                return _pri.decrypt(cipher_text, "ERROR").decode()
            offset = 0
            params_lst = []
            while len_content - offset > 0:
                if len_content - offset > default_length:
                    params_lst.append(_pri.decrypt(cipher_text[offset: offset + default_length], "ERROR"))
                else:
                    params_lst.append(_pri.decrypt(cipher_text[offset:], "ERROR"))
                offset += default_length
            target = b''.join(params_lst)
            return target.decode()
        except ValueError:
            return None


if __name__ == '__main__':
    aes = AESCipher('AES密钥')
    a = aes.encrypt('加密内容-aes')
    b = aes.decrypt(a)
    print(a, b)
    _public_key = '-----BEGIN RSA PUBLIC KEY-----\nMIGJAoGBAIamUzs7xYd2jzGuMvmlhQbBZXvglsdrtOd+nbV7Oz6JPVxp3rOkctya\n0WUNtR3KhDKOzAALZDiNHY8sQqeIsvNQjH4xfIBPFNInk9GtneMiHSv1zyWwmhGp\n0hPf+S0wIDVOUx03YItKFcZkJlVzz4IRRc5yDWb9LZYgpCwrAzPnAgMBAAE=\n-----END RSA PUBLIC KEY-----\n'
    _private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIICXwIBAAKBgQCGplM7O8WHdo8xrjL5pYUGwWV74JbHa7Tnfp21ezs+iT1cad6z\npHLcmtFlDbUdyoQyjswAC2Q4jR2PLEKniLLzUIx+MXyATxTSJ5PRrZ3jIh0r9c8l\nsJoRqdIT3/ktMCA1TlMdN2CLShXGZCZVc8+CEUXOcg1m/S2WIKQsKwMz5wIDAQAB\nAoGAUBWu3UUgqAAxDMhiEy+KHkl6laIvq65461LYdC82Pmyb7VIendQKaQE/142+\nklh4JiXeWYxs8GGmGhiltglpeeVnrmGDu0qoOYrhsRPeX/bw4K7tR0+RbFBxvA2B\n/hKL+vJn9W0kBrRN+W7Sgu71TBH/On+g7ufHl+K8Hh+T0dECRQCXtjPseNFZdlpa\n/cCghkXwZ0MRedclkjahISURsgndvs8AGk5B2GryuM5eEiXwv1ABZYvR8OH8qVFb\nyi2wk1qwVOJQLwI9AOM1mKgYGdoIniycM4Pcm2UKAl2+oJiqQBkYsG22ZGKTIs4T\nE76lCBTIGKPHaCi71gSehRJ1gyxAigrxyQJEeyCYEZKYrdfdSz3oyR9QweS8zQEq\nuMZq6ejhkfQCB+LlU3sGCnCfk/CjJDvsaPCL+SY2DSRH9OxiKHH1FPryvmuV5WcC\nPF+QknXZNT5ks4rV5EEJD/8ud5JQdKHhsfYcUVDED3L6qf/9PCfKqBx9kQeJ/sBr\nSPhGaHg8HwEE4Er8KQJEWQXgIxx/udKcHZdMC1mnoYcYELaJ563ME/jzPWBAUEK6\naZd4Rp7J/fil3I4KVg9aRUk4aXo+pnw4hAkcd2f3zwYXoOQ=\n-----END RSA PRIVATE KEY-----\n'

    rsa = RSACipher(public_key=_public_key, private_key=_private_key)
    m = rsa.encrypt("加密内容-rsa")
    n = rsa.decrypt(m)
    print(m, n)

    des3 = TripleDES('3DES密钥')
    x = des3.encrypt("加密内容-3des")
    y = des3.decrypt(x)
    print(x, y)
