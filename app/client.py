import hashlib
import string
import random
import time

from instagram_web_api import Client

# просто Client не работает, поэтому переопределена функция _extract_rhx_gis для захода в web инста
class MyClient(Client):
    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode())


def getWebAPI(username, password):
    # ждем некоторое время, так как нельзя подряд делать бесконечное число http-запросов
    time.sleep(3)
    return MyClient(auto_patch=True, authenticate=True, username=username, password=password)
