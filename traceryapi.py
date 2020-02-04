
from flask import Flask, request
from flask_json import FlaskJSON, as_json, JsonError

from grammar.grammar_inventory import GrammarInventory
from settings import GRAMMAR_DIR, BASE_URL, SOURCE_ENABLED, MAX_RESULTS

grammar_inventory = GrammarInventory.from_dir_path(GRAMMAR_DIR)

app = Flask(__name__)
FlaskJSON(app)


def _get_route(local_route):
    return BASE_URL + local_route


def _clamp(minimum, value, maximum):
    return max(minimum, min(value, maximum))


@app.route('/grammars/<title>')
@as_json
def get_result(title):
    if 'n' in request.args:
        requested_amount = int(request.args.get('n'))
        n = _clamp(0, requested_amount, MAX_RESULTS)
    else:
        n = 1

    results = {
        'result': [
            grammar_inventory.get_grammar(title).get()
            for _ in range(n)
        ],
        'list': _get_route('/grammars'),
    }

    if SOURCE_ENABLED and 'debug' in request.args:
        results['source'] = _get_route(f'/grammars/{title}/source')

    return results


if SOURCE_ENABLED:
    @app.route('/grammars/<title>/source')
    @as_json
    def get_source(title):
        results = {
            'result': [
                grammar_inventory.get_grammar(title).source
            ],
            'eval': _get_route(f'/grammars/{title}'),
            'list': _get_route('/grammars'),
        }
        return results


@app.route('/grammars')
@as_json
def get_grammar_list():
    return {
        'result': [
            {
                'title': title,
                'href': _get_route(f'/grammars/{title}')
            }
            for title in grammar_inventory.titles
        ]
    }



