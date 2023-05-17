from django.db import models

#
"id SERIAL PRIMARY KEY",
"timestamp TIMESTAMP DEFAULT NOW()",
"flow_id VARCHAR(50)",
"sender_ip VARCHAR(15)",
"protocol VARCHAR(5)",
"flow_duration FLOAT",
"flow_iat_mean FLOAT",
"fwd_iat_tot FLOAT",
"bwd_bytes_per_avg FLOAT",
"bwd_pkts_per_avg FLOAT",
"bwd_blk_rate_avg FLOAT",
"subflow_fwd_pkts INT",
"subflow_fwd_bytes INT",
"fwd_act_data_pkts INT",
"fwd_seg_size_min INT"

#
class nids(models.Model):
    id = models.AutoField(primary_key=True)
    flow_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    flow_duration = models.FloatField()
    flow_iat_mean = models.FloatField()
    fwd_iat_tot = models.FloatField()
    subflow_fwd_pkts = models.IntegerField()
    subflow_fwd_bytes = models.IntegerField()
    fwd_act_data_pkts = models.IntegerField()
    fwd_seg_size_min = models.IntegerField()
    bwd_pkts_count = models.IntegerField()
    bwd_bytes_per_avg = models.FloatField()
    bwd_payload_count = models.IntegerField()
    bwd_payload_bytes_per_avg = models.FloatField()
    bwd_blk_rate_avg = models.FloatField()
    bwd_pkts_per_avg = models.FloatField()

    class Meta:
        db_table = 'nids'


class typing_stats(models.Model):
    timestamp = models.DateTimeField()
    keystroke_counter = models.IntegerField()
    erase_keys_counter = models.IntegerField()
    erase_keys_percentage = models.FloatField()
    press_press_average_interval = models.FloatField()
    press_press_stddev_interval = models.FloatField()
    press_release_average_interval = models.FloatField()
    press_release_stddev_interval = models.FloatField()
    word_counter = models.IntegerField()
    word_average_length = models.FloatField()
    word_stddev_length = models.FloatField()
    active_apps_average = models.FloatField()
    current_app = models.CharField(max_length=255)
    penultimate_app = models.CharField(max_length=255)
    current_app_foreground_time = models.IntegerField()
    current_app_average_processes = models.FloatField()
    current_app_stddev_processes = models.FloatField()
    cpu_percent = models.IntegerField(default=0)
    ram_percent = models.IntegerField(default=0)
    bytes_sent = models.IntegerField(default=0)
    bytes_received = models.IntegerField(default=0)

    class Meta:
        db_table = 'typing_stats'


class Alert(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    src_ip = models.GenericIPAddressField()
    dst_ip = models.GenericIPAddressField()
    src_port = models.PositiveIntegerField()
    dst_port = models.PositiveIntegerField()

    class Meta:
        db_table = 'alerts'


class IpMalicious(models.Model):
    ip_address = models.GenericIPAddressField(primary_key=True)
    is_malicious = models.BooleanField(default=False)
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=5)

    class Meta:
        db_table = 'ip_malicious'
