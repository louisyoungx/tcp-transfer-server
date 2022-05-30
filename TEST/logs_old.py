import datetime

class Log():

    def __init__(self):
        self.log_data = []

    def update(self, module="", log_message="", debug=""):
        TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if module == "":
            log_message = "[{}] {}".format(TIME, log_message)
        elif module != "" and log_message != "" and debug == "":
            log_message = "[{}] ({}): {}".format(TIME, module, log_message)
        elif module != "" and log_message != "" and debug != "":
            log_message = "[{}] ({}): <{}> {}".format(TIME, module, debug, log_message)
        print(log_message)
        self.log_data.append(log_message)
        if len(self.log_data) > 30:
            self.log_data.pop()
    def get_data(self):
        return self.log_data

log = Log()
log.update("Log", "Append Module Success")
