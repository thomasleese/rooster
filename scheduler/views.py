from django.shortcuts import get_object_or_404, render, redirect

from .forms import SignUpForm
from .models import Event, VolunteerResource, Volunteer, ScheduleEntry


def sign_up(request, slug):
    event = get_object_or_404(Event, slug=slug)

    resources = event.resources

    form = SignUpForm(request.POST or None, resources=resources)

    if form.is_valid():
        volunteer = form.save(commit=False)
        volunteer.event = event
        volunteer.save()

        for resource in resources:
            value = form.cleaned_data[form.get_id_for_resource(resource)]
            r = VolunteerResource(volunteer=volunteer, resource=resource,
                                  value=value)
            r.save()

        volunteer.save()
        form.save_m2m()
        return redirect('sign_up_success', slug)
    else:
        context = {'form': form, 'event': event}
        return render(request, 'scheduler/sign_up.html', context)


def sign_up_success(request, slug):
    event = get_object_or_404(Event, slug=slug)

    context = {'event': event}
    return render(request, 'scheduler/sign_up_success.html', context)


def volunteer_timetable(request, eventslug, volunteerslug):
    try:
        event = Event.objects.get(slug=eventslug)
    except Event.DoesNotExist:
        return volunteer_timetable_notfound(request, eventslug, volunteerslug)

    try:
        volunteer = Volunteer.objects.get(slug=volunteerslug)
    except Volunteer.DoesNotExist:
        return volunteer_timetable_notfound(request, eventslug, volunteerslug)

    if volunteer.event != event:
        return volunteer_timetable_notfound(request, eventslug, volunteerslug)

    jobs_list = ScheduleEntry.objects \
        .filter(event=event, volunteer=volunteer) \
        .order_by('time_slot', 'day')

    number_of_days = event.number_of_days
    slots_per_day = event.slots_per_day

    allocations = [[0] * number_of_days] * slots_per_day
    for allocation in jobs_list:
        allocations[allocation.time_slot - 1][allocation.day - 1] = allocation

    context = {
        'event': event,
        'volunteer': volunteer,
        'number_of_days': range(1, number_of_days+1),
        'slots_per_day': range(1, slots_per_day+1),
        'allocations': allocations
    }

    return render(request, 'scheduler/volunteer_timetable.html', context)


def volunteer_timetable_notfound(request, eventslug, volunteerslug):
    context = {'event': eventslug, 'volunteer': volunteerslug}
    return render(request, 'scheduler/timetable_not_found.html', context)
