class Direct(object):
    def __init__(self, target):
        for key in target:
            if type(target[key]) == dict:
                child = Direct(target[key])
                exec(f'self.{key} = child')
            else:
                exec(f'self.{key} = target[key]')
