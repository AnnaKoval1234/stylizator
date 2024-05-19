import pymorphy2
import re
from .for_analyzers import names
from .for_analyzers import verbs
from .for_analyzers import functional_parts_of_speech
from .for_analyzers.constant import *
from .for_analyzers.functional import *
from .errors import *

class MorphologicalAnalyzer:
    def __init__(self):
        self.morph_tagger = pymorphy2.MorphAnalyzer()
        self.number_of_sentences = 0
        self.number_of_tokens = 0
        self.number_of_words = 0
        self.style = ""
        self.errors = ErrorList()

        noun = names.Noun()
        adjf = names.Adjective()
        adjs = names.Adjective()
        comp = names.Comparative()
        numr = names.Numeral()
        npro = names.Pronoun()

        verb = verbs.Verb()
        infn = verbs.Infinitive()
        prtf = verbs.Participle()
        prts = verbs.Participle()
        grnd = verbs.Gerund()
        advb = verbs.Adverb()
        pred = verbs.Predicative()

        prep = functional_parts_of_speech.Preposition()
        conj = functional_parts_of_speech.Conjunction()
        prcl = functional_parts_of_speech.Particle()
        intj = functional_parts_of_speech.Interjection()
        x = functional_parts_of_speech.Other()
        unkn = functional_parts_of_speech.Unknown()

        self.parts_of_speech = { NOUN: noun, ADJF: adjf, ADJS: adjs, COMP: comp, VERB: verb,
                                 INFN: infn, PRTF: prtf, PRTS: prts, GRND: grnd,
                                 NUMR: numr, ADVB: advb, NPRO: npro, PRED: pred,
                                 PREP: prep, CONJ: conj, PRCL: prcl, INTJ: intj,
                                 X: x, UNKN: unkn }
        self.parts_of_speech_ru = { NOUN: NOUN_RU, ADJF: ADJF_RU, ADJS: ADJF_RU, COMP: COMP_RU, VERB: VERB_RU,
                                    INFN: INFN_RU, PRTF: PRTF_RU, PRTS: PRTS_RU, GRND: GRND_RU,
                                    NUMR: NUMR_RU, ADVB: ADVB_RU, NPRO: NPRO_RU, PRED: PRED_RU,
                                    PREP: PREP_RU, CONJ: CONJ_RU, PRCL: PRCL_RU, INTJ: INTJ_RU,
                                    X: X_RU, UNKN: UNKN_RU }
        
        self.features = {
            VERBAL_NOUN: 0,     # отглагольное существительное на -(е)ние
            VERBAL_NE_NOUN: 0,  # отглагольное существительное на не(до)-
            NMOD_GENT: 0,       # существительное в роли определения
            ABBR: 0,            # аббревиатуры
            COMPLEX_COMPARE: 0, # сложная сравнительная степень
            IMPR_PLUR: 0,       # глаголы в повелительном наклонении множественного числа
            I: 0,               # местоимение я
            WE: 0,              # местоимение мы
            PERSONAL: 0,        # личные местоимения
            FIXED: 0,           # производный предлог
        }

    def count_grammemes(self, my_sentence):
        self.number_of_sentences += 1
        id_token = 0
        for token in my_sentence.token_list:
            self.number_of_tokens += 1
            id_token += 1

            tag = token.pos
            pos = tag.POS
            parse = self.morph_tagger.parse(token.text)[0]

            # обрабатываем "UNKN" и "Х"
            if pos == None:
                if UNKN in tag:
                    self.parts_of_speech[UNKN].count += 1
                else:
                    self.parts_of_speech[X].count += 1
                    if PNCT not in tag:
                        self.number_of_words += 1
                    for label in self.parts_of_speech[X].labels:
                        if label in tag:
                            self.parts_of_speech[X].labels[label] += 1

            # обрабатываем части речи
            else:
                # прибавляем 1 к счетчику частей речи
                self.parts_of_speech[pos].count += 1
                self.number_of_words += 1
                # смотрим метки
                # уже на этом этапе отсеятся "PREP", "PRCL", "INTJ", "PRED"
                # "ADJS" и "PRTS" рассмотрим отдельно
                if pos != PREP and pos != PRCL and pos != INTJ and pos != PRED:
                    if pos != ADJS and pos != PRTS:
                        for label in self.parts_of_speech[pos].labels:
                            if label in tag:
                                self.parts_of_speech[pos].labels[label] += 1
                    elif pos == ADJS:
                        for label in self.parts_of_speech[ADJF].labels:
                            if label in tag:
                                self.parts_of_speech[pos].labels[label] += 1
                    elif pos == PRTS:
                        for label in self.parts_of_speech[PRTF].labels:
                            if label in tag:
                                self.parts_of_speech[pos].labels[label] += 1

                # обрабатываем признаки именных и глагольных частей речи
                if tag.case != None:
                    self.parts_of_speech[pos].case[tag.case] += 1
                if tag.gender != None:
                    self.parts_of_speech[pos].gender[tag.gender] += 1
                if tag.number != None:
                    self.parts_of_speech[pos].number[tag.number] += 1
                if tag.animacy != None:
                    self.parts_of_speech[pos].animacy[tag.animacy] += 1
                if tag.person != None:
                    self.parts_of_speech[pos].person[tag.person] += 1
                if tag.aspect != None:
                    self.parts_of_speech[pos].aspect[tag.aspect] += 1
                if tag.transitivity != None:
                    self.parts_of_speech[pos].transitivity[tag.transitivity] += 1
                if tag.tense != None:
                    self.parts_of_speech[pos].tense[tag.tense] += 1
                if tag.involvement != None:
                    self.parts_of_speech[pos].involvement[tag.involvement] += 1
                if tag.mood != None:
                    self.parts_of_speech[pos].mood[tag.mood] += 1
                if tag.voice != None:
                    self.parts_of_speech[pos].voice[tag.voice] += 1

                # ищем аббревиатуры
                if ABBR in tag:
                    self.features[ABBR] += 1
                # ищем производные предлоги
                if token.rel == FIXED:
                    self.features[FIXED] += 1
                if pos == NOUN:
                    # ловим существительные-определения
                    if tag.case != None:
                        if tag.case == GENT and token.rel == NMOD:
                            self.features[NMOD_GENT] += 1
                    # ловим отглагольные существительные на -(е)ние
                    if re.search(r'(\w*)((ение)|(ние))$', parse.normal_form) != None:
                        self.features[VERBAL_NOUN] += 1
                    # ловим отглагольные существительные на не(до)-
                    if re.search(r'^((не)|(недо))(\w*)((ение)|(ние))$', parse.normal_form) != None:
                        self.features[VERBAL_NE_NOUN] += 1
                # ищем глаголы повелительного наклонения множественного числа
                if pos == VERB:
                    if tag.mood != None and tag.number != None:
                        if tag.mood == IMPR and tag.number == PLUR:
                            self.features[IMPR_PLUR] += 1
                if pos == ADVB:
                    # проверяем, есть ли сложная сравнительная или превосходная степень
                    if token.text == "наиболее" or token.text == "более" or token.text == "наименее" or token.text == "менее":
                        token_head = my_sentence.get_parent(token.id)
                        if token_head.pos.POS != None:
                            if token_head.pos.POS == ADJF:
                                # более лучший?
                                if SUPR in token_head.pos:
                                    self.errors.add((my_sentence.text, token.text + " " + token_head.text), STYLE_SET, 
                                                    BUTTER_BUTTER, "")
                                else:
                                    self.features[COMPLEX_COMPARE] += 1
                            # более лучше?
                            if token_head.pos.POS == COMP:
                                self.errors.add((my_sentence.text, token.text + " " + token_head.text), STYLE_SET, 
                                               BUTTER_BUTTER, "")
                # ищем местоимения я, мы
                if pos == NPRO:
                    if tag.person != None and tag.number != None:
                        self.features[PERSONAL] += 1
                        if tag.person == PER1:
                            if tag.number == SING:
                                self.features[I] += 1
                                self.errors.add((my_sentence.text, token.text),
                                             {SCIENTIFIC, SCIENCE_OFF}, I, "замените на 'мы'")
                            else:
                                self.features[WE] += 1

    def compare(self, pos):
        return pos.count
    def sort_pos(self):
        self.parts_of_speech = dict(sorted(self.parts_of_speech.items(), key=lambda x: self.compare(x[1]))[::-1])

    def analyze(self):
        conversational = 0
        official = 0
        scientific = 0
        publicistic = 0

        noun = self.parts_of_speech[NOUN]
        npro = self.parts_of_speech[NPRO]
        adjf = self.parts_of_speech[ADJF]
        adjs = self.parts_of_speech[ADJS]
        
        verb = self.parts_of_speech[VERB]
        infn = self.parts_of_speech[INFN]
        prtf = self.parts_of_speech[PRTF]
        prts = self.parts_of_speech[PRTS]
        grnd = self.parts_of_speech[GRND]
        
        conj = self.parts_of_speech[CONJ]
        prcl = self.parts_of_speech[PRCL]
        intj = self.parts_of_speech[INTJ]

        if noun.count > 0:
            # именительный падеж
            if max_value(noun.case)[0] == NOMN:
                conversational += 1

            # родительный падеж
            elif max_value(noun.case)[0] == GENT:
                if ge_critical(self.features[NMOD_GENT], noun.case[GENT], 50):
                    scientific += 1

                else:
                    publicistic += 1


            # отглагольные существительные
            if ge_critical(self.features[VERBAL_NOUN], noun.count, 33):
                scientific += 1
                official += 1
            if ge_critical(self.features[VERBAL_NE_NOUN], noun.count, 33):
                official += 1

            # глаголы против существительных
            # глаголы побеждают
            if verb.count + infn.count > noun.count:
                conversational += 1
            elif ge_critical(verb.count + infn.count, self.number_of_words, 50):
                publicistic += 1
            # имена побеждают
            elif not ge_critical(verb.count + infn.count, noun.count, 10):
                official += 1
            elif not ge_critical(verb.count + infn.count, noun.count, 25):
                scientific += 1

            # местоимений много
            if ge_critical(npro.count, noun.count, 50):
                if ge_critical(self.features[PERSONAL], noun.count, 50) or \
                    max_value(npro.labels)[0] == DMNS:
                    conversational += 1
            else:
                # местоимений мало
                if not ge_critical(self.features[PERSONAL], noun.count, 5):
                    official += 1
                # "мы"
                elif self.features[I] == 0 and self.features[WE] > 0:
                    scientific += 1

        if verb.count > 0:
            # наст. и прош. время
            if ge_critical(verb.tense[PRES] + verb.tense[PAST], verb.count, 77):
                publicistic += 1

            # повелительное наклонение
            if self.features[IMPR_PLUR] > 0:
                publicistic += 1
                official += 1

        # нет причастий/деепричастий, кратких прилагательных/причастий
        if not ge_critical(adjs.count + prtf.count + prts.count + grnd.count, self.number_of_words, 1):
            conversational += 1

        # производные предлоги
        if ge_critical(self.features[FIXED], self.number_of_words, 20):
            scientific += 1
            official += 1

        # аббревиатуры
        if self.features[ABBR] > 0:
            official += 1
            publicistic += 1

        # многократные глаголы
        if verb.labels[MULT] > 0 or infn.labels[MULT] > 0:
            conversational += 1
        # междометия
        if intj.count > 0:
            conversational += 1
        # частицы
        if ge_critical(prcl.count, self.number_of_words, 20):
            conversational += 1
        # притяжательные прилагательные
        if adjf.labels[POSS] > 0:
            conversational += 1
        
        # вовлеченность
        if verb.involvement[INCL] > 0:
            publicistic += 1

        # прилагательные сложной сравнительной степени
        if self.features[COMPLEX_COMPARE] > 0:
            scientific += 1
        # вводные слова
        if ge_critical(conj.labels[PRNT], self.number_of_words, 20):
            scientific += 1

        # глаголы в неопределённой форме в значении повелительного наклонения
        if infn.aspect[PERF] > 0 and infn.aspect[IMPF] == 0:
            official += 1
        # субстантивации
        if noun.labels[SUBX] > 0 or adjf.labels[SUBX] > 0:
            official += 1

        self.style = get_style(conversational, scientific, official, publicistic)

    def __str__(self):
        self.sort_pos()
        string = ""
        string += "КОЛИЧЕСТВО ТОКЕНОВ = " + str(self.number_of_tokens) + "\n\n"
        for key, value in self.parts_of_speech.items():
            if value.count != 0:
                string += self.parts_of_speech_ru[key] + ":\n" + str(value) + "\n"
        return string
