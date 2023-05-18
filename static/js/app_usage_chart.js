document.addEventListener('DOMContentLoaded', function () {
    var appUsageData = {
        labels: [],
        datasets: [{
            label: 'App Usage',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1
        }]
    };

    var ctx = document.getElementById('appUsageChart').getContext('2d');
    var apiUrl = ctx.canvas.dataset.url;

    var appUsageChart = new Chart(ctx, {
        type: 'bar',
        data: appUsageData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    function updateAppUsageChart() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                appUsageChart.data.labels = data.labels;
                appUsageChart.data.datasets[0].data = data.values;
                appUsageChart.update();
            });
    }

    updateAppUsageChart();
    setInterval(updateAppUsageChart, 500);
});
