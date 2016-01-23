from django.contrib import admin

from .models import ConstraintTemplate, Constraint, Event, Volunteer, Job


@admin.register(ConstraintTemplate)
class ConstraintTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    pass


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass
