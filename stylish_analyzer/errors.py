from .for_analyzers.constant import LONG
class Error():
    def __init__(self, text: tuple, style: list, description: str, tips: str):
        self.text = text
        self.style = style
        self.description = description
        self.tips = tips

class ErrorList():
    def __init__(self):
        self.count = 0
        self.error_list = []

    def __add__(self, other):
        return str(self) + str(other)

    def add(self, text: tuple, style: set, description: str, tips):
        err = Error(text, style, description, tips)
        self.error_list.append(err)
        self.count += 1

    def remove(self, allowed_style_set: set):
        i = 0
        while i < self.count:
            if self.error_list[i].style <= allowed_style_set:
                self.error_list.pop(i)
                self.count -= 1
            else:
                i += 1

    def __str__(self):
        string = ''
        for i in range(0, self.count):
            if self.error_list[i].description == LONG:
                string += f'Предложение:\t"{self.error_list[i].text[0]}"\t'
            elif self.error_list[i].text[0] == "":
                string += f'В тексте:\t"{self.error_list[i].text[1]}"\t'
            else:
                string += f'В предложении:\t"{self.error_list[i].text[0]}"\t'

            string += f'{self.error_list[i].description}'
            if self.error_list[i].text[1] != "" and self.error_list[i].text[0] != "":
                string += f': {self.error_list[i].text[1]}'
            if self.error_list[i].tips != "":
                string += f' — {self.error_list[i].tips}'
            string += '\n\n'
        return string
