from string_utils.validation import is_string
class Openwebinar:
    def __init__(self, name):
        if is_string(name):
            self.name = name
        else:
            self.name = ''

    def __str__(self):
        return self.name