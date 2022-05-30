import json
import urllib.request
from Logger import logger
from Config import config


class Message(object):
    def __init__(self):
        self.DEBUG = config.Debug.open
        self.URL = config.Message.target_server
        self.OPEN = config.Message.open

    def sender(self, url, data):
        if not self.OPEN:
            logger.warn("Message Closed")
            return
        try:
            str_data = json.dumps(data)
            byte_data = bytes(str_data, encoding='utf-8')
            response = urllib.request.urlopen(url, data=byte_data)
            mes = data["messageChain"][0]["text"].replace("\n", " ")
            if len(mes) > 10:
                mes = mes[:10] + "···"
            if self.DEBUG:
                logger.info(f'{self.URL} - {mes} - {response.read().decode("utf-8")}')
            else:
                logger.info("Send {}".format(mes))
            return True
        except Exception as e:
            if self.DEBUG:
                logger.error("Message Send Failed -", e)
            else:
                logger.error("Message Send Failed")
            return False

    def user(self, message, userid):

        path = "sendFriendMessage"
        url = "http://{}/{}".format(self.URL, path)

        data = {
            "sessionKey": "YourSession",
            "target": userid,
            "messageChain": [
                {"type": "Plain", "text": message}
            ]
        }
        return self.sender(url, data)

    def group(self, message, groupid):

        path = "sendGroupMessage"
        url = "http://{}/{}".format(self.URL, path)

        data = {
            "sessionKey": "YourSession",
            "target": groupid,
            "messageChain": [
                {"type": "Plain", "text": message}
            ]
        }
        return self.sender(url, data)
