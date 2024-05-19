from .part_of_speech import base_part_of_speech
from .constant import *

# предлог
class Preposition(base_part_of_speech):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return super().__str__()

# союз
class Conjunction(base_part_of_speech):
    def __init__(self):
        super().__init__()
        # метки
        self.labels = {
            PRNT: 0   # вводное слово
        }
        # метки на русском
        self.labels_ru = {
            PRNT: PRNT_RU
        }
    def __str__(self):
        string = super().__str__()
        labels = ""
        labels += self.feature_to_string(LABELS, self.labels, self.labels_ru)
        return string + labels

# частица
class Particle(base_part_of_speech):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return super().__str__()

# междометие
class Interjection(base_part_of_speech):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return super().__str__()

# другие токены
class Other(base_part_of_speech):
    def __init__(self):
        super().__init__()
        # метки
        self.labels = {
            LATN: 0,  # токен состоит из латинских букв
            PNCT: 0,  # пунктуация
            NUMB: 0,  # число
            ROMN: 0,  # римское число
        }
        # метки на русском
        self.labels_ru = {
            LATN: LATN_RU,  # токен состоит из латинских букв
            PNCT: PNCT_RU,  # пунктуация
            NUMB: NUMB_RU,  # число
            ROMN: ROMN_RU,  # римское число
        }
    
    def __str__(self):
        string = super().__str__()
        labels = ""
        labels += self.feature_to_string(LABELS, self.labels, self.labels_ru)
        return string + labels

# неопознанный токен
class Unknown(base_part_of_speech):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return super().__str__()
