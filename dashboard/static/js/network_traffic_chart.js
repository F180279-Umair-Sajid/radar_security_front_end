document.addEventListener('DOMContentLoaded', function () {
    var lineChartData = {
        labels: [], datasets: [{
            label: 'Network Traffic',
            data: [],
            fill: false,
            cubicInterpolationMode: 'monotone',
            borderColor: 'rgb(172,180,187)',
            borderWidth: 1
        }]
    };

    var ctx = document.getElementById('lineChart').getContext('2d');
    var apiUrl = ctx.canvas.dataset.url;

    var lineChart = new Chart(ctx, {
        type: 'line', data: lineChartData, options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }, elements: {
                line: {
                    tension: 0.4, cubicInterpolationMode: 'monotone'
                }
            }, tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        var label = data.datasets[tooltipItem.datasetIndex].label || '';
                        if (label) {
                            label += ': ';
                        }
                        var value = tooltipItem.yLabel;
                        var timestamp = data.labels[tooltipItem.index];
                        var date = new Date(timestamp * 1000);
                        var hours = date.getHours().toString().padStart(2, '0');
                        var minutes = date.getMinutes().toString().padStart(2, '0');
                        var seconds = date.getSeconds().toString().padStart(2, '0');
                        var timeString = hours + ':' + minutes + ':' + seconds;
                        label += value + ' at ' + timeString;
                        return label;
                    }
                }
            }
        }
    });

    function updateLineChart() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                lineChart.data.labels = data.labels;
                lineChart.data.datasets[0].data = data.values;
                lineChart.update();
            });
    }

    updateLineChart();
    setInterval(updateLineChart, 500);
});
