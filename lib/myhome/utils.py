import inspect
import re


def component_name():
    for s in inspect.stack():
        if s[1].find('lib/components/') >= 0:
            return re.sub(r'(^lib/components/)|(/[^/]+.py$)', '', s[1]).replace('/', '.')
