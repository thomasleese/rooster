from django.shortcuts import get_object_or_404, render, redirect

from .forms import SignUpForm
from .models import Event, VolunteerResource


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
        return redirect('sign_up_success',slug)
    else:
        context = {'form': form, 'event': event}
        return render(request, 'scheduler/sign_up.html', context)

def sign_up_success(request, slug):
    event = get_object_or_404(Event, slug=slug)

    resources = event.resources

    context = {'event': event}
    return render(request, 'scheduler/sign_up_success.html', context)
