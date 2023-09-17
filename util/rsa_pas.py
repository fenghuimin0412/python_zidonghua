import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA


def _encrpt(string, public_key):
    rsakey = RSA.importKey(public_key)  # 读取公钥
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    # 因为encryptor.encrypt方法其内部就实现了加密再次Base64加密的过程，所以这里实际是通过下面的1和2完成了JSEncrypt的加密方法
    encrypt_text = cipher.encrypt(string.encode())  # 1.对账号密码组成的字符串加密
    cipher_text_tmp = base64.b64encode(encrypt_text)  # 2.对加密后的字符串base64加密
    return cipher_text_tmp.decode()


# 使用公钥加密
def gen_body(pwd, public_key=None):
    '''根据账号密码生成请求的body然后调用_encrpt方法加密'''
    if not public_key: public_key = '输入公钥'  # 输入对应的公钥
    key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
    encrypt_res = _encrpt(pwd, key)
    return encrypt_res


if __name__ == '__main__':
    PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAk8fEwBXx7pNAx7L6eUMwLDb7g2d04cCFakT07GRBnwBZGftkImKh86tRJHeIserYkvXEmQN3oPmr2J/r6Z7fco5yO5WS02sufOJ6PmAkAvE1efXZNZ042S41HNwz0CyTLcimJdSwR5PmOoDd88NZYmTiHorkW6bFzNLaIiMQUm+wtbDiDtObo/IvIGMRBZK9QhVu+8gl6UOkg+zRQtnnpOV6FoDGDCXLIdMgHZBN2dBSNpbsuFH4yebzC1Bd+podCcOMPBEub4QlIwWnfhRutdvZfXbOGX7fa1i4E95vJRP2CSE7h+3oW3paoRoqkqNlcQZQtYPzxY7W3Fvt1cl2kwIDAQAB"
    print(gen_body("Admin!123456", PUBLIC_KEY))  # 输入要加密的密码```