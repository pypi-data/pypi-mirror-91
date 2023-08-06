"""
The argsCaller class wraps a function so that it can be invoked with dynamic
arguments while performing validations. When a validation fails an exception
is raised allowed for more sensible handling fromt the caller code.
"""
from inspect import signature, Parameter
from .exceptions import MissingArgument, TooManyArgument, UnsupportedKeyArgument


class argsCaller:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.new_args = []
        self.new_kwargs = {}
        self.provided_args = list(args[::-1])  # Reverse to use pop
        self._param_list = []  # Keep the list of arguments to build the arg str

        PARAM_MAP = {
            Parameter.POSITIONAL_OR_KEYWORD: self.handle_positional_or_keyword,
            Parameter.VAR_POSITIONAL: self.handle_var_positional,
            Parameter.VAR_KEYWORD: self.handle_var_keyword,
        }

        sig = signature(func)
        for i, param in enumerate(sig.parameters.values()):
            self._param_list.append(param)
            try:
                param_func = PARAM_MAP[param.kind]
            except KeyError:
                raise NotImplementedError(param.kind)
            param_func(param)

        for key in kwargs.keys():
            if key not in self.new_kwargs:
                raise UnsupportedKeyArgument(key)

        if self.provided_args:
            raise TooManyArgument(self.provided_args[0])

    def handle_positional_or_keyword(self, param):
        # if it was provived as a kwarg
        if param.name in self.kwargs.keys():
            # pass it as kwarg
            self.new_kwargs[param.name] = self.kwargs[param.name]
        else:
            # must be fetched from positional arguments
            try:
                arg = self.provided_args.pop()
            except IndexError:
                if param.default == Parameter.empty:
                    raise MissingArgument(param.name) from None
                arg = param.default
            self.new_args.append(arg)

    def handle_var_positional(self, param):
        self.provided_args.reverse()
        self.new_args.extend(self.provided_args)
        self.provided_args = []

    def handle_var_keyword(self, param):
        self.new_kwargs.update(self.kwargs)

    def call(self):
        return self.func(*self.new_args, **self.new_kwargs)

    def args_str(self):
        """ return the list of expected arguments represented as a string"""
        arg_list = []
        for param in self._param_list:
            value = f"<{param.name}>"
            if param.default is not Parameter.empty:
                value = f"[<{param.name}> = {param.default}]"
            arg_list.append(value)
        return ' '.join(arg_list)
