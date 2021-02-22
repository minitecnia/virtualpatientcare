/*!
 * Chart.js v2.8.0
 * https://www.chartjs.org
 * (c) 2019 Chart.js Contributors
 * Released under the MIT License
 */
/*var dataset = [10, 59, 40, 20, 20, 55, 40];*/

var speedCanvas = document.getElementById("myECGChart");

    Chart.defaults.global.defaultFontFamily = "Lato";
    Chart.defaults.global.defaultFontSize = 18;

var speedData = {
    /*labels: ["0s", "10s", "20s", "30s", "40s", "50s", "60s"],*/
    labels: tiempo,
    datasets: [{
        /*label: "ECG",*/
        data: dataset,
        /*data: [{% for item in y %}
            {{ item}},
        {% endfor %*/
    }]
};

var chartOptions = {
    legend: {
        display: false,
        position: 'top',
        labels: {
            boxWidth: 40,
            fontColor: 'black'
        }
    }
};

var lineChart = new Chart(speedCanvas, {
    type: 'line',
    data: speedData,
    options: chartOptions
});