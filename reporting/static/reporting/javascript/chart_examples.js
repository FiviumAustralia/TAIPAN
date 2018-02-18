window.chartColors = {
    red: '#FFB6A8',
    orange: '#FFCFA8',
    yellow: '#FFE2A8',
    green: '#BFE799',
    blue: '#6E9FA6',
    purple: '#8F7FB7',
    grey: '#545454'
};

var randomScalingFactor = function(val) {
    var max = 100
    if(val) {
        max = val;
    }
    return Math.round(Math.random() * max);
};

var pieConfig = {
    type: 'pie',
    data: {
        datasets: [{
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
            ],
            backgroundColor: [
                window.chartColors.red,
                window.chartColors.orange,
                window.chartColors.green,
            ],
            label: 'Dataset 1'
        }],
        labels: [
            "Red",
            "Orange",
            "Green",
        ]
    },
    options: {
        responsive: true,
        legend: {
            display: false
        },
        tooltips: {
            enabled: false
        }
    }
};

var barConfig = {
    type: 'bar',
    data: {
        datasets: [
        {
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
            ],
            backgroundColor: window.chartColors.red,
            label: 'Dataset 1'
        },
        {
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
            ],
            backgroundColor: window.chartColors.green,
            label: 'Dataset 3'
        },
        ],
        labels: [
            "Test 1",
            "Test 2",
            "Test 3"
        ]
    },
    options: {
        responsive: true,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                stacked: true
            }],
            yAxes: [{
                stacked: true
            }]
        },
        tooltips: {
            enabled: false
        },
        maintainAspectRatio: false
    }
};

var burndownConfig = {
    type: 'line',
    data: {
        labels: ["S", "M", "T", "W", "T", "F", "S"],
        datasets: [{
            label: "Linear interpolation",
            data: [100, 90, 90, 85, 70, 60, 55],
            borderColor: window.chartColors.green,
            backgroundColor: 'rgba(0, 0, 0, 0)',
            fill: false,
            lineTension: 0
        }]
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 100,
                }
            }]
        },
        legend: {
            display: false
        },
        tooltips: {
            enabled: false
        },
        maintainAspectRatio: false
    }
};


window.onload = function() {
    var ctxPie = document.getElementById('pie-chart');
    window.chartPie = new Chart(ctxPie, pieConfig);
    var ctxBar = document.getElementById('bar-chart');
    window.chartBar = new Chart(ctxBar, barConfig);
    var ctxBurndown = document.getElementById('burndown-chart');
    window.chartBurndown = new Chart(ctxBurndown, burndownConfig);
};