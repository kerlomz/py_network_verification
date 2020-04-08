#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import rsa

(client_public_key, server_private_key) = rsa.newkeys(1024)
(server_public_key, client_private_key) = rsa.newkeys(1024)

SPLIT_FLAG = "|'''--''?\\\\%&SPLIT_FLAG&%\\\\?''--'''|"
AES_KEY = "123456"
DES3_KEY = "123456"
CLIENT_PUBLIC_KEY = client_public_key.save_pkcs1().decode()
CLIENT_PRIVATE_KEY = client_private_key.save_pkcs1().decode()
SERVER_PUBLIC_KEY = server_public_key.save_pkcs1().decode()
SERVER_PRIVATE_KEY = server_private_key.save_pkcs1().decode()

CLIENT_CONF = """
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

SPLIT_FLAG = "{SPLIT_FLAG}"
AES_KEY = '{AES_KEY}'
DES3_KEY = '{DES3_KEY}'
PUBLIC_KEY = '{CLIENT_PUBLIC_KEY}'
PRIVATE_KEY = '{CLIENT_PRIVATE_KEY}'
""".format(
    SPLIT_FLAG=SPLIT_FLAG,
    AES_KEY=AES_KEY,
    DES3_KEY=DES3_KEY,
    CLIENT_PUBLIC_KEY=CLIENT_PUBLIC_KEY.replace("\n", "\\n"),
    CLIENT_PRIVATE_KEY=CLIENT_PRIVATE_KEY.replace("\n", "\\n")
)


SERVER_CONF = """
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

SPLIT_FLAG = "{SPLIT_FLAG}"
AES_KEY = '{AES_KEY}'
DES3_KEY = '{DES3_KEY}'
PUBLIC_KEY = '{SERVER_PUBLIC_KEY}'
PRIVATE_KEY = '{SERVER_PRIVATE_KEY}'
""".format(
    SPLIT_FLAG=SPLIT_FLAG,
    AES_KEY=AES_KEY,
    DES3_KEY=DES3_KEY,
    SERVER_PUBLIC_KEY=SERVER_PUBLIC_KEY.replace("\n", "\\n"),
    SERVER_PRIVATE_KEY=SERVER_PRIVATE_KEY.replace("\n", "\\n")
)
print(CLIENT_CONF)
with open("nv_client/nv/constants.pyx", "w", encoding="utf8") as f:
    f.write(CLIENT_CONF)

print(SERVER_CONF)
with open("nv_backend/constants.py", "w", encoding="utf8") as f:
    f.write(SERVER_CONF)