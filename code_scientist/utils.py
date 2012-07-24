import re

def regex_filter(regex, iterable):
    compiled_re = re.compile(regex)
    return filter(compiled_re.search, iterable)

def compose(function_sequence, target):
    value = target
    for f in function_sequence:
        value = f(value)
    return value
