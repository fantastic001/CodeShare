# coding: UTF-8

class TextMessage:
    def __init__(self, text):
        self.text = text

    def set_text(self, text):
        self.text = text

    def get_message(self):
        return {'text': self.text}
