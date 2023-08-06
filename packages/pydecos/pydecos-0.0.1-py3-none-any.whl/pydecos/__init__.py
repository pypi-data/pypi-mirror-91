__author__ = 'Andrey Komissarov'
__email__ = 'a.komisssarov@gmail.com'
__date__ = '12.2020'

import functools
import inspect
import warnings


class deprecated:
    """
    Class-decorated to deprecate functions, classes and methods.
    Can be used with reason specifying.
    """

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.function = func

    def __call__(self, *args, **kwargs):

        # If you specify deprecation reason
        if isinstance(self.function, str):

            fmt = 'Deprecated function/method "{name}" has been invoked: {reason}.'
            if inspect.isclass(args[0]):
                fmt = 'Deprecated class has been invoked "{name}": {reason}.'

            @functools.wraps(args[0])
            def wrapper(*args_, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(fmt.format(name=args[0].__name__, reason=self.function),
                              category=DeprecationWarning,
                              stacklevel=2)
                warnings.simplefilter('default', DeprecationWarning)

                return args[0](*args_, **kwargs)

            return wrapper

        # Used is no 'reason' specified
        elif inspect.isclass(self.function) or inspect.isfunction(self.function):

            fmt = 'Deprecated function/method "{name}" has been invoked.'
            if inspect.isclass(self.function):
                fmt = 'Deprecated class has been invoked "{name}".'

            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(fmt.format(name=self.function.__name__), category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)

            return self.function(*args, **kwargs)
        else:
            raise TypeError(repr(type(self.function)))
