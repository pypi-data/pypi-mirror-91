'''
    Custom Errors thrown in the fit Module

1 The Hormonal Sex was not defined but needed for a module / function / ...
2 The Waist and/or Hip size was not define but needed ...
'''


class HormonalSexNotDefined(Exception):
    ''' Raised if the Hormonal Sex
        was not defined before calling.
    '''
    def __init__(self):
        Exception.__init__(
            self,
            'The Hormonal Sex needs to be defined for this equation.'
        )

class WaistOrHipNotDefined(Exception):
    ''' Raised if either the size
        of the waist or the hips was
        not defined before calling.
    '''
    def __init__(self):
        Exception.__init__(
            self,
            'The Waist and Hip size need to be defined for this quation.'
        )


class BodyParamIsNotExisting(Exception):
    ''' Raised if one param
        is not existing
    '''
    def __init__(self):
        Exception.__init__(
            self,
            'Some params are missing.'
        )
