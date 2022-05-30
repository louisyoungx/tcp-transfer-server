import os
import configparser


class Config(object):
    def __init__(self, config_file='config.ini'):
        self.rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._path = self.rootPath + "/Config/" + config_file
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def settings(self, section, name):
        return eval(self._config.get(section, name))

    def raw(self, section, name):
        return self._configRaw.get(section, name)

    def menu(self):
        menus = {}
        for module in self._config:
            modules = self._config[module]
            menus[module] = {}

            for item in modules:
                print(item.upper())
                menus[module][item.upper()] = modules[item]
                # DEBUG print(modules, item, value, type(value))
        print(menus)
        return menus

    def path(self):
        return self.rootPath


class Target(object):
    def __init__(self, target):
        for key in target:
            if type(target[key]) == dict:
                child = Target(target[key])
                exec(f'self.{key} = child')
            else:
                exec(f'self.{key} = target[key]')


_config_ = Config()
config = Target(_config_.menu())
print(config.Information.AUTHOR)
