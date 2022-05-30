import os

# 返回码
class ErrorCode(object):
    OK = "HTTP/1.1 200 OK\r\n"
    NOT_FOUND = "HTTP/1.1 404.html Not Found\r\n"

# Content类型
class ContentType(object):
    HTML = 'Content-Type: text/html\r\n'
    CSS = "Content-Type: text/css\r\n"
    JavaScript = "Content-Type: application/javascript\r\n"
    PNG = 'Content-Type: img/png\r\n'

class HttpRequest(object):
    RootDir = os.getcwd() + "/Static"   # 根目录
    NotFoundHtml = RootDir+'/404.html.html'  # 404页面

    def __init__(self):
        self.method = None
        self.url = None
        self.protocol = None
        self.host = None
        self.request_data = None
        self.response_line = ErrorCode.OK  # 响应码
        self.response_head = ContentType.HTML # 响应头部
        self.response_body = '' # 响应主题
        
    # 解析请求，得到请求的信息
    def pass_request(self, request):
        request_line, body = request.split('\r\n', 1)
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        self.url = header_list[1]
        # print self.url
        self.protocol = header_list[2]
        # 获得请求参数
        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            parameters = request_body.split('\n')   # 每一行是一个字段
            for i in parameters:
                key, val = i.split('=')
                self.request_data[key] = val
            self.handle_file_request(HttpRequest.RootDir + self.url)
        if self.method == 'GET':
            file_name = ''
            # 获取get参数
            if self.url.find('?') != -1:
                self.request_data = {}
                req = self.url.split('?', 1)[1]
                file_name = self.url.split('?', 1)[0]
                parameters = req.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.request_data[key] = val
            else:
                file_name = self.url
                # self.handle_keywords_request()
            if len(self.url) == 1:  # 如果是根目录
                file_name = '/index.html'
            file_path = HttpRequest.RootDir + file_name
            self.handle_file_request(file_path)

    # 处理请求
    def handle_file_request(self, file_path):
        # 如果找不到的话输出404
        if not os.path.isfile(file_path):
            f = open(HttpRequest.NotFoundHtml, 'r')
            self.response_line = ErrorCode.NOT_FOUND
            self.response_head = ContentType.HTML
            self.response_body = f.read()
        else:
            f = None
            self.response_line = ErrorCode.OK
            extension_name = os.path.splitext(file_path)[1] # 扩展名
            # 图片资源需要使用二进制读取
            if extension_name == '.png':
                f = open(file_path, 'rb')
                self.response_head = ContentType.PNG
                self.response_body = f.read()
            # 执行CGI，将请求转发到本地的python脚本
            elif extension_name == '.py':
                file_path = file_path.split('.', 1)[0]
                file_path = file_path.replace('/', '.')
                m = __import__(file_path)
                self.response_head = ContentType.HTML
                self.response_body = m.main.app(self.request_data)
            # 其他静态文件
            else:
                f = open(file_path, 'r')
                self.response_head = ContentType.HTML
                self.response_body = f.read()

    def get_response(self):
        return self.response_line+self.response_head+'\r\n'+self.response_body