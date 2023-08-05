from .input import Input

class TextInput(Input):
    def __init__(self, id, label, default=None, placeholder=None):
        super().__init__(id, label, "text", default, placeholder)
