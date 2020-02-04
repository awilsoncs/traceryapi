import os
from typing import List, Dict

from grammar.grammar import Grammar


class GrammarInventory(object):
    def __init__(self, title_grammar_map: Dict[str, Grammar]):
        self.title_grammar_map = title_grammar_map if title_grammar_map else {}

    @property
    def titles(self) -> List[str]:
        return list(self.title_grammar_map.keys())

    def get_grammar(self, title: str) -> Grammar:
        return self.title_grammar_map[title]

    @staticmethod
    def from_dir_path(inventory_path: str) -> 'GrammarInventory':
        return GrammarInventory(
            {
                f.replace('.json', ''): Grammar.from_file_path(inventory_path + '/' + f)
                for f in os.listdir(inventory_path)
            }
        )

