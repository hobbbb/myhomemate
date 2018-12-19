import inspect
import re


def component_name(module):
    path = module.__file__
    if path.find('lib/components/') >= 0:
        return re.sub(r'(.*?lib/components/)|((/__init__)?\.py$)', '', path).replace('/', '.')
