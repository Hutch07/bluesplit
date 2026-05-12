from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import FlightForm, SiteAccessForm
from .models import Site


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


@login_required
def site_access(request):
    if not is_pilot_or_admin(request.user):
        messages.error(request, 'You do not have permission to manage site access.')
        return redirect('dashboard')

    selected_site = None
    form = SiteAccessForm()

    # If a site is already selected (GET with ?site=id or after POST), load it
    site_id = request.POST.get('site') or request.GET.get('site')
    if site_id:
        try:
            selected_site = Site.objects.get(pk=site_id)
        except Site.DoesNotExist:
            selected_site = None

    if request.method == 'POST':
        if 'load_site' in request.POST:
            # Just loading the site to show current users — re-render with pre-filled checkboxes
            if selected_site:
                form = SiteAccessForm(initial={
                    'site': selected_site,
                    'allowed_users': selected_site.allowed_users.all(),
                })
        elif 'save_access' in request.POST:
            form = SiteAccessForm(request.POST)
            if form.is_valid():
                site = form.cleaned_data['site']
                users = form.cleaned_data['allowed_users']
                site.allowed_users.set(users)
                site.save()
                messages.success(request, f'Allowed users updated for {site.name}.')
                return redirect(f"{request.path}?site={site.pk}")
    else:
        if selected_site:
            form = SiteAccessForm(initial={
                'site': selected_site,
                'allowed_users': selected_site.allowed_users.all(),
            })

    return render(request, 'core/site_access.html', {
        'form': form,
        'selected_site': selected_site,
    })


