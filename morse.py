from typing import Dict, List, Generator, Set

def morse_dict(fname: str) -> Dict:
    with open(fname) as f:
        lines = f.read().split("\n")[:-1]

    split = lambda x: x.split(",")
    return {m : c for c, m in map(split, lines)}

def dictionary(fname: str) -> Set:
    with open(fname) as f:
        lines = f.read().split("\n")[:-1]

    return {w.upper() for w in lines}


class Tree:
    def __init__(self, code=None):
        self.code = code
        self.char = MORSE[code] if code is not "" else None
        self.left = None
        self.right = None

    def __repr__(self):
        return f"{self.char}"

    def __eq__(self, other):
        return self.code == other.code


def populate_tree(morse: Dict) -> Tree:

    tree = Tree("")

    frontier = [tree]
    while frontier:
        f = frontier.pop()
        if f.code + "-" in morse:
            node = Tree(f.code + "-")
            f.left = node
            frontier.append(node)
        if f.code + "." in morse:
            node = Tree(f.code + ".")
            f.right = node
            frontier.append(node)

    return tree


MORSE = morse_dict("morse.csv")
TREE = populate_tree(MORSE)
DICTIONARY = dictionary("/usr/share/dict/british-english")


def next_tree(tree: Tree, code: str) -> Tree:
    return tree.left if code is '-' else tree.right


def parse(code: str, state: Tree = TREE, tree: List = []) -> Generator:

    if code:
        head, tail = code[0], code[1:]

        state = next_tree(state, head)
        if state:
            yield from parse(tail, state, tree)
            yield from parse(tail, TREE, tree + [state])

    elif state == TREE:
        yield tree


def is_word(word: str) -> bool:
    return word in DICTIONARY


def show_parse(code: str, n: int = 100) -> List[str]:

    for _, trees in zip(range(n), parse(code)):
        word = "".join(t.char for t in trees)

        if is_word(word):
            print(word)


if __name__ == "__main__":
    show_parse("......-...-..---", n=1000)
