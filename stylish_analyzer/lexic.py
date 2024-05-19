import time
import requests
import pymorphy2
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .for_analyzers.functional import *
from .for_analyzers.constant import *

class LexicalAnalyzer():
    def __init__(self) -> None:
        self.url = "https://livedict.syllabica.com/json"
        self.morph_tagger = pymorphy2.MorphAnalyzer()
        self.number_of_words = 0
        self.number_of_tokens = 0
        self.style = ""

        self.cache = {}
        self.lexic_styles = {
            SCIENTIFIC: 0,      # научный
            BELLES_LETTRES: 0,  # художественный
            OFFICIAL_RED: 0,    # офиц.-деловой
            IDEOLOGICAL: 0,     # идеологический
            RELIGIOUS: 0,       # религиозный
            CONVERSATIONAL: 0   # разговорный
        }

    def count_lexemes(self, sent):

        for token in sent.tokens:
            self.number_of_tokens += 1

            tag = self.morph_tagger.tag(token.text)[0]
            parse = self.morph_tagger.parse(token.text)[0]
            
            if PNCT not in tag:
                self.number_of_words += 1

            if tag.POS != None:
                if not self.morph_tagger.word_is_known(token.text):
                    self.lexic_styles[CONVERSATIONAL] += 1
                else:
                    normal_word = parse.normal_form
                    if normal_word not in self.cache.keys():
                        try:
                            lexem = Lexem.objects.get(word=normal_word)
                            self.lexic_styles[lexem.style] += 1
                            self.cache[normal_word] = lexem.style
                        except ObjectDoesNotExist:
                            data = {'word': normal_word}
                            res = requests.post(self.url, data=data)
                            i = 0
                            while res.status_code == 500:
                                waiting = i
                                i += 1
                                time.sleep(waiting)
                                res = requests.post(self.url, data=data)
                                if waiting == 100:
                                    break
                            try:
                                json = res.json()
                                style = json['results'][1]['value'][0]

                                Lexem.objects.create(word=normal_word, style=style)
                                self.lexic_styles[style] += 1
                                self.cache[normal_word] = style
                            except requests.JSONDecodeError:
                                self.lexic_styles[CONVERSATIONAL] += 1
                                self.cache[normal_word] = CONVERSATIONAL
                    else:
                        self.lexic_styles[self.cache[normal_word]] += 1

    def analyze(self):
        lexic_styles = reverse_sorted_list(self.lexic_styles)
        fst_style = lexic_styles[0]
        snd_style = lexic_styles[1]

        is_substyle = ge_critical(snd_style[1], fst_style[1], 66)

        if fst_style[0] == BELLES_LETTRES:
            self.style = fst_style[0]
        
        elif fst_style[0] == OFFICIAL_RED:
            self.style = OFFICIAL
        
        elif fst_style[0] == SCIENTIFIC:
            if is_substyle:
                if snd_style[0] == OFFICIAL_RED:
                    self.style = SCIENTIFIC_TECH
                elif snd_style[0] == CONVERSATIONAL:
                    self.style = SCIENTIFIC_PUB
                else:
                    self.style = SCIENTIFIC
            else:
                self.style = SCIENTIFIC
        
        elif fst_style[0] == IDEOLOGICAL:
            if is_substyle:
                if snd_style[0] == OFFICIAL_RED:
                    self.style = PUBLICISTIC_IDEA
                else:
                    self.style = PUBLICISTIC
            else:
                self.style = PUBLICISTIC

        elif fst_style[0] == RELIGIOUS:
            if is_substyle:
                if snd_style[0] == BELLES_LETTRES or snd_style[0] == SCIENTIFIC:
                    self.style = snd_style[0]
                elif snd_style[0] == IDEOLOGICAL or snd_style[0] == CONVERSATIONAL:
                    self.style = PUBLICISTIC
                elif snd_style[0] == OFFICIAL_RED:
                    self.style = PUBLICISTIC_IDEA
            else:
                self.style = PUBLICISTIC

        elif fst_style[0] == CONVERSATIONAL:
            if is_substyle:
                if snd_style[0] == BELLES_LETTRES:
                    self.style = snd_style[0]
                elif snd_style[0] == SCIENTIFIC:
                    self.style = SCIENTIFIC_PUB
                elif snd_style[0] == IDEOLOGICAL or snd_style[0] == RELIGIOUS:
                    self.style = PUBLICISTIC
                else:
                    self.style = CONVERSATIONAL
            else:
                self.style = CONVERSATIONAL
    
    def __str__(self):
        self.lexic_styles = reverse_sorted_dict(self.lexic_styles)
        string = ""
        string += "всего слов: " + str(self.number_of_words) + "\n\n"
        for key, value in self.lexic_styles.items():
            string += key + ": " + str(value) + '\n'
        return string
