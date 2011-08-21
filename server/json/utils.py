from collections import Iterable

def process_item_or_list(fun, input, **args):
    if isinstance(input, Iterable):
        return [fun(item, **args) for item in input]
    else:
        return fun(input, **args)