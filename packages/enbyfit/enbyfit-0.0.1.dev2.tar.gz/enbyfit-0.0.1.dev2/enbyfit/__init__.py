'''
    Init File of fitpy package

All modules are imported here
so each :class: can be used
independently.
'''


__author__ = 'm1ghtfr3e'
__version__ = '0.0.1.dev1'


from .person import Person
from .body import Body
from .sports import Running
from . import exceptions
from .helper import Database


def main():
    ''' Entry Point to
        call __main__
    '''
    import runpy
    runpy.run_module(__name__)
