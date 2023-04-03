from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse

from dashboard.models import typing_stats, nids
from django.db.models import Count, F, Window, Subquery, OuterRef
from django.db import models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import logout
from django.shortcuts import redirect


def fetch_cpu_data(request):
    # Retrieve data from the database for TypingStats model
    data = typing_stats.objects.order_by('-timestamp').values('timestamp', 'cpu_percent')[:10]

    # Transform the data into the format expected by Chart.js
    labels = []
    values = []
    for row in reversed(data):
        labels.append(row['timestamp'].strftime('%H:%M:%S'))
        values.append(row['cpu_percent'])

    # Create a dictionary containing the labels and values
    chart_data = {
        'labels': labels,
        'values': values
    }

    # Return the data as a JSON response
    return JsonResponse(chart_data)


def fetch_ram_data(request):
    # Retrieve data from the database for TypingStats model
    data = typing_stats.objects.order_by('-timestamp').values('timestamp', 'ram_percent')[:10]

    # Transform the data into the format expected by Chart.js
    labels = []
    values = []
    for row in reversed(data):
        labels.append(row['timestamp'].strftime('%H:%M:%S'))
        values.append(row['ram_percent'])

    # Create a dictionary containing the labels and values
    chart_data = {
        'labels': labels,
        'values': values
    }

    # Return the data as a JSON response
    return JsonResponse(chart_data)


@login_required
def dashboard(request):
    # Retrieve data from the database for TypingStats model
    typing_data = typing_stats.objects.values('current_app').annotate(usage=Count('current_app')).order_by('-usage')[
                  :10]

    # Transform the data into the format expected by Chart.js for TypingStats model
    typing_labels = []
    typing_values = []
    for row in typing_data:
        typing_labels.append(row['current_app'])
        typing_values.append(row['usage'])

    # Pass the data to the template
    context = {
        'typing_labels': typing_labels,
        'typing_values': typing_values,
    }
    return render(request, 'dashboard.html', context)


def fetch_data(request):
    # Retrieve data from the database
    data = nids.objects.values('timestamp', 'flow_duration')

    # Transform the data into the format expected by Chart.js
    labels = []
    values = []
    for row in data:
        timestamp = int(row['timestamp'].timestamp())
        label = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        labels.append(label)
        values.append(row['flow_duration'])
    # Create a dictionary containing the labels and values
    chart_data = {
        'labels': labels,
        'values': values
    }

    # Return the data as a JSON response
    return JsonResponse(chart_data)


def fetch_app_data(request):
    # Retrieve data from the database for TypingStats model
    data = typing_stats.objects.values('current_app').annotate(usage=Count('current_app')).order_by('-usage')[:10]

    # Transform the data into the format expected by Chart.js
    labels = []
    values = []
    for row in data:
        labels.append(row['current_app'])
        values.append(row['usage'])

    # Create a dictionary containing the labels and values
    chart_data = {
        'labels': labels,
        'values': values
    }

    # Return the data as a JSON response
    return JsonResponse(chart_data)


def fetch_typing_data(request):
    # Retrieve data from the database for TypingStats model
    previous_keystroke = typing_stats.objects.filter(
        timestamp__lt=OuterRef('timestamp')
    ).order_by('timestamp').values('keystroke_counter')[:1]

    data = typing_stats.objects.annotate(
        keystroke_diff=F('keystroke_counter') - Subquery(previous_keystroke, output_field=models.IntegerField())
    ).values('timestamp', 'keystroke_diff')

    # Transform the data into the format expected by Chart.js
    labels = []
    values = []
    for row in data:
        labels.append(row['timestamp'].strftime('%H:%M:%S'))
        values.append(row['keystroke_diff'])

    # Create a dictionary containing the labels and values
    chart_data = {
        'labels': labels,
        'values': values
    }

    # Return the data as a JSON response
    return JsonResponse(chart_data)


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))  #


def nids_logs(request):
    return render(request, 'nids_logs.html')


def fetch_nids_data(request):
    nids_data = nids.objects.values(
        'timestamp', 'flow_id', 'flow_duration', 'flow_iat_mean', 'fwd_iat_tot',
        'subflow_fwd_pkts', 'subflow_fwd_bytes', 'fwd_act_data_pkts', 'fwd_seg_size_min',
        'bwd_pkts_count', 'bwd_bytes_per_avg', 'bwd_payload_count', 'bwd_payload_bytes_per_avg',
        'bwd_blk_rate_avg', 'bwd_pkts_per_avg'
    ).order_by('-timestamp')[:100]

    data = list(nids_data)
    for item in data:
        item['timestamp'] = item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    return JsonResponse({'data': data})
