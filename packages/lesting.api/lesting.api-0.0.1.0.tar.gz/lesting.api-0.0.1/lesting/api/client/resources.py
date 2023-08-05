from typing import Dict, Any, List, Union
from ..resources import Service, Resource, Method
from ..schemas import Schema
from httplib2 import Http
from itertools import zip_longest
import json
import re

REGEX = re.compile(r"({[a-zA-Z0-9.]+})")

class Client:

    service: Service
    schemas: Dict[str, Schema]
    http: Http
    headers: Dict[str, str]

    def __init__(self, service: Service, http: Http) -> None:
        self.service = service
        self.http = http
        self.headers = {
            "Content-Type": "application/json"
        }

    @property
    def schemas(self):
        return self.service.schemas

    def request(self, method: str, path: str, parameters: Dict[str, Schema]):
        headers, response = self.http.request(self.service.base + path, method, json.dumps(parameters), self.headers)
        assert headers["status"] == "200"
        return json.loads(response)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.service, name)

def null() -> None: ...

def create(document: Dict[str, Any], base: Union[Client, Http] = None):

    if document["type"] == "service":
        service = Service(document["name"], document["version"], document["base"])
        client = Client(service, base)
        for name, value in document["schemas"].items():
            service.schemas[name] = Schema.Meta.make(value, service.schemas)
        for name, value in document["resources"].items():
            service.resources[name] = create(value, client)
        return client

    elif document["type"] == "resource":
        resource = Resource(base, document["name"])
        for name, value in document["resources"].items():
            resource.resources[name] = create(value, base)
        return resource

    elif document["type"] == "method":
        parameters = {name: Schema.Meta.make(parameter, base.schemas) for name, parameter in document["parameters"].items()}
        response = Schema.Meta.make(document["response"], base.schemas)
        method = Method(base, null, document["method"])
        groups = [match.group()[1:-1] for match in REGEX.finditer(document["path"])]
        def func(*args: Any, **kwargs: Any) -> Any:
            for parameter, value in zip_longest(parameters.items(), args):
                if value is not None:
                    kwargs[parameter[0]] = value
                if getattr(parameter[1], "required", True) and parameter[0] not in kwargs:
                    raise TypeError("`%s` required" % (parameter[0]))
            path = document["path"].format_map({name: kwargs[name] for name in groups})
            return response.new(base.request(document["method"], path, {name: parameters[name].dump(value) for name, value in kwargs.items()}))
        method.func = func
        method.path = document["path"].split("/")
        method.parameters = parameters
        method.response = response
        return method