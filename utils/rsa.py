# coding=utf-8
"""
@author: kaaokou
create_rsa_key() - 创建RSA密钥
my_encrypt_and_decrypt() - 加密解密测试
"""

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
from urllib import parse
import base64

public_key_file = "/rsa_keys/pub_rsa_key.pem"
private_key_file = "/rsa_keys/my_private_rsa_key.bin"


def create_rsa_key(code="XXXX", base_path=""):
    """创建RSA密钥"""
    # 1.生成一个密码，可以使1024或者2048位
    key = RSA.generate(1024)

    # 2.调用 RSA 密钥实例的 exportKey 方法，传入密码、使用的 PKCS 标准以及加密方案这三个参数
    encrypted_key = key.exportKey(passphrase=code, pkcs=8,
                                  protection="scryptAndAES128-CBC")
    # 3、将公钥和私钥写入磁盘的文件。
    with open(base_path + private_key_file, "wb") as f:
        f.write(encrypted_key)
    with open(base_path + public_key_file, "wb") as f:
        f.write(key.publickey().exportKey())


def decrypt_data(inputdata, code="XXXX", base_path=""):
    """解密函数，code为设置的加密密钥"""
    # 1.URL解码和base64解码
    data = base64.b64decode(parse.unquote(inputdata))
    # 2.获取私钥
    private_key = RSA.import_key(
        open(base_path + private_key_file, 'r').read(),
        passphrase=code
    )
    # 3.使用 PKCS1_v1_5，不要用 PKCS1_OAEP，使用 PKCS1_OAEP 的话，前端 jsencrypt.js 加密的数据解密不了
    cipher_rsa = PKCS1_v1_5.new(private_key)

    # 4.解密，当解密失败，会返回 sentinel，返回字符串 --> bytes 需要转 string
    sentinel = None
    ret = cipher_rsa.decrypt(data, sentinel)
    ret = ret.decode('utf-8')
    return ret


def get_public_key(base_path=""):
    """获取公钥"""
    with open(base_path + public_key_file, 'r') as file:
        public_key = file.read()
    return public_key


if __name__ == '__main__':
    # 生成密钥
    create_rsa_key()
