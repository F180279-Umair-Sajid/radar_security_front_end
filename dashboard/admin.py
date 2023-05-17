from django.contrib import admin
from .models import nids, typing_stats, Alert, IpMalicious


@admin.register(nids)
class NidsAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_id', 'timestamp', 'flow_duration', 'flow_iat_mean', 'fwd_iat_tot')
    list_filter = ('flow_id', 'timestamp', 'flow_duration')
    search_fields = ('flow_id', 'timestamp__date')  # You can customize the search fields based on your requirements


@admin.register(typing_stats)
class TypingStatsAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'keystroke_counter', 'erase_keys_counter', 'word_counter')
    list_filter = ('timestamp', 'current_app')
    search_fields = ('current_app', 'timestamp__date')


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'name', 'description', 'src_ip', 'dst_ip', 'src_port', 'dst_port')
    list_filter = ('timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port')
    search_fields = ('name', 'description', 'src_ip', 'dst_ip')


@admin.register(IpMalicious)
class IpMaliciousAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'is_malicious', 'country', 'country_code')
    list_filter = ('is_malicious', 'country')
    search_fields = ('ip_address', 'country')
