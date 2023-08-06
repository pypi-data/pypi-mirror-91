# pylint: disable = invalid-name
from typing import List
from injecta.service.class_.InspectedArgument import InspectedArgument
from databricksbundle.display import display
from databricksbundle.notebook.decorator.argsChecker import checkArgs
from databricksbundle.notebook.function.functionInspector import inspectFunction

def _resolveArguments(inspectedArguments: List[InspectedArgument], decoratorArgs: tuple):
    from databricksbundle.notebook.init import argumentsResolver  # pylint: disable = import-outside-toplevel
    return argumentsResolver.resolve(inspectedArguments, decoratorArgs)

def _callFunction(fun, decoratorArgs: tuple):
    arguments = _resolveArguments(inspectFunction(fun), decoratorArgs)
    return fun(*arguments)

def _notebookFunctionExecuted(fun):
    return fun.__module__ == '__main__'

class FunctionDecorator:

    _function = None

    @property
    def function(self):
        return self._function

class ResultDecorator(FunctionDecorator):

    _result = None

    @property
    def result(self):
        return self._result

class notebookFunction(ResultDecorator):

    def __init__(self, *args): # pylint: disable = unused-argument
        self._decoratorArgs: tuple = args
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        self._function = fun

        if _notebookFunctionExecuted(fun):
            self._result = _callFunction(fun, self._decoratorArgs)

        return self

class dataFrameLoader(ResultDecorator):

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        self._decoratorArgs: tuple = args
        self._displayEnabled = kwargs.get('display', False)
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        self._function = fun

        if _notebookFunctionExecuted(fun):
            self._result = _callFunction(fun, self._decoratorArgs)

            if self._displayEnabled:
                display(self._result)

        return self

class transformation(ResultDecorator):

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        self._decoratorArgs: tuple = args
        self._displayEnabled = kwargs.get('display', False)
        self._checkDuplicateColumns = kwargs.get('checkDuplicateColumns', True)

    def __call__(self, fun, *args, **kwargs):
        self._function = fun

        if _notebookFunctionExecuted(fun):
            self._result = _callFunction(fun, self._decoratorArgs)

            if self._checkDuplicateColumns:
                from databricksbundle.notebook.init import duplicateColumnsChecker  # pylint: disable = import-outside-toplevel
                resultDecorators = tuple(decoratorArg for decoratorArg in self._decoratorArgs if isinstance(decoratorArg, ResultDecorator))
                duplicateColumnsChecker.check(self._result, resultDecorators)

            if self._displayEnabled:
                display(self._result)

        return self

class dataFrameSaver(FunctionDecorator):

    def __init__(self, *args):
        self._decoratorArgs: tuple = args

    def __call__(self, fun, *args, **kwargs):
        self._function = fun

        if _notebookFunctionExecuted(fun):
            _callFunction(fun, self._decoratorArgs)

        return self
