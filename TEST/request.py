# import json
# import urllib.request
#
#
# class Message(object):
#     def __init__(self):
#         self.DEBUG = True
#         self.URL = "www.louisyoung.site:8088"
#
#     def sender(self, url, data):
#         try:
#             str_data = json.dumps(data)
#             byte_data = bytes(str_data, encoding='utf-8')
#             response = urllib.request.urlopen(url, data=byte_data)
#             mes = data["messageChain"][0]["text"].replace("\n", " ")
#             if len(mes) > 10:
#                 mes = mes[:10] + "···"
#             if self.DEBUG:
#                 print(f'{self.URL} - {mes} - {response.read().decode("utf-8")}')
#             else:
#                 print("Send {}".format(mes))
#             return True
#         except Exception as e:
#             if self.DEBUG:
#                 print("Message Send Failed -", e)
#             else:
#                 print("Message Send Failed")
#             return False
#
#     def sendFriendMessage(self, message, userid):
#
#         path = "sendFriendMessage"
#         url = "http://{}/{}".format(self.URL, path)
#
#         data = {
#             "sessionKey": "YourSession",
#             "target": userid,
#             "messageChain": [
#                 {"type": "Plain", "text": message}
#             ]
#         }
#         return self.sender(url, data)
#
#     def sendGroupMessage(self, message, groupid):
#
#         path = "sendGroupMessage"
#         url = "http://{}/{}".format(self.URL, path)
#
#         data = {
#             "sessionKey": "YourSession",
#             "target": groupid,
#             "messageChain": [
#                 {"type": "Plain", "text": message}
#             ]
#         }
#         return self.sender(url, data)
#
#
# message = Message()
#
#
# if __name__ == "__main__":
#     message.sendFriendMessage("hello", 1462648167)
