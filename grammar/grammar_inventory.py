import os

from grammar.grammar_node import Grammar, GrammarLibrary


def read_grammar_inventory(base_url, file_path):
    output = {}
    for root, dirs, files in os.walk(file_path):
        for name in files:
            if name.endswith('.json'):
                output[root + '/' + name.replace('.json', '')] = Grammar.from_file_path(base_url, root, name)
        for name in dirs:
            output[root + '/' + name] = GrammarLibrary.from_file_path(base_url, root, name)
    output[file_path] = GrammarLibrary.from_file_path(base_url, '', file_path)
    return output
