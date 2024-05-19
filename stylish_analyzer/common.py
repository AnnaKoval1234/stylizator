import pymorphy2
from natasha import Segmenter, Doc, NewsEmbedding, NewsSyntaxParser
from .lexic import LexicalAnalyzer
from .morphology import MorphologicalAnalyzer
from .syntax import SyntaxAnalyzer
from .for_analyzers.sentence import Token as MyToken, Sentence as MySentence
from .for_analyzers.functional import *
from .for_analyzers.constant import STYLE_SET

class Analyzer():
    def __init__(self, text):
        self.text = text
        self.doc = Doc(text)
        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.morph_tagger = pymorphy2.MorphAnalyzer()
        self.syntax_parser = NewsSyntaxParser(self.emb)

        self.lexical = LexicalAnalyzer()
        self.morphology = MorphologicalAnalyzer()
        self.syntax = SyntaxAnalyzer()
        self.final_style_set = {}

    def parse(self):
        
        self.doc.segment(self.segmenter)
        self.doc.parse_syntax(self.syntax_parser)

        my_sentence = MySentence()
        for sent in self.doc.sents:
            my_sentence.set_text(sent.text)
            self.lexical.count_lexemes(sent)

            for token in sent.tokens:
                my_token = MyToken(int(token.id.split('_')[1]), 
                                    int(token.head_id.split('_')[1]),
                                    token.text,
                                    self.morph_tagger.tag(token.text)[0],
                                    token.rel)
                my_sentence.add(my_token)
                #del my_token

            self.morphology.count_grammemes(my_sentence)
            self.syntax.count_sent(my_sentence)

            my_sentence.clear()
        #del my_sentence

    def analyze(self):
        self.lexical.analyze()
        self.morphology.analyze()
        self.syntax.analyze()

        string = ""
        string += f'Лексика: {self.lexical.style} стиль\n\n'
        string += f'Морфология: {self.morphology.style} стиль\n\n'
        string += f'Синтаксис: {self.syntax.style} стиль\n\n'
        return string
    
    def find_errors(self):
        self.final_style_set = get_final_style(self.lexical.style, self.morphology.style, self.syntax.style)
        self.morphology.errors.remove(STYLE_SET - self.final_style_set)
        self.syntax.errors.remove(STYLE_SET - self.final_style_set)
        return self.morphology.errors + self.syntax.errors