# argscall


argscall is python library that can be used to call functions while mapping and validating dynamic input arguments «*args or **kwargs» using the function arguments signature.

# Usage
```python
from argscall import argsCaller

# A simple function that requires one argument
def do_something(name):
    print(name.upper())

# Call the function passing a list with arguments
argscall(do_something, "a").call()
```

It becomes more usefull when used with dynamic input arguments, e.g command line arguments:
```python
# test.py
import sys
from argscall import argsCaller


# A sample function that requires an argument
def do_something(name):
    print(name.upper())


# Call the function passing the command line arguments
argsCaller(do_something, *sys.argv[1:]).call()
```

Testing different use cases
```
$ python test.py Joe
JOE

$ python test.py
Traceback (most recent call last)
...
argscall.exceptions.MissingArgument: Missing required argument: name


$ python test.py Joe Black
Traceback (most recent call last)
...
argscall.exceptions.TooManyArgument: Got more arguments than expected (value: 'Black')
```
