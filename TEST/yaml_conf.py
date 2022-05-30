import yaml
import os


class Direct(object):
    def __init__(self, target):
        for key in target:
            if type(target[key]) == dict:
                child = Direct(target[key])
                exec(f'self.{key} = child')
            else:
                exec(f'self.{key} = target[key]')


class Config(object):

    def __init__(self):
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file = self.path + '/TEST/config.yaml'
        self.data = self.read()
        self.data['path'] = self.path
        self.direct = Direct(self.data)

    def read(self):
        # 打开yaml文件
        file = open(self.file, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()
        # 将字符串转化为字典或列表
        return yaml.full_load(file_data)


config = Config().direct
print(config.Scheduler.time)
print(config.path)
