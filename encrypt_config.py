import pyaes
import base64

GKEY, GIV = 'XMRIG_XMRIG_XMR_', 'RX/0_RX/0_RX/0_R'
def encrypter_aes(plain_text) -> str:
    aes = pyaes.AESModeOfOperationCBC(
        GKEY.encode("ascii"),
        iv=GIV.encode("ascii")
    )

    encrypter = pyaes.Encrypter(aes)

    encrypted = (
        encrypter.feed(plain_text.encode("utf-8")) +
        encrypter.feed()
    )

    return base64.b64encode(encrypted).decode("ascii")

