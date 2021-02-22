/*!
 * Chart.js v2.8.0
 * https://www.chartjs.org
 * (c) 2019 Chart.js Contributors
 * Released under the MIT License
 */
var spo = document.getElementById("hit-rate-doughnut");

var myChart = new Chart(spo, {
  type: 'doughnut',
  data: {
    labels:["Remain","Completed"],
    datasets: [{
      label:"Favourite",
      backgroundColor:["#28D094","#FF4961"],
      data: [18, 82],
    }]
  },
  options:{
    responsive:!0,title:{
        display:!1
        },legend:{
            display:!1
        },layout:{
            padding:{
                left:16,right:16,top:16,bottom:16
            }
        },cutoutPercentage:92,animation:{animateScale:!1,duration:2500
        }
    }

});

var blo = document.getElementById("deals-doughnut");

var myChart = new Chart(blo, {
  type: 'doughnut',
  data:{
    labels:["Remain","Completed"],
    color:"#fff",
    datasets:[{
        label:"Favourite",
        borderWidth:0,
        backgroundColor:["#ff7b8c","#FFF"],
        data:[24,80]
    }]
  },
  options:{
    responsive:!0,title:{
        display:!1
    },
    legend:{
        display:!1
    },
    elements:{},
    layout:{
        padding:{
            left:16,right:16,top:16,bottom:16
        }
    },
    cutoutPercentage:94,
    animation:{
        animateScale:!1,duration:5e3
    }
  }

});