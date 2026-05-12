import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import FlightForm, SiteAccessForm
from .models import Site, Flight


def is_pilot_or_admin(user):
    return user.is_superuser or user.group.filter(name__in=['Pilot', 'Admin']).exists()


def home(request):
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    user = request.user
    _is_pilot_or_admin = is_pilot_or_admin(user)
    _is_admin = user.is_superuser or user.group.filter(name='Admin').exists()

    # Pilots and admins see all sites; customers/general see only their allowed sites
    if _is_pilot_or_admin:
        sites = Site.objects.all().order_by('name')
    else:
        sites = user.allowed_sites.all().order_by('name')

    # Selected site from query param
    selected_site = None
    site_id = request.GET.get('site')
    if site_id:
        try:
            candidate = Site.objects.get(pk=site_id)
            if _is_pilot_or_admin or candidate in sites:
                selected_site = candidate
        except Site.DoesNotExist:
            pass

    return render(request, 'core/dashboard.html', {
        'is_admin': _is_admin,
        'is_pilot_or_admin': _is_pilot_or_admin,
        'sites': sites,
        'selected_site': selected_site,
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

    site_id = request.POST.get('site') or request.GET.get('site')
    if site_id:
        try:
            selected_site = Site.objects.get(pk=site_id)
        except Site.DoesNotExist:
            selected_site = None

    if request.method == 'POST':
        if 'load_site' in request.POST:
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


@login_required
def splitmap(request, site_id):
    site = get_object_or_404(Site, pk=site_id)

    # Access check: non-pilot/admin users must be in allowed_users
    if not is_pilot_or_admin(request.user):
        if not site.allowed_users.filter(pk=request.user.pk).exists():
            messages.error(request, 'You do not have access to this site.')
            return redirect('dashboard')

    # Get all flights for this site sorted chronologically
    flights = Flight.objects.filter(site=site).order_by('date')

    if flights.count() < 2:
        messages.error(request, 'This site needs at least 2 flights to use the split map.')
        return redirect(f'/dashboard/?site={site_id}')

    flights_list = list(flights)
    flight_right = flights_list[-1]   # most recent
    flight_left  = flights_list[-2]   # second most recent

    def date_to_key(d):
        # Converts date to folder key format: 2026_0422
        return d.strftime('%Y_%m%d')

    def tile_url(aws_url):
        # aws_url already contains the full base path, append tile suffix
        base = aws_url.rstrip('/')
        return base + '/{z}/{x}/{y}.png'

    # Build flight dict for datepicker: { "2026_0422": "https://.../" }
    flight_dict = {}
    flight_dates = []
    for f in flights_list:
        key = date_to_key(f.date)
        flight_dict[key] = f.aws_url.rstrip('/') + '/'
        flight_dates.append(f.date.strftime('%Y-%m-%d'))

    context = {
        'site': site,
        'flight_left': flight_left,
        'flight_right': flight_right,
        'flight_left_key': date_to_key(flight_left.date),
        'flight_right_key': date_to_key(flight_right.date),
        'flight_left_url': tile_url(flight_left.aws_url),
        'flight_right_url': tile_url(flight_right.aws_url),
        'flight_dict_json': json.dumps(flight_dict),
        'flight_dates_json': json.dumps(flight_dates),
        'flights': flights_list,
    }
    return render(request, 'core/splitmap.html', context)
