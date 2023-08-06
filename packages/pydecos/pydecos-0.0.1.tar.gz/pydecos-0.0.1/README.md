# pydecos - is a set of useful decorators.

## deprecate

to deprecate class/method/function. Deprecation reason can be specified.

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

# Usage

### function

```python
from pydecos import deprecated


@deprecated
def some_func(t):
    print('weeeee' * t)


some_func(3)
# <input>:1: DeprecationWarning: Call to deprecated function some_func.
# weeeeeweeeeeweeeee
```

### class

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

### method

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

### deprecation with reason specified

```python
from pydecos import deprecated


@deprecated('Use the new function "awesome_func()" instead')
def some_func(t):
    return t


some_func(3)
# DeprecationWarning: Deprecated function/method "some_func" has been invoked: Use the new function "awesome_func()" instead.
#  some_func(3)
```

# Changelog

##### 1.0.0 (14.01.2021)

- initial commit
