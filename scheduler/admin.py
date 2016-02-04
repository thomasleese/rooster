from django import forms
from django.contrib import admin

from .models import Resource, Event, Job, JobResource, Volunteer, \
    VolunteerResource, ScheduleEntry


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'visible', 'default_value')
    list_filter = ('type', 'visible')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slots_per_day', 'number_of_days')


class JobResourceInline(admin.TabularInline):
    model = JobResource


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (JobResourceInline,)


class VolunteerResourceInline(admin.TabularInline):
    model = VolunteerResource


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('real_name', 'public_name', 'event')
    list_filter = ('event',)
    fields = ('event', 'real_name', 'email_address', 'phone_number',
              'public_name', 'slug')
    readonly_fields = ('public_name', 'slug')
    inlines = (VolunteerResourceInline,)


class ManualScheduleEntryAdminForm(forms.ModelForm):
    class Meta:
        model = ScheduleEntry
        exclude = ['manual']

    def save(self, *args, **kwargs):
        # Jobs allocated by an admin are marked as manually allocated.
        self.instance.manual = True
        return super().save(*args, **kwargs)


@admin.register(ScheduleEntry)
class ManualScheduleEntryAdmin(admin.ModelAdmin):
    form = ManualScheduleEntryAdminForm
    list_display = ('event', 'job', 'volunteer', 'day', 'time_slot', 'manual')
    list_filter = ('event',)
