from typing import Union, Iterator, Dict
from ..resources import Service, Resource, Method
from ..fields import Array
from ..schemas import Object

def iter(resource: Union[Service, Resource, Method]) -> Iterator[Method]:
    if isinstance(resource, Resource):
        for resource in resource.resources.values():
            yield from iter(resource)
    elif isinstance(resource, Method):
        yield resource

class Discovery:

    discovery: Service
    services: Dict[str, Dict[str, Service]]

    def __init__(self) -> None:
        self.discovery = Service("discovery", "v1")
        self.services = {}

        services = self.discovery.resource("services")

        @services.method("GET")
        def rest(service: str, version: str) -> None:
            return self.services[service][version]
        rest.path.insert(-1, "{service}/{version}")

        @services.method("GET")
        def list() -> Array(Object.quick("Service", {"name": str, "version": str})):
            return [{"name": service["name"], "version": service["version"]} for versions in self.services.values() for service in versions.values()]

        list.path.pop(-1)
        list.path.append("")

        self.register(self.discovery)

    def register(self, service: Service) -> None:
        self.services.setdefault(service.name, {})[service.version] = service.format()
        for method in iter(service):
            self.make(method)

    def make(self, method) -> None:
        raise NotImplementedError