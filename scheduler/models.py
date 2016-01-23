from enum import Enum

from django.db import models


class ConstraintDescription(models.Model):
    class DataType(Enum):
        integer = 'integer'
        boolean = 'bool'

    DATA_TYPE_CHOICES = ((DataType.integer.value, 'Integer'),
                         (DataType.boolean.value, 'True/False'))

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES)

    def __str__(self):
        return self.name


class JobDescription(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    day_length = models.PositiveSmallIntegerField()
    day_count = models.PositiveSmallIntegerField()

    volunteer_constraints = models.ForeignKey(ConstraintDescription,
                                              related_name='volunteer_events',
                                              on_delete=models.CASCADE)
    job_constraints = models.ForeignKey(ConstraintDescription,
                                        related_name='job_events',
                                        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Constraint(models.Model):
    description = models.ForeignKey(ConstraintDescription,
                                    on_delete=models.CASCADE)

    integer_value = models.IntegerField(null=True)
    boolean_value = models.NullBooleanField()

    def __str__(self):
        return '{}: {}'.format(self.description.name, self.value)

    @property
    def value(self):
        if self.template.data_type == ConstraintDescription.DataType.integer:
            return self.int_value
        elif self.template.data_type == ConstraintDescription.DataType.boolean:
            return self.boolean_value
        else:
            raise ValueError('Unknown data type.')


class Volunteer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    real_name = models.CharField(max_length=200)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20)

    public_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)

    constraints = models.ForeignKey(Constraint, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.real_name, self.public_name)


class Job(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    description = models.ForeignKey(ConstraintDescription,
                                    on_delete=models.CASCADE)

    constraints = models.ForeignKey(Constraint, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.description.name, self.event.name)
