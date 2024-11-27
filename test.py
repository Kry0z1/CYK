from .grammar import Grammar
from .cyk import CYK
from itertools import product
from collections import deque

def construct_grammar(not_terminals, terminals, rules, start):
    return Grammar(not_terminals, terminals, list(map(tuple, [rule.split("->") for rule in rules])), start)

def in_grammar(grammar, word):
    e = CYK()
    e.fit(grammar)
    return e.predict(word)

def is_RBS(word, brackets=None):
    if brackets == None:
        brackets = ["()"]
    table = {br[0]: br[1] for br in brackets}
    table_rv = {br[1]: br[0] for br in brackets}
    stack = deque()
    for c in word:
        if c in table.keys():
            stack.append(c)
            continue
        if c not in table_rv.keys() or len(stack) == 0:
            return False
        if stack.pop() != table_rv[c]:
            return False
    return len(stack) == 0

## Тест ПСП
def test_RBS():
    rules = [
        "A->",
        "A->BB",
        "A->CD",
        "B->BB",
        "B->CD",
        "C->(",
        "D->BE",
        "D->)",
        "E->)"
    ]
    g = construct_grammar("ABCDE", "()", rules, "A")
   
    for rep in range(11):
        for seq in product("()", repeat=rep):
            result_gr = in_grammar(g, "".join(seq))
            result = is_RBS("".join(seq))
            assert (result_gr and result) or (not result_gr and not result)
    assert in_grammar(g, "")

