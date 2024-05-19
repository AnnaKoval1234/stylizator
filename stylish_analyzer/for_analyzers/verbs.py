from .part_of_speech import base_part_of_speech
from .names import base_name_with_animacy
from .constant import *

# базовый класс для глаголов
class base_verb(base_part_of_speech):
    def __init__(self):
        super().__init__()
        # вид
        self.aspect = {
            PERF: 0,  # совершенный
            IMPF: 0,  # несовершенный
        }
        # вид на русском
        self.aspect_ru = {
            PERF: PERF_RU,
            IMPF: IMPF_RU,
        }
        # переходность
        self.transitivity = {
            TRAN: 0,  # переходный
            INTR: 0,  # непереходный
        }
        # переходность на русском
        self.transitivity_ru = {
            TRAN: TRAN_RU,
            INTR: INTR_RU,
        }
        # метки
        self.labels = {
            REFL: 0,  # возвратность
            MULT: 0,  # многократный
        }
        # метки на русском
        self.label_ru = {
            REFL: REFL_RU,
            MULT: MULT_RU,
        }

    def __str__(self):
        string = base_part_of_speech.__str__(self)
        labels = ""

        string += self.feature_to_string(ASPECT, self.aspect, self.aspect_ru)
        string += self.feature_to_string(TRANSITIVITY, self.transitivity, self.transitivity_ru)

        labels += self.feature_to_string(LABELS, self.labels, self.label_ru)

        return string, labels

# базовый класс для глаголов с временем
class base_verb_with_tense(base_verb):
    def __init__(self):
        super().__init__()
        # время
        self.tense = {
            PRES: 0,  # настоящее
            PAST: 0,  # прошедшее
            FUTR: 0,  # будущее
        }
        # время на русском
        self.tense_ru = {
            PRES: PRES_RU,
            PAST: PAST_RU,
            FUTR: FUTR_RU,
        }

    def __str__(self):
        string, labels = super().__str__()
        string += self.feature_to_string(TENSE, self.tense, self.tense_ru)
        return string, labels

# класс "глагол"
class Verb(base_verb_with_tense):
    def __init__(self):
        super().__init__()
        # род
        self.gender = {
            MASC: 0,  # мужской
            FEMN: 0,  # женский
            NEUT: 0,  # средний
        }
        # род на русском
        self.gender_ru = {
            MASC: MASC_RU,
            FEMN: FEMN_RU,
            NEUT: NEUT_RU,
        }
        # совместность
        self.involvement = {
            INCL: 0,  # говорящий включён в действие
            EXCL: 0,  # говорящий не включён в действие
        }
        # совместность на русском
        self.involvement_ru = {
            INCL: INCL_RU,
            EXCL: EXCL_RU,
        }
        # наклонение
        self.mood = {
            INDC: 0,  # изъявительное
            IMPR: 0,  # повелительное
        }
        # наклонение на русском
        self.mood_ru = {
            INDC: INDC_RU,
            IMPR: IMPR_RU,
        }
        # число
        self.number = {
            SING: 0,  # единственное
            PLUR: 0,  # множественное
        }
        # число на русском
        self.number_ru = {
            SING: SING_RU,
            PLUR: PLUR_RU,
        }
        # лицо
        self.person = {
            PER1: 0,  # 1 лицо
            PER2: 0,  # 2 лицо
            PER3: 0,  # 3 лицо
        }
        self.person_ru = {
            PER1: PER1_RU,
            PER2: PER2_RU,
            PER3: PER3_RU,
        }
        # метки
        self.labels[IMPE] = 0  # безличный
        self.labels[IMPX] = 0  # возможно безличный
        # метки на русском
        self.label_ru[IMPE] = IMPE_RU
        self.label_ru[IMPX] = IMPX_RU

    def __str__(self):
        string, labels = super().__str__()
        
        string += self.feature_to_string(GENDER, self.gender, self.gender_ru)
        string += self.feature_to_string(INVOLVEMENT, self.involvement, self.involvement_ru)
        string += self.feature_to_string(MOOD, self.mood, self.mood_ru)
        string += self.feature_to_string(NUMBER, self.number, self.number_ru)
        string += self.feature_to_string(PERSON, self.person, self.person_ru)

        return string + labels

# класс "инфинитив"
class Infinitive(base_verb):
    def __init__(self):
        super().__init__()
    def __str__(self):
        string, labels = super().__str__()
        return string + labels

# класс "деепричастие"
class Gerund(base_verb_with_tense):
    def __init__(self):
        super().__init__()
        # метки
        self.labels[FIMP] = 0  # деепричастие от глагола несовершенного вида
        self.label_ru[FIMP] = FIMP_RU
    def __str__(self):
        string, labels = super().__str__()
        return string + labels

# класс "причастие"
class Participle(base_verb_with_tense, base_name_with_animacy):
    def __init__(self):
        super().__init__()
        # залог
        self.voice = {
            ACTV: 0,  # действительный
            PSSV: 0,  # страдательный
        }
        self.voice_ru = {
            ACTV: ACTV_RU,
            PSSV: PSSV_RU,
        }
    def __str__(self):
        string, labels = base_verb_with_tense.__str__(self)

        string += self.feature_to_string(VOICE, self.voice, self.voice_ru)
        string += self.feature_to_string(CASE, self.case, self.case_ru)
        string += self.feature_to_string(GENDER, self.gender, self.gender_ru)
        string += self.feature_to_string(NUMBER, self.number, self.number_ru)
        string += self.feature_to_string(ANIMACY, self.animacy, self.animacy_ru)

        return string + labels

# класс "наречие"
# обычно примыкает к глаголам, поэтому объявим его здесь
class Adverb(base_part_of_speech):
    def __init__(self):
        super().__init__()
        # метки
        self.labels = {
            PRDX: 0,  # может выступать в роли предикатива
        }
        # метки на русском
        self.label_ru = {
            PRDX: PRDX_RU,
        }

    def __str__(self):
        string = super().__str__()
        labels = ""
        labels += self.feature_to_string(LABELS, self.labels, self.label_ru)
        return string + labels

# класс "предикатив" или "категория состояния"
# обычно предстают в виде наречия, поэтому объявим его тоже здесь
class Predicative(base_part_of_speech):
    def __init__(self):
        super().__init__()
        self.tense = {
            PRES: 0,
            PAST: 0,
            FUTR: 0,
        }
        self.tense_ru = {
            PRES: PRES_RU,
            PAST: PAST_RU,
            FUTR: FUTR_RU,
        }
    def __str__(self):
        string = super().__str__()
        string += self.feature_to_string(TENSE, self.tense, self.tense_ru)
        return string
    