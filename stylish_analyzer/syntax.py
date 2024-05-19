# https://universaldependencies.org/ru/dep/
# root - сказуемое (обычно глагол)
# acl, acl:relcl - сказуемое придаточного предложения либо причастие, зависит от подлежащего
# advcl - деепричастие, инфинитив или придаточная часть (?), в предложении играет роль обстоятельства
# xcomp - составная часть сказуемого
# ccomp - сказуемое придаточного предложения
# aux, aux:pass, cop - вспомогательный глагол "быть", разница в том, что cop используется в именном сказуемом
# parataxis - сказуемое, обычно используется в цитатах и диалогах ("сказал он", "ответила она"), а также слово в скобках
# nsubj, nsubj:pass, csubj, csubj:pass - подлежащее (именное и инфинитив соответственно)
# appos - уточняющие подлежащего (в предложении "Пришел Михаил, мой брат" слово "брат" является appos)
# nummod:gov - числительное-подлежащее
# nummod, nummod:entity - числительное-дополнение/определение
# obj, iobj - дополнение (существительное)
# advmod - обстоятельство (наречие)
# obl, obl:agent - обстоятельство (существительное в творительном падеже)
# amod, det - определение (прилагательное и местоименное прилагательное)
# nmod - определение (существительное)
# conj - однородные члены предложения
# dislocated - необычное построение предложения ("Он никогда мне не нравился, этот Миша.")
# expl - связка "это"
# mark - подчинительный союз
# cc - сочинительный союз
# case - предлог
# fixed - производный предлог
# vocative - обращение
# discourse - междометие
# flat - используется в ФИО, адресах и дате ("Владимир Владимирович Путин", "31 декабря", "ул. Гагарина 35")
# list - цепочка элементов, как, например, номер телефона или слоги, записанные через дефис
# compound - составное слово ("Жар птица", "бизнес центр")
# orphan - пропуск в неполных предложениях ("Павел заказал говядину, а Мария - свинину.")
# goeswith, reparandum - разрыв или перенос слова
# punct - пунктуация
# dep - не определено
import pymorphy2
# from .for_analyzers.sentence import Token as MyToken, Sentence as MySentence
from .for_analyzers.functional import *
from .for_analyzers.constant import *
from .errors import *

class SyntaxAnalyzer:
    def __init__(self) -> None:
        self.morph_tagger = pymorphy2.MorphAnalyzer()
        self.previous_sentence = ""
        self.number_of_sentences = 0
        self.length_of_sentences = {}
        self.parcellation = {}
        self.style = ""
        self.errors = ErrorList()

        self.sentences = {
            # по цели высказывания
            BY_PURPOSE: {
                NARRATIVE: 0,       # повествовательные
                INTERROGATIVE: 0,   # вопросительные
                INCENTIVE: 0,       # побудительные
            },
            # по интонации
            BY_INTONATION: {
                EXCLAMATION: 0,     # восклицательные
                NON_EXCLAMATION: 0, # невосклицательные
            },
            # по количеству грамматических основ
            BY_GRAMM_BASIS_NUM: {
                SIMPLE: 0,  # простые
                COMPLEX: 0, # сложные
            },
            # по виду связи в сложных предложениях
            BY_COMPLEX_TYPE: {
                COMPLEX_CCONJ: 0,       # ССП
                COMPLEX_SCONJ: 0,       # СПП
                COMPLEX_NON_CONJ: 0,    # БСП
                COMPLEX_MIXED: 0,       # с разными видами связи
            },
            # по осложненности
            BY_COMPLICATION: {
                NOT_COMPLICATED: 0,     # не осложнено
                HOMO_MEMBERS: 0,        # однородными членами
                PRTF_GRND_PHRASES: 0,   # причастными/деепричастными оборотами
                INTRO_WORDS: 0,         # вводными словами
                VOCT_WORDS: 0,          # обращениями
            },
            # по строению грамматических основ
            BY_GRAMM_BASIS_STRUCT: {
                TWO_PART: 0,    # двусоставные
                ONE_PART: 0,    # односоставные
            },
            # по распространенности
            BY_PREVALENCE: {
                COMMON: 0,      # распространенные
                NON_COMMON: 0,  # нераспространенные
            },
            # по наличию необходимых членов
            BY_PRESENCE_NECESSARY_MEMBERS: {
                COMPLETE: 0,    # полные
                INCOMPLETE: 0,  # неполные
            }
        }
        self.features = {
            INVERSION: 0,       # инверсия
            PARCELLATION: 0,    # парцелляция
            BEGIN_CONJ: 0,      # союз в начале
            SENTENCE_WORD: 0,   # слово-предложение
            SHORT: 0,           # короткое предложение
            LONG: 0,            # длинное предложение
            PASSIVE: 0,         # пассивные конструкции
            CASE_STRINGING: 0,  # нанизывание падежей
            ANONYMOUS: 0,       # безличное предложение
            MANY_CONJ: 0,       # много однородных членов
        }
        
    def __str__(self):
        string = ""
        string += "всего предложений: " + str(self.number_of_sentences) + "\n\n"
        for key, value in self.sentences.items():
            string += key + ": { "
            for value_key, value_value in value.items():
                string += value_key + ": " + str(value_value) + "; "
            string += "}\n\n"
        return string

    def count_sent(self, my_sentence):
        self.number_of_sentences += 1
        self.length_of_sentences[self.number_of_sentences] = my_sentence.length

        case_stringing= []

        # считаем общие характеристики предложений
        # цель высказывания
        if my_sentence.is_exists_morph_tag(IMPR):
            self.sentences[BY_PURPOSE][INCENTIVE] += 1
        else:
            if my_sentence[-1].text == "?!" or my_sentence[-1].text == "!?" or my_sentence[-1].text == "?":
                self.sentences[BY_PURPOSE][INTERROGATIVE] += 1
            else:
                self.sentences[BY_PURPOSE][NARRATIVE] += 1
        
        # интонация
        if my_sentence[-1].text == "?!" or my_sentence[-1].text == "!?" or my_sentence[-1].text == "!":
            self.sentences[BY_INTONATION][EXCLAMATION] += 1
        else:
            self.sentences[BY_INTONATION][NON_EXCLAMATION] += 1

        num_subj = my_sentence.number_of_subjects()
        num_pred = my_sentence.number_of_predicates()
        # количество грамматических основ
        if num_subj > 1 and num_pred > 1:
            self.sentences[BY_GRAMM_BASIS_NUM][COMPLEX] += 1
            # вид связи между сп
            if CC in my_sentence.rel_list and MARK not in my_sentence.rel_list:
                self.sentences[BY_COMPLEX_TYPE][COMPLEX_CCONJ] += 1
            elif CC not in my_sentence.rel_list and MARK in my_sentence.rel_list:
                self.sentences[BY_COMPLEX_TYPE][COMPLEX_SCONJ] += 1
            elif CC in my_sentence.rel_list and MARK in my_sentence.rel_list:
                self.sentences[BY_COMPLEX_TYPE][COMPLEX_MIXED] += 1
            else:
                self.sentences[BY_COMPLEX_TYPE][COMPLEX_NON_CONJ] += 1
        else:
            self.sentences[BY_GRAMM_BASIS_NUM][SIMPLE] += 1
            # одно- и двусоставные
            if num_subj == 1 and num_pred >= 1 or num_subj >= 1 and num_pred == 1:
                self.sentences[BY_GRAMM_BASIS_STRUCT][TWO_PART] += 1
            elif num_subj == 0 or num_pred == 0:
                self.sentences[BY_GRAMM_BASIS_STRUCT][ONE_PART] += 1

                # парцелляция
                if my_sentence.length < 5:
                    if self.number_of_sentences - 1 != 0:
                        if self.length_of_sentences[self.number_of_sentences - 1] < 5:
                            self.parcellation[self.number_of_sentences - 1] = self.previous_sentence
                            self.parcellation[self.number_of_sentences] = my_sentence.text

                # безличные, неопределенно-личные, обощенно-личные предложения
                if num_pred > 0:
                    root = my_sentence.get_token_rel(ROOT)
                    if root.pos.POS == VERB:
                        if root.pos.number == SING:
                            if root.pos.person == PER3:
                                self.features[ANONYMOUS] += 1
                        else:
                            if root.pos.person == PER1 or root.pos.person == PER3:
                                self.features[ANONYMOUS] += 1
            
            # распространенные/нераспространенные
            if my_sentence.is_exists_minor_members_of_sentence():
                self.sentences[BY_PREVALENCE][COMMON] += 1
            else:
                self.sentences[BY_PREVALENCE][NON_COMMON] += 1

        # осложненность
        is_compicated = False
        if CONJ_REL in my_sentence.rel_list:
            self.sentences[BY_COMPLICATION][HOMO_MEMBERS] += 1
            conj = 0
            for rel in my_sentence.rel_list:
                if rel == CONJ_REL:
                    conj += 1
            if conj >= 10:
                self.features[MANY_CONJ] += 1
                    
            is_compicated = True
        if ACL in my_sentence.rel_list:
            acl = my_sentence.get_token_rel(ACL)
            if acl.pos.POS == PRTF:
                if my_sentence.has_children(acl.id):
                    self.sentences[BY_COMPLICATION][PRTF_GRND_PHRASES] += 1
                    is_compicated = True
        elif ADVCL in my_sentence.rel_list:
            advcl = my_sentence.get_token_rel(ADVCL)
            if advcl.pos.POS == GRND:
                self.sentences[BY_COMPLICATION][PRTF_GRND_PHRASES] += 1
                is_compicated = True
        if my_sentence.is_exists_morph_tag(PRNT):
            self.sentences[BY_COMPLICATION][INTRO_WORDS] += 1
            is_compicated = True
        if my_sentence.is_exists_morph_tag(VOCT):
            self.sentences[BY_COMPLICATION][VOCT_WORDS] += 1
            is_compicated = True
        if not is_compicated:
            self.sentences[BY_COMPLICATION][NOT_COMPLICATED] += 1
        
        # полнота
        if ORPHAN in my_sentence.rel_list:
            self.sentences[BY_PRESENCE_NECESSARY_MEMBERS][INCOMPLETE] += 1
        else:
            self.sentences[BY_PRESENCE_NECESSARY_MEMBERS][COMPLETE] += 1
        
        # союз в начале предложения
        if my_sentence[0].rel == CC:
            self.features[BEGIN_CONJ] += 1
            self.errors.add((my_sentence.text, ""), 
                            STYLE_SET - {CONVERSATIONAL, BELLES_LETTRES}, 
                            BEGIN_CONJ, "если он не задумывался, то лучше убрать")
        
        # пассивные конструкции
        if NSUBJ_PASS in my_sentence.rel_list or CSUBJ_PASS in my_sentence.rel_list:
            self.features[PASSIVE] += 1
            self.errors.add((my_sentence.text, ""), 
                            STYLE_SET - {SCIENTIFIC, SCIENCE_OFF, OFFICIAL}, 
                            PASSIVE, "попробуйте переделать в действительный")
        elif AUX_PASS in my_sentence.rel_list or OBL_AGENT in my_sentence.rel_list:
            self.features[PASSIVE] += 1
            self.errors.add((my_sentence.text, ""), 
                            STYLE_SET - {SCIENTIFIC, SCIENCE_OFF, OFFICIAL}, 
                            PASSIVE, "попробуйте переделать в действительный")

        # инверсия
        if num_subj == 1 and num_pred == 1:
            if NSUBJ in my_sentence.rel_list and ROOT in my_sentence.rel_list:
                nsubj = my_sentence.get_token_rel(NSUBJ)
                root = my_sentence.get_parent(nsubj.head_id)
                if nsubj.id > root.id:
                    self.features[INVERSION] += 1
                    self.errors.add((my_sentence.text, ""), 
                                {SCIENTIFIC, SCIENCE_OFF, OFFICIAL},
                                INVERSION, "попробуйте переставить слова")
            # else:
            #     for s_mod in NUMMOD, AMOD, DET:
            #         if s_mod in my_sentence.rel_list:
            #             mod = my_sentence.get_token_rel(s_mod)
            #             if mod.id > my_sentence.get_parent(mod.id).id:
            #                 self.features[INVERSION] += 1
            #                 self.errors.add((my_sentence.text, ""), 
            #                     {SCIENTIFIC, SCIENCE_OFF, OFFICIAL},
            #                     INVERSION, "попробуйте переставить слова")
            #     for s_add in NMOD, OBJ, IOBJ, OBL, OBL_AGENT:
            #         if s_add in my_sentence.rel_list:
            #             add = my_sentence.get_token_rel(s_add)
            #             if add.id < my_sentence.get_parent(add.id).id:
            #                     self.features[INVERSION] += 1
            #                     self.errors.add((my_sentence.text, ""), 
            #                     {SCIENTIFIC, SCIENCE_OFF, OFFICIAL},
            #                     INVERSION, "попробуйте переставить слова")

        # нанизывание падежей
        for i in range(0, my_sentence.count):
            if my_sentence[i].rel == NMOD and my_sentence[i].pos.POS == NOUN:
                if len(case_stringing) == 0 or case_stringing[-1] == i - 1:
                    case_stringing.append(i)
            else:
                if len(case_stringing) == 1:
                    case_stringing.clear()
                elif len(case_stringing) > 2:
                    self.features[CASE_STRINGING] += 1
                    
                    str = ""
                    for j in case_stringing:
                        str += my_sentence.text_list[j] + " "
                    self.errors.add((my_sentence.text, str),
                                STYLE_SET - {OFFICIAL, SCIENCE_OFF},
                                CASE_STRINGING, "лучше перефразировать")
                    break

        # избыток придаточных
        acl_relcl_count = 0
        acl_relcl_head_set = {-1}
        acl_count = 0
        advcl_count = 0
        for i in range(0, my_sentence.count):
            if my_sentence[i].rel == ACL_RELCL or my_sentence[i].rel == CCOMP:
                acl_relcl_count += 1
                acl_relcl_head_set.add(my_sentence.get_parent(i+1).id)
            elif my_sentence[i].rel == ACL and my_sentence[i].pos.POS == PRTF:
                acl_count += 1
            elif my_sentence[i].pos.POS == GRND:
                advcl_count += 1
        acl_relcl_head_set.remove(-1)
        if acl_relcl_count - len(acl_relcl_head_set) >= 2:
            self.errors.add((my_sentence.text, ""),
                                STYLE_SET,
                                "избыток придаточных", "лучше переcтроить")
        if acl_count >= 2:
            self.errors.add((my_sentence.text, ""),
                                STYLE_SET,
                                "много причастий", "лучше переcтроить")
        if advcl_count >= 2:
            self.errors.add((my_sentence.text, ""),
                                STYLE_SET,
                                "много деепричастий", "лучше переcтроить")
        
        # короткие/длинные предложения
        if my_sentence.length <= 2:
            if self.number_of_sentences not in self.parcellation.keys():
                self.features[SENTENCE_WORD] += 1
        if my_sentence.length < 5:
            self.features[SHORT] += 1
                
        elif my_sentence.length >= 25:
            self.features[LONG] += 1
            self.errors.add((my_sentence.text, ""), STYLE_SET - {OFFICIAL, SCIENCE_OFF, SCIENTIFIC}, 
                            LONG, "лучше сократить или разделить предложение на два")

        self.previous_sentence = my_sentence.text

    def analyze(self):
        conversational = 0
        official = 0
        scientific = 0
        publicistic = 0
        
        purpose = self.sentences[BY_PURPOSE]
        intonation = self.sentences[BY_INTONATION]
        gramm_basis_num = self.sentences[BY_GRAMM_BASIS_NUM]
        complex_type = self.sentences[BY_COMPLEX_TYPE]
        complication = self.sentences[BY_COMPLICATION]
        necessary_members = self.sentences[BY_PRESENCE_NECESSARY_MEMBERS]

        # длина предложений
        if self.features[SENTENCE_WORD] > 0:
            conversational += 1
        elif self.features[LONG] > 0:
            official += 1
            scientific += 1

        # простые, ссп, спп, бсп
        if ge_critical(gramm_basis_num[SIMPLE], self.number_of_sentences, 75):
            if ge_critical(self.features[SHORT], gramm_basis_num[SIMPLE], 33):
                conversational += 1
        elif ge_critical(gramm_basis_num[COMPLEX], self.number_of_sentences, 50):
            if ge_critical(complex_type[COMPLEX_CCONJ] + complex_type[COMPLEX_SCONJ], gramm_basis_num[COMPLEX], 75):
                scientific += 1
            elif ge_critical(complex_type[COMPLEX_NON_CONJ], gramm_basis_num[COMPLEX], 75):
                publicistic += 1

        # восклицательные предложения
        if intonation[EXCLAMATION] > 0:
            conversational += 1
            publicistic += 1

        # вопросительные предложения
        if ge_critical(purpose[INTERROGATIVE], self.number_of_sentences, 20):
            conversational += 1
            publicistic += 1

        # инверсия
        if self.features[INVERSION] > 0:
            publicistic += 1
            conversational += 1

        # парцелляция
        if len(self.parcellation.keys()) > 0:
            self.features[PARCELLATION] += 1
            str = ""
            for value in self.parcellation.values():
                str += value + " "
            self.errors.add(("", str), {OFFICIAL, SCIENCE_OFF, SCIENTIFIC}, PARCELLATION, 
                            "если она не задумывалась, то лучше объединить в одно предложение")

        # парцелляция
        if self.features[PARCELLATION] > 0:
            publicistic += 1
            conversational += 1

        # неполные предложения
        if necessary_members[INCOMPLETE] > 0:
            publicistic += 1
            conversational += 1

        # побудительные
        if ge_critical(purpose[INCENTIVE], self.number_of_sentences, 40):
            publicistic += 1
        elif ge_critical(purpose[INCENTIVE], self.number_of_sentences, 20):
            official += 1

        # пассивные и осложненные причастными/деепричастными оборотами
        if ge_critical(self.features[PASSIVE], self.number_of_sentences, 66):
            official += 1
            scientific += 1
        if ge_critical(complication[PRTF_GRND_PHRASES], self.number_of_sentences, 66):
            official += 1
            scientific += 1

        # безличные
        if self.features[ANONYMOUS] > 0:
            scientific += 1

        # нанизывание падежей
        if self.features[CASE_STRINGING] > 0:
            official += 1

        # обращения
        if self.sentences[BY_COMPLICATION][VOCT_WORDS] > 0:
            publicistic += 1
            conversational += 1

        # однородные члены предложения
        if self.sentences[BY_COMPLICATION][HOMO_MEMBERS] > 0:
            if self.features[MANY_CONJ] > 0:
                official += 1

        self.style = get_style(conversational, scientific, official, publicistic)
