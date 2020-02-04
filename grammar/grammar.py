import json

import tracery
from tracery.modifiers import base_english


class Grammar(object):
    def __init__(self, grammar, source):
        self.grammar = grammar
        self.source = source

    def get(self):
        return self.grammar.flatten("#origin#")

    @staticmethod
    def from_file_path(file: str) -> 'Grammar':
        with open(file) as f:
            source = json.load(f)
        grammar = tracery.Grammar(source)
        grammar.add_modifiers(base_english)

        return Grammar(grammar, source)
