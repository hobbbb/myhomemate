from collections import defaultdict
from functools import wraps

from core import const


class EventBus:
    # __slots__ = '_events'

    def __init__(self):
        self._events = defaultdict(set)

    def listen(self, busevent):
        def outer(func):
            self._events[busevent].add(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return outer

    def throw(self, busevent, *args, **kwargs):
        for func in self._event_funcs(busevent):
            func(*args, **kwargs)

        if busevent != const.EVENT_ALL:
            for func in self._event_funcs(const.EVENT_ALL):
                func(*args, **kwargs)

    def _event_funcs(self, busevent):
        for func in self._events[busevent]:
            yield func


class ServiceRegistry:
    def __init__(self):
        self._services = defaultdict(set)

    def register(self, component, service):
        print('component', component)
        for k, v in service.items():
            print(k, v)
