__author__ = 'Andrey Komissarov'
__email__ = 'a.komisssarov@gmail.com'
__date__ = '12.2020'

# deprecated
# time_limit
# count_call
# timestamp
# timer
# makebold
# makeitalic

import datetime
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
            def wrapper(*args_, **kwargs_):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(fmt.format(name=args[0].__name__, reason=self.function),
                              category=DeprecationWarning,
                              stacklevel=2)
                warnings.simplefilter('default', DeprecationWarning)

                return args[0](*args_, **kwargs_)

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


class time_limit:
    """Set entity execution timeout. Works on Linux only!"""

    def __init__(self, seconds):
        self.seconds = seconds

    def __call__(self, func):
        import signal

        def signal_handler(signum, frame):
            raise Exception('Timed out!')

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(self.seconds)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
                print('Timed out!')

        return wrapper


def count_call(func):
    """Count the number of function calls. Use func.counter attr to get calls
    >>> @count_call
    >>> def some_func():
    ...     pass

    >>> some_func()
    >>> some_func()
    >>> some_func()
    >>> print(some_func.counter)
    3
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        return func(*args, **kwargs)

    wrapper.counter = 0
    return wrapper


def timestamp(func):
    """Capture the function call timestamp. Use func.created_at attr to get timestamp

    >>> @timestamp
    ... def test(x):
    ...     return x

    >>> print(test(5))
    >>> print(test.created_at)
    25
    2021-01-15 20:41:58.911966

    print(test1(25))
    print(test1.created_at)
    """

    func.created_at = str(datetime.datetime.now())
    return func


def timer(func):
    """Get a function execution time."""

    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        print('Start time:', start_time.strftime('%X'))
        func(*args, **kwargs)
        print('Finish time:', datetime.datetime.now().strftime('%X'))
        print("--- Time elapsed: %s ---" % (datetime.datetime.now() - start_time))

    return wrapper


def makebold(func):
    def wrapped(*args, **kwargs):
        return "<b>" + str(func(*args, **kwargs)) + "</b>"

    return wrapped


def makeitalic(func):
    def wrapped(*args, **kwargs):
        return "<i>" + str(func(*args, **kwargs)) + "</i>"

    return wrapped
