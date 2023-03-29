from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from dashboard.models import Nids


def dashboard(request):
    # Retrieve data from the database
    data = Nids.objects.values('timestamp', 'total_fwd_packet_size')

    # Transform the data into the format expected by Chart.js
    labels = []
    values = []
    for row in data:
        labels.append(str(row['timestamp']))
        values.append(row['total_fwd_packet_size'])

    # Pass the data to the template
    context = {
        'labels': labels,
        'values': values,
    }
    return render(request, 'dashboard.html', context)
