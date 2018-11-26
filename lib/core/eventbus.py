from collections import defaultdict
from functools import wraps

from core import const


class EventBus:
    # __slots__ = '_events'

    def __init__(self):
        self._events = defaultdict(set)

    def listen(self, event):
        def outer(func):
            self._events[event].add(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return outer

    def throw(self, event):
        for func in self._event_funcs(event):
            func()

        if event != const.EVENT_ALL:
            for func in self._event_funcs(const.EVENT_ALL):
                func()

    def _event_funcs(self, event):
        for func in self._events[event]:
            yield func
