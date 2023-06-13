from typing import Any
import functools

""" Basic decorator function """


def deco1(func):
    def wrapper():
        print('Before')
        func()
        print('After')

    return wrapper


@deco1
def func1_simple():
    print('A simple function...')


""" Decorating a func with argeuments and return values
    and preserving the introspcation info of the decorated function """


def deco2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        rst = func(*args, **kwargs)
        return rst

    return wrapper


@deco2
def func2_arg(name):
    print(f'Hello {name}')

    if len(name) > 5:
        return 1
    else:
        return 0


""" The decorator itself may also have arguments """


def deco3(num_times=3):  # the decorated func is passed IMPLICITLY
    def deco3_deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return deco3_deco


# A better way: using decorator w/ or w/o arguments
# * syntax: all following arguments have to be kw ones
def deco3_both(_func=None, *, num_times=3):
    def deco3_deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper

    if _func is None:
        return deco3_deco
    else:
        return deco3_deco(_func)


# @deco3(5)
# @deco3_both(num_times=2)  # has to use kw arguments
@deco3_both
def func3_comp():
    print('Be decorated...')


""" The decorator also could be a class:
In this case, the way it decorates a function is to take that function as an
argument in its .__init__() method.
Furthermore, the class instance needs to be callable, that's by implementing a
.__call__() method.
"""


class Deco4:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    # executed when an instance is called
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.count += 1
        print(f'Call {self.count} of {self.func.__name__!r}')
        return self.func(*args, **kwds)


@Deco4
def func4():
    print(f'Calling {__name__}...')


if __name__ == '__main__':
    """ to demo the usage of decorators

    Firstly shows how to use the decorator in an old way (w/o the @ statement)
    Second one shows how to use the decorator in a normal way (the @ notation)
    """
    # func1_simple = deco1(func=func1_simple)
    # func1_simple()

    # func2_arg = deco2(func=func2_arg)
    func2_arg('Mei')  # w/o dealing w/ return value
    print(func2_arg('Mei'))  # print return value

    # func3_comp = deco3(func3_comp)  # This form WON'T work as func not passed
    # func3_comp = deco3_both(func3_comp)  # use the dft kwargs of deco3_both
    func3_comp()

    for i in range(3):
        func4()
