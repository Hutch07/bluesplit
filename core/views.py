from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    is_admin = request.user.is_superuser or request.user.group.filter(name='Admin').exists()
    return render(request, 'core/dashboard.html', {'is_admin': is_admin})
