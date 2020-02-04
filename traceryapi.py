
from flask import Flask, request
from flask_json import FlaskJSON, as_json

from grammar.grammar_inventory import read_grammar_inventory
from settings import GRAMMAR_DIR, BASE_URL, MAX_RESULTS

grammar_inventory = read_grammar_inventory(BASE_URL, GRAMMAR_DIR)
app = Flask(__name__)
FlaskJSON(app)


def _get_route(local_route):
    return BASE_URL + local_route


def _clamp(minimum, value, maximum):
    return max(minimum, min(value, maximum))


@app.route('/content')
@as_json
def get_content_root():
    return grammar_inventory.get('./content').evaluate(0)


@app.route('/content/<path:title>')
@as_json
def get_result(title):
    try:
        if 'n' in request.args:
            n = _clamp(0, int(request.args.get('n')), MAX_RESULTS)
        else:
            n = 1
        return grammar_inventory.get(GRAMMAR_DIR + '/' + title).evaluate(n)
    except AttributeError:
        if title not in grammar_inventory:
            print(f'Searching for: {title}')
            print('Found:')
            for route in grammar_inventory.keys():
                print(f'\t{route}')
