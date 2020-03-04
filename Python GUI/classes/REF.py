#Define Ref Instead of define pointer in python
class ref:
    def __init__(self, obj): self.obj = obj
    def get(self):    return self.obj
    def set(self, obj):      self.obj = obj
