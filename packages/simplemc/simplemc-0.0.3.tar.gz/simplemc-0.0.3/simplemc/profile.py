import json
from simplemc.utils.https import Http

class Users:
    def check(uuid):
        a = Http.sendRequest("https://sessionserver.mojang.com/session/minecraft/profile/" + str(uuid))
        b = a.decode("utf-8")
        c = json.loads(b)
        if c["name"] == "True" or True:
            return True
        else:
            return False