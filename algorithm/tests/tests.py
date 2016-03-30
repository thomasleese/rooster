from django.test import TestCase
from algorithm.timetable_solver import TimetableSolver
from scheduler.models import Event, Volunteer, Job, JobResource, VolunteerResource, Resource, ScheduleEntry


class MyTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(name="SR", slots_per_day=10, number_of_days=2)

        # Resources

        knowsTheKit = Resource.objects.create(
            name="KnowsTheKit",
            description="Knows The Kit",
            type=Resource.Type.integer,
            min_value=5,
            max_value=10
        )

        teaMaking = Resource.objects.create(
            name="TeaMaking",
            description="Knows how to make tea",
            type=Resource.Type.boolean,
            min_value=False,
            max_value=True
        )

        # Jobs

        helpDesk = Job.objects.create(
            event=self.event,
            name="HelpDesk",
            description="Helping at a desk"
        )
        JobResource.objects.create(
            resource=knowsTheKit,
            job=helpDesk,
            min_value=5,
            target_value=10
        )

        catering = Job.objects.create(
            event=self.event,
            name="Catering",
            description="Catering"
        )

        JobResource.objects.create(
            resource=teaMaking,
            job=catering,
            min_value=True,
            target_value=True
        )

        # Volunteers

        tom = Volunteer.objects.create(
            event=self.event,
            real_name="Tom Release",
            email_address="test@example.com",
        )

        VolunteerResource.objects.create(resource=knowsTheKit, volunteer=tom, value=9)
        VolunteerResource.objects.create(resource=teaMaking, volunteer=tom, value=True)

        james = Volunteer.objects.create(
            event=self.event,
            real_name="James Listerine",
            email_address="test@example.com",
        )
        VolunteerResource.objects.create(resource=knowsTheKit, volunteer=james, value=6)
        VolunteerResource.objects.create(resource=teaMaking, volunteer=james, value=False)

        samson = Volunteer.objects.create(
            event=self.event,
            real_name="Samson Zinger",
            email_address="test@example.com",
        )
        VolunteerResource.objects.create(resource=knowsTheKit, volunteer=samson, value=8)
        VolunteerResource.objects.create(resource=teaMaking, volunteer=samson, value=True)

        self.catering = catering
        self.helpDesk = helpDesk
        self.tom = tom
        self.james = james
        self.samson = samson

    #
    # def test_format(self):
    #     TimetableSolver(self.event, self.participants, self.jobs)

    def test_can_do(self):
        self.assertTrue(self.tom.can_do_job(self.helpDesk), "Volunteer seemingly can't do a job even though they can.")

    def test_cant_do(self):
        self.assertFalse(self.james.can_do_job(self.catering), "Volunteer assigned to job when they aren't meant to.")

    def test_time_slots(self):
        solver = TimetableSolver(self.event, [self.tom, self.samson, self.james], [self.helpDesk, self.catering])
        results = solver.run()
