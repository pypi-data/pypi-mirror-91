'''
    Body module.

Defines a Body object for the
Person's object in fitpy.
Person and Body are defined
independently, but can be
defined together.
Both objects can also be added
and/or use the objects defined
in sports.py .
'''

from . import exceptions


class Body:

    '''
        Body Class.

    :param age: Age of the Person in years
    :type age: int, protected
    :param height: Height of the Person in cm
    :type height:  float, protected
    :param weight: Weight of the Person in kg
    :type weight:  float, protected
    :param hormonal_sex: Hormonal Sex of the Person
    :type hormonal_sex: string, protected
    :param waist: Waist size of the Person in cm
    :type waist: float, protected
    :param hip: Hip size of the Person in cm
    :type hip: float, protected
    '''

    def __init__(self, age, height, weight,
                    hormonal_sex=None,
                    waist=None,
                    hip=None,
                ):
        super().__init__()

        self._age = age
        self._height = height
        self._weight = weight
        self._hormonal_sex = hormonal_sex
        self._waist = waist
        self._hip = hip

    @property
    def bmi(self):
        '''
            Get the BMI.

        The bmi is calculated with
        the weight in kg divided by
        the square ofthe height
        in meters;
        In general the Ponderal Index
        is more expressive.

        :return: Returns the Body-Mass-Index
        :rtype: float

        :Example:
            >>> Body(22, 120, 80).bmi
            55.6
        '''
        return float('%.1f' % (self._weight / ((self._height/100) ** 2)))

    @property
    def ponderal_index(self):
        '''
            Get the Ponderal Index

        The ponderal index is calculated
        by the weight in kg divided by
        the height in meters to the
        power of three.

        -> Results between 11 and 14
        are interpreted as normal.

        :return: Returns the Ponderal Index
        :rtype: float
        '''
        return float('%.1f' % (self._weight / ((self._height/100) ** 3)))

    @property
    def broca_index(self):
        '''
            Get Broca Index

        :return: Returns the Broca Index
        :rtype: float
        '''
        return float('%.1f' % (self._weight / (self._height - 100) * 100))

    @property
    def metabolic_rate(self):
        '''
            Get the Basal Metabolic Rate

        The basal metabolic rate is calculated
        with the weight * 24 (hours);
        It is not really expressive, as it is
        igonring body facts which have influence
        on this, like muscle mass.
        It is recommended to use the Harris-
        Benedict Formula instead.

        :return: Returns the Metabolic Rate
        :rtype: int
        :Example:
            >>> Body(22, 180, 50).metabolic_rate
            1200
        '''
        return int(self._weight * 24)

    @property
    def harris_benedict_equation(self):
        '''
            Get the BMR based on the
            Harris-Benedict equation

        Hormonal Female:
            BMR = 655 + (9.6 X weight in kilos)
                + (1.8 X height in cm) – (4.7 x age in years)

        Hormonal Male:
            BMR = 66 + (13.7 x weight in kilos)
                + (5 x height in cm) – (6.8 x age in years)

        :return: Returns the Daily calory need
        :rtype: int

        if obj._hormonal_sex is not defined:
            :raise: AttributeError
        '''

        try:
            if self._hormonal_sex == 'male':
                return int(66 + (13.7 * self._weight) \
                        + (5 * self._height) \
                        - (6.8 * self._age))

            elif self._hormonal_sex == 'female':
                return int(655 + (9.6 * self._weight) \
                        + (1.8 * self._height) \
                        - (4.7 * self._age))

            else:
                return 'Raise Error'

        except AttributeError as no_hormsex:
            raise exceptions.HormonalSexNotDefined(no_hormsex) from no_hormsex
        else:
            pass

    @property
    def waist2hip_ratio(self):
        '''
            Get the Waist-to-Hip Ratio

        :return: Returns the W-H-Ratio
        :rtype: float
        '''
        try:
            return self._waist / self._hip

        except AttributeError:
            pass#raise exceptions.WaistOrHipNotDefined
        except TypeError:
            pass#raise exceptions.WaistOrHipNotDefined
        else:
            pass

# Add informations!
    @property
    def max_heartrate_moderate(self):
        ''' Age predicted Maximum
            Heart Rate

        (BPM)

        :return: The max Heart Rate
        :rtype: int
        '''
        return 220 - self._age

    def asdict(self):
        '''
            As dict Module

        Get all param as dict.

        :return: Dicitonary of all attributes
            of :class:
        :rtype: dict
        '''
        try:
            param_dict = {
                'age' : self._age,
                'height' : self._height,
                'weight' : self._weight,
                'hormonal_sex' : self._hormonal_sex,
                'waist' : self._waist,
                'hip' : self._hip,
                'bmi' : self.bmi,
                'ponderal' : self.ponderal_index,
                'broca' : self.broca_index,
                'metabolic' : self.metabolic_rate,
                'hbe' : self.harris_benedict_equation,
                'w2h' : self.waist2hip_ratio,
            }

        except AttributeError:
            pass#raise exceptions.BodyParamIsNotExisting
        else:
            pass

        return param_dict

    def __repr__(self):
        represent = f'''Body(
            _height={self._height},
            _weight={self._weight},
            )'''
        return represent

    def __str__(self):

        represent = f'''\n
        Age:                {self._age}

        Height:             {self._height}
        Weight:             {self._weight}
        Hormonal Sex:       {self._hormonal_sex}

        BMI:                {self.bmi}

        Ponderal Index:     {self.ponderal_index} kg/m³

        Broca Index:        {self.broca_index}

        Metabolic Rate:     {self.metabolic_rate} kcal

        Harris-Benedict:    {self.harris_benedict_equation} kcal

        Waist-to-Hip Ratio: {self.waist2hip_ratio}
        '''
        return represent





if __name__ == '__main__':
    import doctest

    doctest.testmod()


    import fire

    fire.Fire(Body)
