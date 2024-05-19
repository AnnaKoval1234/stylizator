from .constant import *
class Token():
    def __init__(self, id, head_id, text, pos, rel):
        self.id = id
        self.head_id = head_id
        self.text = text
        self.pos = pos
        self.rel = rel
    def __del__(self):
        return

class Sentence():
    def __init__(self):
        # количество токенов в предложении
        self.__count = 0
        # количество слов в предложении
        self.__length = 0
        # текст предложения
        self.__text = ""

        self.__token_list = []
        self.__id_list = []
        self.__head_id_list = []
        self.__text_list = []
        self.__pos_list = []
        self.__rel_list = []
    def __del__(self):
        return

    def __iter__(self):
        return self.__token_list.__iter__()
    def __getitem__(self, key):
        return self.__token_list[key]
    def __setitem__(self, key, value):
        self.__token_list[key] = value

    @property
    def count(self):
        return self.__count
    @property
    def length(self):
        return self.__length
    @property
    def text(self):
        return self.__text
    @property
    def token_list(self):
        return self.__token_list
    @property
    def id_list(self):
        return self.__id_list
    @property
    def head_list(self):
        return self.__head_list
    @property
    def text_list(self):
        return self.__text_list
    @property
    def pos_list(self):
        return self.__pos_list
    @property
    def rel_list(self):
        return self.__rel_list

    def add(self, token : Token):
        self.__count += 1
        if PNCT not in token.pos:
            self.__length += 1
        self.__token_list.append(token)
        self.__id_list.append(token.id)
        self.__head_id_list.append(token.head_id)
        self.__text_list.append(token.text)
        self.__pos_list.append(token.pos)
        self.__rel_list.append(token.rel)
    def set_text(self, text):
        self.__text = text
    def clear(self):
        self.__count = 0
        self.__length = 0
        self.__text = ""
        self.__token_list.clear()
        self.__id_list.clear()
        self.__head_id_list.clear()
        self.__text_list.clear()
        self.__pos_list.clear()
        self.__rel_list.clear()

    def get_token_rel(self, rel):
        i = self.__rel_list.index(rel)
        return self.__token_list[i]
    def get_token_pos(self, pos):
        i = self.__pos_list.index(pos)
        return self.__token_list[i]
    
    def get_parent(self, id):
        return self.__token_list[self.__token_list[id - 1].head_id - 1]
    def has_children(self, id):
        for i in range(0, self.__count):
            if id == self.__head_id_list[i]:
                if PNCT not in self.__pos_list[i]: 
                    return True
                elif self.__pos_list[i].POS != CONJ:
                    return True
                elif self.__pos_list[i].POS != PRCL:
                    return True
                elif self.__pos_list[i].POS != PREP:
                    return True
        return False
    
    def is_exists_morph_tag(self, morph_tag):
        for pos in self.__pos_list:
            if morph_tag in pos:
                return True
        return False
    
    def number_of_subjects(self):
        num_subj = 0
        for i in range(0, self.__count):
            if self.__rel_list[i] == NSUBJ:
                num_subj += 1
            elif self.__rel_list[i] == NSUBJ_PASS:
                num_subj += 1
            elif self.__rel_list[i] == CSUBJ:
                num_subj += 1
            elif self.__rel_list[i] == CSUBJ_PASS:
                num_subj += 1
            elif self.__rel_list[i] == APPOS:
                num_subj += 1
            elif self.__rel_list[i] == NUMMOD_GOV:
                if self.__pos_list[i].POS == NUMR and self.get_parent(i+1).rel != NSUBJ:
                    num_subj += 1

            elif self.__rel_list[i] == CONJ:
                parent = self.get_parent(i+1)
                if parent.rel == NSUBJ:
                    num_subj += 1
                elif parent.rel == NSUBJ_PASS:
                    num_subj += 1
                elif parent.rel == CSUBJ:
                    num_subj += 1
                elif parent.rel == CSUBJ_PASS:
                    num_subj += 1
                elif parent.rel == APPOS:
                    num_subj += 1
                elif parent.rel == NUMMOD_GOV:
                    if self.__pos_list[i].POS == NUMR and self.get_parent(parent.id).rel != NSUBJ:
                        num_subj += 1 
        return num_subj
    
    def number_of_predicates(self):
        num_pred = 0
        for i in range(0, self.__count):
            if self.__rel_list[i] == ROOT:
                num_pred += 1
            elif self.__rel_list[i] == CCOMP:
                num_pred += 1
            elif self.__rel_list[i] == ACL_RELCL:
                num_pred += 1
            elif self.__rel_list[i] == ACL:
                if self.__pos_list[i].POS == VERB:
                    num_pred += 1
            elif self.__rel_list[i] == PARATAXIS:
                if self.get_parent(i+1).rel == ROOT:
                    num_pred += 1

            elif self.__rel_list[i] == CONJ:
                parent = self.get_parent(i+1)
                if parent.rel == ROOT:
                    num_pred += 1
                elif parent.rel == CCOMP:
                    num_pred += 1
                elif parent.rel == ACL_RELCL:
                    num_pred += 1
                elif parent.rel == ACL:
                    if parent.pos.POS == VERB:
                        num_pred += 1
                elif parent.rel == PARATAXIS:
                    if self.get_parent(parent.id).rel == ROOT:
                        num_pred += 1
        return num_pred
    
    def is_exists_minor_members_of_sentence(self):
        minor_members = [NUMMOD, NUMMOD_ENTITY, 
                         OBJ, IOBJ, ADVCL, ADVMOD, OBL, 
                         OBL_AGENT, AMOD, DET, NMOD, 
                         COMPOUND]
        for minor in minor_members:
            if minor in self.__rel_list:
                return True
        for i in range(0, self.__count):
            if self.__rel_list[i] == ACL:
                if self.__pos_list[i].POS == PRTF:
                    return True
            if self.__rel_list[i] == NUMMOD_GOV:
                if self.__pos_list[i].POS != NUMR:
                    return True
            if self.__rel_list[i] == CONJ or self.__rel_list[i] == PARATAXIS:
                parent = self.get_parent(i+1)
                if parent.rel in minor_members:
                    return True
                if parent.rel == ACL:
                    if parent.pos.POS == PRTF:
                        return True
                if parent.rel == NUMMOD_GOV:
                    if self.__pos_list[i].POS != NUMR:
                        return True
        return False
