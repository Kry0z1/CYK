from cyk import CYK
from grammar import Grammar


def main():
    n, sigma, p = map(int, input().split())

    not_terminals = list(input()) 
    terminals = list(input())
    rules = list()

    for _ in range(p):
        left, right = input().split("->")
        left = left.strip()
        right = right.strip()
        rules.append((left, right))

    start = input()

    cyk = CYK()
    cyk.fit(Grammar(not_terminals, terminals, rules, start))

    word_count = int(input())
    for _ in range(word_count):
        print("Yes" if cyk.predict(input()) else "No")

if __name__ == "__main__":
    main()
