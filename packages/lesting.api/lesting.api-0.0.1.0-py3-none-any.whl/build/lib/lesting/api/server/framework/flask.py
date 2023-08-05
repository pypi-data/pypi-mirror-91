from typing import Union
from ...resources import Method
from ..base import Discovery as T
from flask import Flask, Blueprint, jsonify, request
from itertools import zip_longest
import re

def format_type(type_string: str) -> str:
    if type_string == "str":
        return "string"
    return type_string

REGEX = re.compile(r"({[a-zA-Z0-9.]+})")

def handler(method: Method):
    def wrapper(*args, **kwargs):
        if request.json:
            for name, value in request.json.items():
                kwargs[name] = method.parameters[name].new(value)
        return jsonify(method.response.dump(method.func(*args, **kwargs)))
    return wrapper

class Discovery(T):

    app: Union[Flask, Blueprint]

    def __init__(self, app: Union[Flask, Blueprint]) -> None:
        self.app = app
        super().__init__()
    
    def make(self, method):
        path = "/".join(method.path)
        groups = [match.group()[1:-1] for match in REGEX.finditer(path)]
        path = path.format_map({name: "<%s:%s>" % (format_type(method.parameters[name]._type.__name__), name) for name in groups})
        self.app.add_url_rule(path, path, handler(method), methods=[method.method])