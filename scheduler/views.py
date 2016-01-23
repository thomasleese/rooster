from django.shortcuts import get_object_or_404, render

from .forms import VolunteerForm
from .models import Event, VolunteerResource


def volunteer(request, slug):
    event = get_object_or_404(Event, slug=slug)

    resources = event.resources

    form = VolunteerForm(request.POST or None, resources=resources)

    print(form.errors)

    if form.is_valid():
        volunteer = form.save()

        for resource in resources:
            value = form.cleaned_data[form.get_id_for_resource(resource)]
            r = VolunteerResource(volunteer=volunteer, resource=resource,
                                  value=value)
            r.save()

    context = {'form': form, 'event': event}
    return render(request, 'scheduler/volunteer.html', context)
