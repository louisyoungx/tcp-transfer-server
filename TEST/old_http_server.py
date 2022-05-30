"""HTTP Server Handler
This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

Document https://docs.python.org/3.9/library/http.server.html
"""
import json
import os
import time
import sys
import argparse
import posixpath
import shutil
import mimetypes
import re
import signal
from io import StringIO, BytesIO
from urllib.parse import quote
from urllib.parse import unquote
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
try:
    from html import escape
except ImportError:
    from cgi import escape

from Config import config
from Logger import logger
from Server.router import router


class RequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler with GET/HEAD/POST commands.
    """
    rootPath = config.path + config.Server.static_path
    server_version = "simple_http_server/" + config.Server.version

    # handle a GET request
    def do_GET(self):
        url = self.requestline[4:-9]
        # print(url)
        request_data = {}  # 存放GET请求数据
        try:
            if url.find('?') != -1:
                req = url.split('?', 1)[1]
                url = url.split('?', 1)[0]
                parameters = req.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    request_data[key] = val
        except Exception as e:
            logger.error("URL Format Error")
        if url == "/":
            self.home()
        elif url == "":
            self.noFound()
        elif "/api" in url:
            self.api(url[4:], request_data)
        else:
            self.file(url)

    # handle a POST request
    def do_POST(self):
        LOCAL_HOST = config.Server.local_host
        PORT = config.Server.port
        hostLen = len(f'/{LOCAL_HOST}:{PORT}') + 5
        url = self.requestline[hostLen:-9]
        request_data = json.loads(self.rfile.read(int(self.headers['content-length'])).decode())
        if url == "/":
            self.home()
        elif url == "":
            self.noFound()
        elif "/api" in url:
            self.api(url[4:], request_data)
        else:
            self.file(url)

    def log_message(self, format, *args):
        SERVER_LOGGER = config.Logger.server_logger
        if SERVER_LOGGER:
            logger.info(format % args)
        else:
            pass

    def home(self):
        file_path = self.rootPath + "/index.html"
        home_page_file = open(file_path, 'r', encoding="utf-8")
        content = str(home_page_file.read())

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode())

    def file(self, url):
        file_name = url.split("/")[-1]
        file_sys_path = self.rootPath + url[:-len(file_name)]
        file_path = ""
        for root, dirs, files in os.walk(file_sys_path):
            for file in files:
                if file == file_name:
                    file_path = os.path.join(root, file)
                else:
                    continue
        if file_path != "":
            self.send_response(200)
        if file_path == "":
            # file_path = self.rootPath + "/404.html" # Hard Code
            self.noFound()
        elif file_name[-5:] == ".html":
            self.send_header("Content-Type", "text/html")
        elif file_name[-4:] == ".css":
            self.send_header("Content-Type", "text/css")
        elif file_name[-3:] == ".js":
            self.send_header("Content-Type", "application/javascript")
        elif file_name[-4:] == ".png":  # 二进制文件
            self.send_header("Content-Type", "img/png")
            file_page_file = open(file_path, 'rb')
            self.end_headers()
            self.wfile.write(file_page_file.read())
            return
        elif file_name[-4:] == ".jpg":  # 二进制文件
            self.send_header("Content-Type", "img/jpg")
            file_page_file = open(file_path, 'rb')
            self.end_headers()
            self.wfile.write(file_page_file.read())
            return
        elif file_name[-4:] == ".ico":  # 二进制文件
            self.send_header("Content-Type", "img/ico")
            file_page_file = open(file_path, 'rb')
            self.end_headers()
            self.wfile.write(file_page_file.read())
            return
        elif file_name[-5:] == ".woff":  # 二进制文件
            self.send_header("Content-Type", "img/ico")
            file_page_file = open(file_path, 'rb')
            self.end_headers()
            self.wfile.write(file_page_file.read())
            return
        file_page_file = open(file_path, 'r', encoding="utf-8")
        content = str(file_page_file.read())
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode())

    def api(self, url, request_data):
        content = router(url, request_data)  # 此处进入路由
        localtime = time.localtime(time.time())
        date = \
            localtime.tm_year.__str__() + '-' + \
            localtime.tm_mon.__str__() + '-' + \
            localtime.tm_mday.__str__() + ' ' + \
            localtime.tm_hour.__str__() + ':' + \
            localtime.tm_min.__str__() + ':' + \
            localtime.tm_sec.__str__()
        jsonDict = {"data": content, "time": date}
        res = json.dumps(jsonDict)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(res)))
        self.end_headers()
        self.wfile.write(res.encode())

    def noFound(self):
        self.file("/404.html")
