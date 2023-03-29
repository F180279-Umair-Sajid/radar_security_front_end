# dashboard/views.py

from django.shortcuts import render
from dashboard.models import Nids


def dashboard(request):
    nids = Nids.objects.order_by('-timestamp')[:25]
    return render(request, 'dashboard.html', {'nids': nids})
