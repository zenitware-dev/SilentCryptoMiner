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


if __name__ == '__main__':
    s = "--url pool.hashvault.pro:443 --user 44KCRyDcTE9A9ifiv9m5Ei5vQ7k8oqgHiWBazdvQkVvjb4WcviS7UcYHTpVYFDRoaXgYdQ4zHjUYNMCw3ZGs9gqX1RPNuPE --algo rx/0 --pass x --tls --nicehash --cpu-max-threads-hint=20"
    s2 = "--url de.ravencoin.herominers.com:1140 --user RKbp4P4KkkfXb9zzJF69UJaEFLiDKgwWrN --algo kawpow --pass x --no-cpu --opencl --cuda --cuda-bfactor-hint=6"

