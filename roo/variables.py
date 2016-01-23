class Job(object):

    time = None

    def __init__(self, name, description="", constraints={}):
        self.name = name
        self.description = description
        self.constraints = constraints

    def permitted_at(interval, of_intervals, of_day):
        return True

    def set_time(time_tuple):
        self.time = time_tuple


class Person(object):
    def __init__(self, name, constraints={}):
        self.name = name
        self.constraints = constraints
