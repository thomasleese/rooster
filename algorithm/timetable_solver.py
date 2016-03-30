import random
from scheduler.models import Volunteer, Job, JobResource, VolunteerResource, ScheduleEntry

random.seed(1)

from ortools.constraint_solver import pywrapcp


class TimetableSolver:
    def __init__(
            self,
            event,
            participants,
            jobs,
    ):
        """
        initialiser for timetable solver
        :param event: The event, (Event object from rooster)
        :param participants: list of all participants (list of Volunteer objects)
        :param jobs: list of all jobs (list of Job objects)
        """
        self.timeslots = range(event.slots_per_day * event.number_of_days)
        self.participants = participants
        # The available times per participant
        # TODO: Get free the time slots from participants
        self.available_times = {k: [True for _ in self.timeslots] for k in self.participants}
        # TODO: Get the opening times for each job
        self.job_open_times = {j: [True for _ in self.timeslots] for j in jobs}
        self.jobs = jobs

    def run(self):
        solver = pywrapcp.Solver("timetable")
        variables = self.get_solver_variables(solver)

        self.apply_single_job_constraints(solver, variables)
        solution = solver.Assignment()
        solution.Add(list(variables.values()))
        collector = solver.FirstSolutionCollector(solution)
        solver.Solve(
            solver.Phase(
                list(variables.values()),
                solver.CHOOSE_FIRST_UNBOUND,
                solver.ASSIGN_MIN_VALUE
            ),
            [collector]
        )

        sol_count = collector.SolutionCount()
        print("Solutions:", sol_count)
        solutions = {}
        if sol_count > 0:
            for k, v in variables.items():
                value = collector.Value(0, v)
                print(v, ":", value)
                solutions[k] = int(value)

        return solutions

    def apply_single_job_constraints(self, solver, variables):
        """
        Apply the constraint that each person can only do 1 thing at a time.
        :param solver: the solver to apply the constraint to
        :param variables: a dictionary of {(participant,job,timeslot):Variable}
        """
        for participant in self.participants:
            for timeslot in self.timeslots:
                clashing_slots = []
                for k, v in variables.items():
                    if k[0] == participant and k[2] == timeslot:
                        clashing_slots.append(v)
                if clashing_slots:
                    solver.Add(1 == solver.Sum(clashing_slots))

    def get_solver_variables(self, solver):
        variables = {}
        for participant in self.participants:
            available_times = self.available_times[participant]
            for job in self.jobs:
                job_times = self.job_open_times[job]
                for timeslot in self.timeslots:
                    # If the volunteer is there to do it
                    if available_times[timeslot] and job_times[timeslot]:
                        # If the volunteer meets the minimum requirements to do it
                        if participant.can_do_job(job):
                            time_name = "{}: '{}' doing '{}'".format(timeslot, participant, job)
                            variables[(participant, job, timeslot)] = solver.IntVar(0, 1, time_name)
        return variables
