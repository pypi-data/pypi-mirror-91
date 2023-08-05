import importlib


def model_str(instance, attr):
    return hasattr(instance, attr) and getattr(instance, attr) \
           or f'<{instance.__class__.__name__}: {instance.id}>'


def classgrabber(class_str: str):
    x = class_str.split('.')
    path = '.'.join(x[0:-1])
    models = importlib.import_module(path)
    return getattr(models, x[-1])