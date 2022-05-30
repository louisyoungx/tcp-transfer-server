james = {
    'name': 'james',
    'age': 32,
    'hobby': "football",
    'skills': {
        'html': 'HTML5',
        'css': 'CSS3',
        'js': {
            'ecma': 'ECMA',
            'dom': 'DOM',
            'bom': 'BOM'
        }
    }
}


class Reactive(dict):
    def __init__(self, target):
        print('init')
        super().__init__(target)
        self.target = target
        self.react()

    def react(self):
        for key in self.target:
            if type(self.target[key]) == dict:
                self.target[key] = Reactive(self.target[key])

    def __getitem__(self, key):
        return self.target[key]

    def __setitem__(self, key, value):
        print(f"setter - {{ {key}: {value} }}")
        if type(value) == dict:
            self.target[key] = Reactive(value)
        else:
            self.target[key] = value

    def read(self):
        return str(self.target)


if __name__ == "__main__":
    test = Reactive(james)
    print(test.read())
    test['skills']['js']['ecma'] = 'ECMA7'
    print(test['skills']['js']['ecma'])
    print(test.read())
