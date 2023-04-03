$(document).ready(function () {
    var table = $('#nidsLogsTable').DataTable({
        ajax: {
            url: '/dashboard/fetch_nids_data/', dataSrc: 'data'
        },
        columns: [{data: 'timestamp'}, {data: 'flow_id'}, {data: 'flow_duration'}, {data: 'flow_iat_mean'}, {data: 'fwd_iat_tot'}, {data: 'subflow_fwd_pkts'}, {data: 'subflow_fwd_bytes'}, {data: 'fwd_act_data_pkts'}, {data: 'fwd_seg_size_min'}, {data: 'bwd_pkts_count'}, {data: 'bwd_bytes_per_avg'}, {data: 'bwd_payload_count'}, {data: 'bwd_payload_bytes_per_avg'}, {data: 'bwd_blk_rate_avg'}, {data: 'bwd_pkts_per_avg'}],
        order: [[0, 'desc']]
    });

    function updateTable() {
        table.ajax.reload(null, false);
    }

    setInterval(updateTable, 50000); // Update every 5 seconds
});
