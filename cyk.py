from grammar import Grammar

class CYK:
    _grammar: Grammar

    def __init__(self):
        pass

    def fit(self, grammar: Grammar):
        for left, right_set in grammar._rules.items():
            for right in right_set:
                if len(right) == 0:
                    if left != grammar._start:
                        raise ValueError(f"Grammar is not appropriate for CYK: rule {left}->eps is not allowed")
                    continue 
                if len(right) == 1:
                    if right[0] not in grammar._terminals:
                        raise ValueError(f"Grammar is not appropriate for CYK: not terminal in right side of rule {left}->{right}")
                    continue
                if len(right) == 2:
                    if right[0] == grammar._start or right[1] == grammar._start:
                        raise ValueError(f"Grammar is not appropriate for CYK: starting state in right side of rule {left}->{right}")
                    if right[0] not in grammar._not_terminals or right[1] not in grammar._not_terminals:
                        raise ValueError(f"Grammar is not appropriate for CYK: terminal char in right side of rule {left}->{right}")
                    continue
                raise ValueError(f"Grammar is not appropriate for CYK: right side of rule {left}->{right} is too long")
        self._grammar = grammar

    def predict(self, word: str):
        if len(word) == 0:
            return "" in self._grammar._rules[self._grammar._start]

        dp = {not_terminal: [[0 for _ in range(len(word))] for _ in range(len(word))] for not_terminal in self._grammar._not_terminals}
        
        for i in range(len(word)):
            for not_terminal, right_set in self._grammar._rules.items():
                if word[i] in right_set:
                    dp[not_terminal][i][i] += 1

        for m in range(1, len(word)):
            for not_terminal, right_set in self._grammar._rules.items():
                for right in right_set:
                    if len(right) != 2:
                        continue
                    for i in range(len(word) - m):
                        dp[not_terminal][i][i+m] += sum(dp[right[0]][i][j] * dp[right[1]][j+1][i+m] for j in range(i, i+m))
        
        return dp[self._grammar._start][0][len(word)-1] > 0
