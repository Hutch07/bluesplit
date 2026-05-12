from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import FlightForm


def is_pilot_or_admin(user):
    return user.is_superuser or user.group.filter(name__in=['Pilot', 'Admin']).exists()


def home(request):
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    is_admin = request.user.is_superuser or request.user.group.filter(name='Admin').exists()
    return render(request, 'core/dashboard.html', {
        'is_admin': is_admin,
        'is_pilot_or_admin': is_pilot_or_admin(request.user),
    })


@login_required
def add_flight(request):
    if not is_pilot_or_admin(request.user):
        messages.error(request, 'You do not have permission to log flights.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.pilot = request.user.get_full_name() or request.user.username
            flight.save()
            messages.success(request, 'Flight logged successfully!')
            return redirect('dashboard')
    else:
        form = FlightForm()

    return render(request, 'core/add_flight.html', {'form': form})

