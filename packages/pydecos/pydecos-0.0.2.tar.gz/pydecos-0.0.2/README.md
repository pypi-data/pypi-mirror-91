# pydecos - is a set of useful decorators.

- deprecate:
  to deprecate class/method/function. Deprecation reason can be specified.
- ...

# Installation

For most users, the recommended method to install is via pip:

```cmd
pip install pydedecos
```

or from a source:

```cmd
python setup.py install
```

# Import

```python
from pydecos import deprecated
```

---

# Usage examples

## - @deprecated

- function

```python
from pydecos import deprecated


@deprecated
def some_func(t):
  print('weeeee' * t)


some_func(3)
# <input>:1: DeprecationWarning: Call to deprecated function some_func.
# weeeeeweeeeeweeeee
```

- class

```python
from pydecos import deprecated


@deprecated
class SomeClass:
    def some_method(self):
        ...


SomeClass()
# DeprecationWarning: Deprecated class has been invoked "SomeClass".
# SomeClass()
```

- method

```python
from pydecos import deprecated


class SomeClass:

    @deprecated
    def some_method(self):
        ...


SomeClass().some_method()
# DeprecationWarning: Deprecated function/method "some_method" has been invoked.
# SomeClass().some_method()
```

- deprecation with reason specified

```python
from pydecos import deprecated


@deprecated('Use the new function "awesome_func()" instead')
def some_func(t):
  return t


some_func(3)
# DeprecationWarning: Deprecated function/method "some_func" has been invoked: Use the new function "awesome_func()" instead.
#  some_func(3)
```

## - @timestamp

```python
from pydecos import timestamp


@timestamp
def some_func(t):
  return t


some_func(3)
print(some_func.created_at)

# 2021-01-15 20:58:45.071720
```

## - @count_call

```python
from pydecos import count_call


@count_call
def some_func():
  pass


some_func()
some_func()
some_func()
print(some_func.counter)
# 3
```

# Changelog

##### 0.0.2 (15.01.2021)

Added new decorators

- time_limit (linux only)
- count_call
- timestamp
- timer
- makebold
- makeitalic

##### 0.0.1 (14.01.2021)

- initial commit
