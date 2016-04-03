import random
from scheduler.models import Volunteer, Job, JobResource, VolunteerResource, ScheduleEntry, JobSumResource

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
        job_res_variables = self.get_non_per_participant_job_resources(solver, variables)
        # Apply the minimum constraints for the job resources which are not per-participant
        for j in job_res_variables:
            solver.Add(j["var"] >= j["min"])
        solution = solver.Assignment()
        solution.Add(list(variables.values()))

        # optimise for the target values
        optimisation_variables = []
        for j in job_res_variables:
            optimisation_variables.append(solver.Max(j["target"] - j["var"], 0))
        optimisation_variable = solver.Sum(optimisation_variables)

        # collector = solver.BestValueSolutionCollector(solution, False)
        collector = solver.LastSolutionCollector(solution)

        minimise_obj = solver.Minimize(optimisation_variable, 1)
        print(minimise_obj)

        solver.Solve(
            solver.Phase(
                list(variables.values()),
                solver.CHOOSE_FIRST_UNBOUND,
                solver.ASSIGN_MIN_VALUE
            ),
            [collector, minimise_obj]
        )

        sol_count = collector.SolutionCount()
        print("Solutions:", sol_count)
        solutions = {}
        if sol_count > 0:
            for k, v in variables.items():
                value = collector.Value(0, v)
                # print(v, ":", value)
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

    def get_non_per_participant_job_resources(self, solver, variables):
        """
        Get solver variables for the non-per-participant job resources
        :param solver: the solver to create the variables for
        :param variables: the variables to calculate the new variable for
        :return: an array of dictionaries:
        [{
        "var": <The solver variable>,
        "min": <the minimum value for the resource>,
        "target": <the target value for the resource>
        },
        ...
        ]
        """
        new_variables = []
        for job in self.jobs:
            # Get every resource that isn't per volunteer
            resources = JobSumResource.objects.filter(job=job)

            # For each resource
            for res in resources:
                participant_resources = {}
                # Call all the database queries and store them
                for participant in self.participants:
                    participant_resources[participant] = VolunteerResource.objects.get(
                        volunteer=participant,
                        resource=res.resource
                    )
                # For each timeslot
                for time in self.timeslots:
                    relevant_variables = []
                    multipliers = []
                    # Get the variables which affect this job at this timeslot
                    for k, v in variables.items():
                        res_job = k[1]
                        res_time = k[2]
                        if res_job == job and res_time == time:
                            res_person = k[0]
                            if res_person in participant_resources:
                                relevant_variables.append(v)
                                multipliers.append(participant_resources[res_person].value)

                    # Create a variable which is the sum of each participants resource values.
                    new_variable = solver.ScalProd(relevant_variables, multipliers)
                    # Put the value in a dictionary with its target and minimum values
                    new_variables.append({"var": new_variable, "min": res.min_value, "target": res.target_value})

        return new_variables
