/*!
 * Chart.js v2.8.0
 * https://www.chartjs.org
 * (c) 2019 Chart.js Contributors
 * Released under the MIT License
 */
 
var chart = echarts.init(document.getElementById('bar'), 'white', {renderer: 'canvas'});
var old_data = [];
$(
    function () {
        fetchData(chart);
        setInterval(getDynamicData, 2000);
    }
);

function fetchData() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/lineChart",
        dataType: "json",
        success: function (result) {
            chart.setOption(result);
            old_data = chart.getOption().series[0].data;
        }
    });
}

function getDynamicData() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/lineDynamicData",
        dataType: "json",
        success: function (result) {
            old_data.push([result.name, result.value]);
            chart.setOption({
                series: [{data: old_data}]
            });
        }
    });
}