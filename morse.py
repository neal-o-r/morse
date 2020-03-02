import re
from collections import Counter
from functools import lru_cache
from typing import Generator


MORSE = {'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..', 'e':'.',
         'f':'..-.', 'g':'--.', 'h':'....', 'i':'..',
         'j':'.---', 'k':'-.-', 'l':'.-..', 'm':'--', 'n':'-.',
         'o':'---', 'p':'.--.', 'q':'--.-', 'r':'.-.',
         's':'...', 't':'-', 'u':'..-', 'v':'...-', 'w':'.--',
         'x':'-..-', 'y':'-.--', 'z':'--..'}

# a map of letters to next letters given the addition of a . or a -
MORSE_PREFIXES = {
    '^': 'et',
    'e': 'ia', 't': 'nm',
    'i': 'su', 'a': 'rw', 'n': 'dk', 'm': 'go',
    's': 'hv', 'u': 'f$', 'r': 'l$', 'w': 'pj', 'd': 'bx', 'k': 'cy', 'g': 'zq'
}


def words(text: str) -> list: return re.findall('\w+', text.lower())

WORDS = Counter(words(open("big.txt").read()))


def encode(word: str) -> str:
    return "".join(MORSE[l] for l in word)


def prob(word: str) -> float:
    return WORDS[word] / sum(WORDS.values())


def next_letter(letter: str, morse_char: str) -> str:
    i = 0 if morse_char is '.' else 1
    return MORSE_PREFIXES.get(letter, '$$')[i]

@lru_cache()
def parse(code: str, i: int =0, text: str = '', letter: str= '^') -> Generator:
    if i < len(code):
        letter = next_letter(letter, code[i])
        if letter != '$':
            yield from parse(code, i + 1, text, letter)
            yield from parse(code, i + 1, text + letter)
    elif letter == '^':
        yield text


def decode(morse: str) -> str:
    candidates = parse(m)
    return max(candidates, key=prob)


if __name__ == "__main__":

    m = encode("code")
    print(decode(m))
