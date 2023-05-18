document.addEventListener('DOMContentLoaded', function () {
    var usageChartData = {
        labels: [],
        datasets: [
            {
                label: 'CPU Usage',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            },
            {
                label: 'RAM Usage',
                data: [],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }
        ]
    };

    var ctx = document.getElementById('usageChart').getContext('2d');
    var cpuDataUrl = ctx.canvas.dataset.cpuUrl;
    var ramDataUrl = ctx.canvas.dataset.ramUrl;

    var usageChart = new Chart(ctx, {
        type: 'bar',
        data: usageChartData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                display: true,
                position: 'bottom'
            },
            responsive: true
        }
    });

    function updateUsageChart() {
        Promise.all([fetch(cpuDataUrl).then(response => response.json()), fetch(ramDataUrl).then(response => response.json())]).then(data => {
            usageChart.data.labels = data[0].labels;
            usageChart.data.datasets[0].data = data[0].values;
            usageChart.data.datasets[1].data = data[1].values;
            usageChart.update();
        });
    }

    updateUsageChart();
    setInterval(updateUsageChart, 500);
});
