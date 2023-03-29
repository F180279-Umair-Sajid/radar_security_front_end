# app/models.py

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
