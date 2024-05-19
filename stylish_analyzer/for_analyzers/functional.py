import pymorphy2
from .constant import *

def ge_critical(number: int, comparative_number: int, percent: int):
    div = round(number / comparative_number * 100)
    return div >= percent and div <= 100

def ge_critical_float(number: int, comparative_number: int, percent: float, ndigits: int):
    div = round(number / comparative_number * 100, ndigits)
    return div >= percent and div <= 100

def is_permissible_range(number: int, comparative_number: int, percent_begin: int, percent_end: int):
    div = round(number / comparative_number * 100)
    return div >= percent_begin and div <= percent_end

def is_permissible_range_float(number: int, comparative_number: int, percent_begin: float, percent_end: float, ndigits: int):
    div = round(number / comparative_number * 100, ndigits)
    return div >= percent_begin and div <= percent_end

def reverse_sorted_list(dictionary: dict):
    return sorted(dictionary.items(), key=lambda item: item[1])[::-1]

def reverse_sorted_dict(dictionary: dict):
    return dict(sorted(dictionary.items(), key=lambda item: item[1])[::-1])

def max_value(dictionary: dict):
    return reverse_sorted_list(dictionary)[0]

def get_style(conversational, scientific, official, publicistic):
    if conversational == scientific == official == publicistic:
        return BELLES_LETTRES
    else:
        result_dict = { CONVERSATIONAL: conversational,
                        SCIENTIFIC: scientific,
                        OFFICIAL: official,
                        PUBLICISTIC: publicistic, }
        result_list = reverse_sorted_list(result_dict)
        fst_style = result_list[0]
        snd_style = result_list[1]

        if fst_style[1] != snd_style[1]:
            return fst_style[0]
        else:
            if fst_style[0] == CONVERSATIONAL and snd_style[0] == PUBLICISTIC or \
                fst_style[0] == PUBLICISTIC and snd_style[0] == CONVERSATIONAL:
                return CONVERSE_PUB
            elif fst_style[0] == CONVERSATIONAL or snd_style[0] == CONVERSATIONAL:
                return CONVERSATIONAL
            elif fst_style[0] == PUBLICISTIC or snd_style[0] == PUBLICISTIC:
                return PUBLICISTIC
            elif fst_style[0] == OFFICIAL and snd_style[0] == SCIENTIFIC or \
                snd_style[0] == OFFICIAL and fst_style[0] == SCIENTIFIC:
                return SCIENCE_OFF

def get_final_style(lex_style, morph_style, synt_style) -> set:
    if lex_style == morph_style == synt_style:
        return {lex_style}
    else:
        if lex_style == SCIENTIFIC or lex_style == OFFICIAL or lex_style == SCIENTIFIC_TECH:
            return {SCIENTIFIC, OFFICIAL, SCIENCE_OFF}
        elif lex_style == SCIENTIFIC_PUB:
            return {SCIENTIFIC, PUBLICISTIC, CONVERSE_PUB}
        elif lex_style == PUBLICISTIC:
            return {PUBLICISTIC, CONVERSE_PUB, BELLES_LETTRES}
        elif lex_style == PUBLICISTIC_IDEA:
            return {OFFICIAL, SCIENCE_OFF}
        elif lex_style == CONVERSATIONAL or BELLES_LETTRES:
            return {CONVERSATIONAL, PUBLICISTIC, CONVERSE_PUB, BELLES_LETTRES}
