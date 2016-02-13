from django.test import TestCase

from .models import Event, Volunteer


class VolunteerTestCase(TestCase):

    def test_gets_public_name(self):
        event = Event.objects.create(name='event', slug='event',
                                     description='event', slots_per_day=1,
                                     number_of_days=1)
        volunteer = Volunteer.objects.create(event=event,
                                             real_name='Real Name',
                                             email_address='a@b.c',
                                             phone_number='123456789')
        volunteer.ensure_has_public_name()
        self.assertIsNot(volunteer.public_name, None)
        self.assertIsNot(volunteer.slug, None)
