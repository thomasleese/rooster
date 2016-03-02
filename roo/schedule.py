from variables import *
from constraint import *

class Schedule(object):

    def __init__(self, name="", allowed_job_constraints=[], allowed_people_constraints=[], days=2, day_length=4, max_continuous_intervals=-1):
        self.jobs = []
        self.people = []
        self.schedule_exists = False
        self.name = name
        self.allowed_job_constraints = allowed_job_constraints
        self.allowed_people_constraints = allowed_people_constraints
        self.days = days
        self.day_length = day_length
        self.max_continuous_intervals = max_continuous_intervals

        self.schedule_pj = [[{} for j in range(day_length)] for i in range(days)]
        self.schedule_jp = [[{} for j in range(day_length)] for i in range(days)]


    def add_job_constraint(self, constraint):
        self.allowed_job_constraints.append(constraint)

    def add_people_constraint(self, constraint):
        self.allowed_people_constraints.append(constraint)

    def add_job(self, job):
        self.jobs.append(job)

    def add_person(self, person):
        self.people.append(person)

    def get_schedule(self):
        if self.schedule_exists and self.schedule:
            return self.schedule
        else:
            return False

    def _setup_problem(self):
        problem = Problem()
        tasks = []

        for task in self.jobs:
            for d in self.days:
                for i in self.day_length:
                    if task.permitted_at(i, day_length, day):
                        task.set_time((i, d))
                        tasks.append(task)



    def find_next_schedule(self):
        # some magic happens
        problem = self._setup_problem()
        return problem.getSolutions()
