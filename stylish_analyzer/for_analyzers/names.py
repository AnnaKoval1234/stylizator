from .part_of_speech import base_part_of_speech
from .constant import *

# базовый класс для имён
# от него наследуются все именные части речи
class base_name(base_part_of_speech): 
    def __init__(self):
        super().__init__()
        # падеж
        self.case = {
            NOMN: 0,  # именительный
            GENT: 0,  # родительный
            DATV: 0,  # дательный
            ACCS: 0,  # винительный
            ABLT: 0,  # творительный
            LOCT: 0,  # предложный
        }
        # падеж на русском
        self.case_ru = {
            NOMN: NOMN_RU,
            GENT: GENT_RU,
            DATV: DATV_RU,
            ACCS: ACCS_RU,
            ABLT: ABLT_RU,
            LOCT: LOCT_RU,
        }
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
        # метки
        self.labels = {}
        self.labels_ru = {}

    def __str__(self):
        string = super().__str__()
        labels = ""

        string += self.feature_to_string(CASE, self.case, self.case_ru)
        string += self.feature_to_string(GENDER, self.gender, self.gender_ru)
        string += self.feature_to_string(NUMBER, self.number, self.number_ru)

        labels += self.feature_to_string(LABELS, self.labels, self.labels_ru)
        return string, labels

# базовый класс для имен с одушевленностью
class base_name_with_animacy(base_name):
    def __init__(self):
        super().__init__()
        # од/неод
        self.animacy = {
            ANIM: 0,  # одушевленность
            INAN: 0,  # неодушевленность
        }
        # од/неод на русском
        self.animacy_ru = {
            ANIM: ANIM_RU,
            INAN: INAN_RU,
        }

    def __str__(self):
        string, labels = super().__str__()
        string += self.feature_to_string(ANIMACY, self.animacy, self.animacy_ru)
        return string, labels
    
# класс "существительное"
class Noun(base_name_with_animacy):
    def __init__(self):
        super().__init__()
        # еще падеж
        self.case[VOCT] = 0 # звательный
        self.case[GEN2] = 0 # второй родительный (частичный)
        self.case[ACC2] = 0 # второй винительный
        self.case[LOC2] = 0 # второй предложный (местный)
        # еще падеж на русском
        self.case_ru[VOCT] = VOCT_RU
        self.case_ru[GEN2] = GEN2_RU
        self.case_ru[ACC2] = ACC2_RU
        self.case_ru[LOC2] = LOC2_RU

        # метки
        self.labels[MSF] = 0   # общий род или колебание по роду
        self.labels[GNDR] = 0  # род не выражен
        self.labels[SGTM] = 0  # только единственное число
        self.labels[PLTM] = 0  # только множественное число
        self.labels[FIXD] = 0  # неизменяемое
        self.labels[INMX] = 0  # может использоваться как одуш. / неодуш.
        self.labels[COUN] = 0  # счётная форма
        self.labels[SUBX] = 0  # возможна субстантивация

        # метки на русском
        self.labels_ru[MSF] = MSF_RU
        self.labels_ru[GNDR] = GNDR_RU
        self.labels_ru[SGTM] = SGTM_RU
        self.labels_ru[PLTM] = PLTM_RU
        self.labels_ru[FIXD] = FIXD_RU
        self.labels_ru[INMX] = INMX_RU
        self.labels_ru[COUN] = COUN_RU
        self.labels_ru[SUBX] = SUBX_RU

    def __str__(self):
        string, labels = super().__str__()
        return string + labels

# класс "прилагательное"
class Adjective(base_name_with_animacy):
    def __init__(self):
        super().__init__()
        # метки
        self.labels[FIXD] = 0  # неизменяемое
        self.labels[SUPR] = 0  # превосходная степень
        self.labels[QUAL] = 0  # качественное
        self.labels[APRO] = 0  # местоименное
        self.labels[ANUM] = 0  # порядковое
        self.labels[POSS] = 0  # притяжательное
        self.labels[ANPH] = 0  # анафорическое (местоимение)
        self.labels[ADJX] = 0  # может выступать в роли прилагательного
        self.labels[SUBX] = 0  # возможна субстантивация
        # метки на русском
        self.labels_ru[FIXD] = FIXD_RU
        self.labels_ru[SUPR] = SUPR_RU
        self.labels_ru[QUAL] = QUAL_RU
        self.labels_ru[APRO] = APRO_RU
        self.labels_ru[ANUM] = ANUM_RU
        self.labels_ru[POSS] = POSS_RU
        self.labels_ru[ANPH] = ANPH_RU
        self.labels_ru[ADJX] = ADJX_RU
        self.labels_ru[SUBX] = SUBX_RU

    def __str__(self):
        string, labels = super().__str__()
        return string + labels

# класс "прилагательные сравнительной степени"
class Comparative(base_part_of_speech):
    def __init__(self):
        super().__init__()
        # метки
        self.labels = {
            QUAL: 0,  # качественное
            CMP2: 0,  # сравнительная степень на по-
            VEJ: 0,   # форма компаратива на -ей
        }
        # метки на русском
        self.labels_ru = {
            QUAL: QUAL_RU,  # качественное
            CMP2: CMP2_RU,  # сравнительная степень на по-
            VEJ: VEJ_RU,    # форма компаратива на -ей
        }

    def __str__(self):
        string = super().__str__()
        labels = ""
        labels += self.feature_to_string(LABELS, self.labels, self.labels_ru)
        return string + labels

# класс "местоимение"
class Pronoun(base_name):
    def __init__(self):
        super().__init__()
        # лицо
        self.person = {
            PER1: 0,  # 1 лицо
            PER2: 0,  # 2 лицо
            PER3: 0,  # 3 лицо
        }
        # лицо на русском
        self.person_ru = {
            PER1: PER1_RU,
            PER2: PER2_RU,
            PER3: PER3_RU,
        }
        # метки
        self.labels[ANPH] = 0  # анафорическое (местоимение)
        self.labels[QUES] = 0  # вопросительное
        self.labels[DMNS] = 0  # указательное
        # метки на русском
        self.labels_ru[ANPH] = ANPH_RU
        self.labels_ru[QUES] = QUES_RU
        self.labels_ru[DMNS] = DMNS_RU

    def __str__(self):
        string, labels = super().__str__()
        string += self.feature_to_string(PERSON, self.person, self.person_ru)
        return string + labels

# класс "числительное"
class Numeral(base_name_with_animacy):
    def __init__(self):
        super().__init__()
        # метки
        self.labels[COLL] = 0  # собирательное числительное
        self.labels_ru[COLL] = COLL_RU

    def __str__(self):
        string, labels = super().__str__()
        return string + labels
