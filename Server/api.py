from Config import config
from Logger import logger


def serverLog(request):
    file_path = config.path + config.Logger.file_path + config.Logger.file_name
    file_page_file = open(file_path, 'r')
    return str(file_page_file.read())

def serverConfig(request):
    return config.raw

def signIn(request):
    # POST example
    username = request["username"]
    password = request["password"]
    return "success"

def stop():
    logger.info("Server stopped")
    exit()
