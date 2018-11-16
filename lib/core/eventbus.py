from collections import defaultdict
from functools import wraps


class EventBus:
    # __slots__ = '_events'

    def __init__(self):
        self._events = defaultdict(set)

    def listen(self, event, once=0):
        def outer(func):
            self._add_event(event, func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return outer

    def throw(self, event):
        for func in self._event_funcs(event):
            # func(*args, **kwargs)
            func()

    def _event_funcs(self, event):
        for func in self._events[event]:
            yield func

    def _add_event(self, event, func):
        self._events[event].add(func)
