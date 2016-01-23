from enum import Enum

from django.db import models


class ConstraintTemplate(models.Model):
    class DataType(Enum):
        integer = 'int'
        boolean = 'bool'

    DATA_TYPE_CHOICES = ((DataType.integer.value, 'Integer'),
                         (DataType.boolean.value, 'True/False'))

    name = models.CharField(max_length=200)
    description = models.TextField()
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES)


class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()

    day_length = models.PositiveSmallIntegerField()
    day_count = models.PositiveSmallIntegerField()

    volunteer_constraints = models.ForeignKey(ConstraintTemplate,
                                              related_name='volunteer_events',
                                              on_delete=models.CASCADE)
    job_constraints = models.ForeignKey(ConstraintTemplate,
                                        related_name='job_events',
                                        on_delete=models.CASCADE)


class Constraint(models.Model):
    template = models.ForeignKey(ConstraintTemplate, on_delete=models.CASCADE)

    integer_value = models.IntegerField(null=True)
    boolean_value = models.NullBooleanField()

    @property
    def value(self):
        if self.template.data_type == ConstraintTemplate.DataType.integer:
            return self.int_value
        elif self.template.data_type == ConstraintTemplate.DataType.boolean:
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


class Job(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.TextField()

    constraints = models.ForeignKey(Constraint, on_delete=models.CASCADE)
