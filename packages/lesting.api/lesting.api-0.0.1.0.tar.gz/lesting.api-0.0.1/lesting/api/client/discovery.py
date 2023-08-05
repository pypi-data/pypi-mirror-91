from .resources import create
from httplib2 import Http
import json

def build(service: str, version: int, discovery: str = "http://127.0.0.1:80/discovery/v1/services/{service}/{version}/rest"):
    http = Http()
    headers, response = http.request(discovery.format_map({
        "service": service,
        "version": version
    }))
    assert headers["status"] == "200"
    return create(json.loads(response), http)