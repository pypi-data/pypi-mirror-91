from importlib.metadata import version

__version__ = version('printfactory')


from .printer import *

__all__ = [
    'Printer'
]
