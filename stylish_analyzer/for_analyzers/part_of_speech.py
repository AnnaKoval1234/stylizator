# абстрактный класс для частей речи
# https://opencorpora.org/dict.php?act=gram

class base_part_of_speech():
    def __init__(self):
        self.count = 0
    def __str__(self):
        return "количество = " + str(self.count) + "\n"
    def feature_to_string(self, name_of_dictionary, dictionary_en, dictionary_ru):
        string = ""
        string += f'{name_of_dictionary}' + " = { "
        for key, value in dictionary_en.items():
            if value != 0:
                string += f'{dictionary_ru[key]}: {value}' + "; "
        string += " }"
        string += "\n"
        return string
