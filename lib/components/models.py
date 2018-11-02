""" Collect models from all components for django migrations """

# import glob
# import importlib
# import os

# currfile = os.path.abspath(__file__)
# currdir = os.path.dirname(currfile)

# for file in glob.iglob('{}/**/models.py'.format(currdir), recursive=True):
#     if file != currfile:
#         begin = len(currdir)+1
#         end = len('/models.py')
#         model_name = 'components.{}'.format(file[begin:-end].replace('/', '.'))
#         spec = importlib.util.spec_from_file_location(model_name, file)
#         model = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(model)
