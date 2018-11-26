import glob
# import importlib
import os


currfile = os.path.abspath(__file__)
currdir = os.path.dirname(currfile)


def get_urls_modules():
    file_tpl = 'urls'
    res = []
    for file in glob.iglob('{}/**/{}.py'.format(currdir, file_tpl), recursive=True):
        begin = len(currdir)+1
        end = len('/{}.py'.format(file_tpl))
        component_name = file[begin:-end]
        module_name = 'components.{}.{}'.format(component_name, file_tpl)
        res.append((component_name, module_name))
    return res

# if file != currfile: #     begin = len(currdir)+1 #     end = len('/models.py')
#     model_name = 'components.{}'.format(file[begin:-end].replace('/', '.'))
#     spec = importlib.util.spec_from_file_location(model_name, file)
#     model = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(model)


def get_apps():
    # for d in os.walk(currdir):
    for d in glob.iglob('{}/*/'.format(currdir)):
        begin = len(currdir)+1
        app = d[begin:-1]
        if app == '__pycache__':
            continue
        print(app)
    # file_tpl = 'urls'
    # res = []
    # for file in glob.iglob('{}/**/{}.py'.format(currdir, file_tpl), recursive=True):
    #     begin = len(currdir)+1
    #     end = len('/{}.py'.format(file_tpl))
    #     component_name = file[begin:-end]
    #     module_name = 'components.{}.{}'.format(component_name, file_tpl)
    #     res.append((component_name, module_name))
    # return res
