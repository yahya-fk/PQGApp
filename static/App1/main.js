function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    if (sidebar.style.width === "250px") {
        sidebar.style.width = "0px";
    } else {
        sidebar.style.width = "250px";
    }
}
const modeToggle = document.getElementById('mode-toggle');
const body = document.body;

function toggleMode() {
    body.classList.toggle('light-mode');
}
modeToggle.addEventListener('click', toggleMode);
function toggleLoadingOverlay(show) {
  if (show) {
    document.getElementById("loading").style.display = 'flex';
  } else {
    document.getElementById("loading").style.display = 'none';
  }
  }



function spinActivated(){
  toggleLoadingOverlay(true);}

  document.addEventListener("DOMContentLoaded", spinActivated());

function createBarChartWithParams1(ctx, labels, data, targetValue) {
    const chartData = {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: ['#006EA6'],
        borderColor: ['WHITE'],
        borderWidth: 1,
        label: 'PQG Efficiency',
      }]
    };

    const chartOptions = {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
            suggestedMax: 100
          }
        }]
      },
      legend: {
        display: false,
      },
      plugins: {
        annotation: {
                annotations: [
                    {
                        type: 'line',
                        mode: 'horizontal',
                        scaleID: 'y',
                        value: targetValue,
                        borderColor: 'green',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        label: {
                            color:"green",
                            backgroundColor: 'rgba(0, 255, 0, 0)', 
                            enabled: true,
                            content: 'Objective ('+targetValue+'%)', 
                            position: 'left',
                        },
                    },
                ],
            },
      },
    };

    const myChart = new Chart(ctx, {
      type: 'bar',
      data: chartData,
      options: chartOptions,
    });
  }




  function createBarChartWithParams(ctx, labels, datasets, targetValue) {
    const backgroundColors = ['rgba(0, 0, 255)', 'rgba(0, 255, 0)', 'rgba(255, 0, 0)', 'rgba(75, 192, 192)'];
    const borderColors = ['rgba(0, 0, 255, 1)', 'rgba(0, 255, 0, 1)', 'rgba(255, 0, 0, 1)', 'rgba(75, 192, 192, 1)'];

    const chartData = {
      labels: labels,
      datasets: datasets.map((dataset, index) => {
        return {
          ...dataset,
          backgroundColor: backgroundColors[index],
          borderColor: borderColors[index],
          borderWidth: 1
        };
      }),
    };

    const chartOptions = {
      plugins: {
        legend: {
          display: true,
        },
      },
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true,
          ticks: {
            stepSize: 10,
          },
        },
      },
      plugins: {
        annotation: {
          annotations: [
            {
              type: 'line',
              mode: 'horizontal',
              scaleID: 'y',
              value: targetValue,
              borderColor: 'green',
              borderWidth: 2,
              borderDash: [5, 5],
              label: {
                enabled: true,
                content: 'Objective (' + targetValue + '%)',
                position: 'top',
              },
            },
          ],
        },
      },
    };

    const config = {
      type: 'bar',
      data: chartData,
      options: chartOptions,
    };

    new Chart(ctx, config);
  }


