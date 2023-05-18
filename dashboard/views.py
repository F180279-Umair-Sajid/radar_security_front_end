from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Count, F, Subquery, OuterRef
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dashboard.models import typing_stats, nids
from .models import Alert


@login_required
def ip_malicious_view(request):
    return render(request, 'notification.html')


@login_required
def alert_view(request):
    # Retrieve distinct IP addresses from the Alert model
    distinct_ips = Alert.objects.values('src_ip').distinct()

    # Fetch the entries with unique IP addresses
    unique_alerts = []
    for ip in distinct_ips:
        alert = Alert.objects.filter(src_ip=ip['src_ip']).last()
        if alert:
            unique_alerts.append(alert)

    # Pass the unique alerts to the HTML template
    context = {
        'alerts': unique_alerts
    }

    # Create a SendGrid client
    message = Mail(
        from_email='umaiesajid@gmail.com',
        to_emails='f180279@cfd.nu.edu.pk',
        subject='Alerts',
        plain_text_content=str(unique_alerts))
    try:
        sg = SendGridAPIClient(
            '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')
        response = sg.send(message)
    except Exception as e:
        print(str(e))

    return render(request, 'alert.html', context)


@login_required
def fetch_cpu_data(request):
    try:
        # Retrieve data from the database
        data = nids.objects.values('timestamp', 'flow_duration')
    except ObjectDoesNotExist:
        return render(request, '404.html')
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


@login_required
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
    try:
        # Retrieve data from the database for TypingStats model
        typing_data = typing_stats.objects.values('current_app').annotate(usage=Count('current_app')).order_by(
            '-usage')[:10]
    except ObjectDoesNotExist:
        return render(request, '404.html')
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


@login_required
def fetch_data(request):
    try:
        # Retrieve data from the database
        data = nids.objects.values('timestamp', 'flow_duration')
    except ObjectDoesNotExist:
        return render(request, '404.html')
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


@login_required
def fetch_app_data(request):
    try:
        # Retrieve data from the database for TypingStats model
        data = typing_stats.objects.values('current_app').annotate(usage=Count('current_app')).order_by('-usage')[:10]
    except ObjectDoesNotExist:
        return render(request, '404.html')
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


@login_required
def fetch_typing_data(request):
    try:
        # Retrieve data from the database for TypingStats model
        previous_keystroke = typing_stats.objects.filter(
            timestamp__lt=OuterRef('timestamp')
        ).order_by('timestamp').values('keystroke_counter')[:1]
    except ObjectDoesNotExist:
        return render(request, '404.html')
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


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))  #


@login_required
def fetch_nids_data(request):
    try:
        nids_data = nids.objects.values(
            'timestamp', 'flow_id', 'flow_duration', 'flow_iat_mean', 'fwd_iat_tot',
            'subflow_fwd_pkts', 'subflow_fwd_bytes', 'fwd_act_data_pkts', 'fwd_seg_size_min',
            'bwd_pkts_count', 'bwd_bytes_per_avg', 'bwd_payload_count', 'bwd_payload_bytes_per_avg',
            'bwd_blk_rate_avg', 'bwd_pkts_per_avg'
        ).order_by('-timestamp')[:100]
    except ObjectDoesNotExist:
        return render(request, '404.html')
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

    def logout_view(request):
        logout(request)
        return redirect(reverse('users:user_login'))  # 'login_app:login' refers to the 'login' view in 'login_app'
