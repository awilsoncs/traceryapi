import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import tracery
from tracery.modifiers import base_english


class AbstractGrammarNode(ABC):

    @abstractmethod
    def evaluate(self, n):
        pass


@dataclass
class Grammar(AbstractGrammarNode):
    grammar: tracery.Grammar
    parent_route: str
    route: str

    def evaluate(self, n):
        return {
            'href': self.route,
            'parent': self.parent_route,
            'results': [self.grammar.flatten('#origin#') for _ in range(n)]
        }

    @staticmethod
    def from_file_path(base_url, parent, file: str) -> 'Grammar':
        file = os.path.join(parent, file)
        with open(file) as f:
            print(f'loading grammar: {file}')
            source = json.load(f)
        grammar = tracery.Grammar(source)
        grammar.add_modifiers(base_english)

        return Grammar(
            grammar,
            base_url + parent[1:],
            base_url + file.replace('.json', '')[1:]
        )


@dataclass
class GrammarLibrary(AbstractGrammarNode):
    route: str
    parent: str
    children: field(default_factory=dict)

    def evaluate(self, n):
        return {
            'route': self.route,
            'parent': self.parent,
            'children': self.children
        }

    @staticmethod
    def from_file_path(base_url, parent: str, file: str) -> 'GrammarLibrary':
        file = os.path.join(parent, file)
        print(f'loading grammar index: {file}')
        return GrammarLibrary(
            base_url + file[1:],
            base_url + parent[1:],
            [
                {
                    'title': child.replace('.json', ''),
                    'href': base_url + file[1:] + '/' + child.replace('.json', '')
                }
                for child in os.listdir(file)
            ]
        )
