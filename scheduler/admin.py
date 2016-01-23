from django.contrib import admin

from .models import ConstraintDescription, JobDescription, Event, Volunteer, \
    Job


@admin.register(ConstraintDescription)
class ConstraintDescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    fields = ('event', 'real_name', 'email_address', 'phone_number',
              'public_name', 'slug', 'constraints')
    readonly_fields = ('public_name', 'slug')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass
