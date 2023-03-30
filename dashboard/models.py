from django.db import models


class Nids(models.Model):
    flow_id = models.IntegerField(primary_key=True)
    protocol = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    flow_duration = models.FloatField()
    total_fwd_packets = models.IntegerField()
    total_bwd_packets = models.IntegerField()
    total_fwd_packet_size = models.IntegerField()
    total_bwd_packet_size = models.IntegerField()
    total_fwd_payload_size = models.IntegerField()
    total_bwd_payload_size = models.IntegerField()

    class Meta:
        db_table = 'nids'


class TypingStats(models.Model):
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
    current_app_foreground_time = models.FloatField()
    current_app_average_processes = models.FloatField()
    current_app_stddev_processes = models.FloatField()

    class Meta:
        db_table = 'typing_stats'
