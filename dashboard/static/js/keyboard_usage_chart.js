document.addEventListener('DOMContentLoaded', function () {
    var keyboardUsageData = {
        labels: [],
        datasets: [{
            label: 'Keyboard Usage',
            data: [],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            borderWidth: 1
        }]
    };

    var ctx = document.getElementById('keystrokeChart').getContext('2d');
    var apiUrl = ctx.canvas.dataset.url;

    var keyboardUsageChart = new Chart(ctx, {
        type: 'line',
        data: keyboardUsageData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            elements: {
                line: {
                    tension: 0.4,
                    cubicInterpolationMode: 'monotone'
                }
            }
        }
    });

    function updateKeyboardUsageChart() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                keyboardUsageChart.data.labels = data.labels;
                keyboardUsageChart.data.datasets[0].data = data.values;
                keyboardUsageChart.update();
            });
    }

    updateKeyboardUsageChart();
    setInterval(updateKeyboardUsageChart, 500);
});
