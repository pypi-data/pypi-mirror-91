'''
    sports Module

Containing different sports and activity
classes which provide modules.
Most classes need the body object as
specific attributes are often needed,
they are set as optional parameters as
some modules or attributes can be used
without specific attr.
More help is provided in each class.
'''

class Running:
    '''
        Running class
    :param body: Instance of an object which has
                     needed parameters
    :type body: class: Body, optional, private
    :param km_run: The distance which was run in km
    :type km_run: float, optional, protected
    :param time_sport: The duration of the activity in minutes
    :type time_sport: int, optional , protected
    '''
    def __init__(self, body=None, km_run=0.0, time_sport=0):
        self.__body = body
        self._km_run = km_run
        self._time_sport = time_sport

    @property
    def calories_used(self):
        '''
        # Add Informations
        '''
        return self._km_run * self.__body._weight * 0.9

    @property
    def run_pace(self):
        '''
        # Add Informations
        '''
        tmp = self._time_sport / self._km_run
        t = tmp - int(tmp)
        t *= 60   # to get minutes
        pace = int(tmp) + (t - int(t))
        return float('%.2f' % pace)

    def asdict(self):
        '''
            As dict Module

        Get all param as dict.

        :return: Dicitonary of all attributes
            of :class:
        :rtype: dict
        '''
        return {'km_run' : self._km_run,
                'time_sport' : self._time_sport,
                'used_calories' : self.calories_used,
                'run_pace': self.run_pace}

    def __repr__(self):
        represent =  f'''Running(
            body={self.__body},
            km_run={self._km_run},
            time_sport={self._time_sport}
            )'''
        return represent

    def __str__(self):
        return f'''\n
        Kind of activity:   Running

        Duration:       {self._time_sport} min
        Distance:       {self._km_run} km
        Speed:          {self.run_pace} min/km
        Calories used:  {self.calories_used}
         '''
