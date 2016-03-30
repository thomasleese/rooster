from enum import Enum
import random

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from . import public_name_data


class Resource(models.Model):
    class Type(Enum):
        integer = 'integer'
        boolean = 'boolean'

    TYPE_CHOICES = ((Type.integer.value, 'Integer'),
                    (Type.boolean.value, 'True/False'))

    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES,
                            default=Type.integer.value)
    visible = models.BooleanField(default=True)
    default_value = models.IntegerField(default=0)
    min_value = models.IntegerField(null=True, blank=True, default=0)
    max_value = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    slots_per_day = models.PositiveSmallIntegerField()
    number_of_days = models.PositiveSmallIntegerField()

    def get_absolute_url(self):
        return reverse('sign_up', args=[str(self.slug)])

    def __str__(self):
        return self.name

    @property
    def resources(self):
        resources = []
        for job in self.jobs.all():
            for r in job.resources.all():
                resources.append(r.resource)
        return set(resources)


class Job(models.Model):
    event = models.ForeignKey(Event, related_name='jobs',
                              on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class JobResource(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name='resources',
                            on_delete=models.CASCADE)
    min_value = models.IntegerField()
    target_value = models.IntegerField()

    def __str__(self):
        return '{} for {}: min={}; target={}'.format(self.resource, self.job,
                                                     self.min_value,
                                                     self.target_value)


class Volunteer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    real_name = models.CharField(max_length=200)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20)

    public_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return '{} ({})'.format(self.real_name, self.public_name)

    def generate_public_name(self):
        adjective = random.choice(public_name_data.ADJECTIVES)
        noun = random.choice(public_name_data.BIRDS)
        return '{} {}'.format(adjective, noun)

    def ensure_has_public_name(self):
        if not self.public_name:
            self.public_name = self.generate_public_name()
            self.slug = slugify(self.public_name)

            # TODO: check this is unique

    def can_do_job(self, job: Job):
        resource_minimums = {}

        for jr in JobResource.objects.filter(job=job):
            resource_minimums[jr.resource] = jr.min_value

        for vr in VolunteerResource.objects.filter(volunteer=self):
            resource = vr.resource
            if resource in resource_minimums:
                # Check the volunteer resource is higher than the minimum
                if vr.value < resource_minimums[resource]:
                    return False
                del resource_minimums[resource]

        # The volunteer is missing a resource needed for the job.
        if len(resource_minimums) > 0:
            return False
        else:
            return True


@receiver(signals.pre_save, sender=Volunteer)
def volunteer_pre_save(sender, instance, **kwargs):
    instance.ensure_has_public_name()


class VolunteerResource(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, related_name='resources',
                                  on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} for {}: {}'.format(self.resource, self.volunteer,
                                      self.value)


class ScheduleEntryQuerySet(models.QuerySet):
    def for_event(self, event):
        return self.filter(event=event)

    def for_volunteer(self, volunteer):
        return self.filter(volunteer=volunteer)

    def with_allocation_ordering(self):
        return self.order_by('time_slot', 'day')


class ScheduleEntry(models.Model):
    event = models.ForeignKey(Event, related_name='schedule',
                              on_delete=models.CASCADE)

    job = models.ForeignKey(Job, related_name='+', on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, related_name='+',
                                  on_delete=models.CASCADE)
    day = models.IntegerField()
    time_slot = models.IntegerField()
    manual = models.IntegerField(default=0)

    entries = ScheduleEntryQuerySet.as_manager()
