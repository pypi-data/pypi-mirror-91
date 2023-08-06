# pylint: disable = protected-access
from databricksbundle.notebook.decorator.ContainerManager import ContainerManager

class DecoratorMetaclass(type):

    def __new__(cls, name, bases, attrs):
        def decorate(decorator, *args):
            if args:
                decorator._function = args[0]
                decorator._result = decorator.onExecution(ContainerManager.getContainer())
            else:
                decorator.onImport()

            return decorator

        attrs['__call__'] = decorate

        return super(DecoratorMetaclass, cls).__new__(cls, name, bases, attrs)
