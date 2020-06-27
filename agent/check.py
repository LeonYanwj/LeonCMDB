# -*- coding:UTF-8 -*-

class Man(object):
    def __init__(self):
        pass

    def a(self):
        self.name = "Leonyan"
        self.b()

    def b(self):

        print(self.name)

m = Man()

m.a()