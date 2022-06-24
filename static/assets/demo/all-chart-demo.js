function get_chart(){
    get_top_use_ratio_bucket_BarChart()
    get_model_use_distribution_PieChart()
    get_top_management_unit_BarChart()
}
function get_model_use_distribution_PieChart(){
    let req = new XMLHttpRequest();
    let url = "/get_model_use_distribution";
    req.open("GET", url);
    console.log(req.status);
    req.onload = function() {
        rep = JSON.parse(req.responseText);
        purpose_ls = rep['purpose']
        purpose_percent_ls = rep['purpose_percent']
        var ctx = document.getElementById("model_use_distribution_PieChart");
        var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: purpose_ls,
            datasets: [{
            data: purpose_percent_ls,
            backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
            }],
        },
        });
      
    }
    req.send();
  
}

function get_top_management_unit_BarChart(){
    let req = new XMLHttpRequest();
    let url = "/get_top_management_unit";
    req.open("GET", url);
    console.log(req.status);
    req.onload = function() {
        rep = JSON.parse(req.responseText);
        unit_ls = rep['unit']
        unit_num_ls = rep['unit_num']
        var ctx = document.getElementById("top_management_unit");
        let myLineChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: unit_ls,
            datasets: [{
              label: "The Number of Bucket",
              backgroundColor: "rgba(2,117,216,1)",
              borderColor: "rgba(2,117,216,1)",
              data: unit_num_ls
            }],
          },
          options: {
            scales: {
              xAxes: [{
                time: {
                  unit: 'month'
                },
                gridLines: {
                  display: false
                },
                ticks: {
                  maxTicksLimit: 6
                }
              }],
              yAxes: [{
                ticks: {
                  min: 0,
                  max: 15,
                  maxTicksLimit: 5
                },
                gridLines: {
                  display: true
                }
              }],
            },
            legend: {
              display: false
            }
          }
        });
      
    }
    req.send();
  
  }

function get_top_use_ratio_bucket_BarChart(){
    let req = new XMLHttpRequest();
    let url = "/get_top_use_ratio_bucket";
    req.open("GET", url);
    console.log(req.status);
    req.onload = function() {
        rep = JSON.parse(req.responseText);
        bucket_ls = rep['bucket']
        use_ratio_ls = rep['use_ratio']
        var ctx = document.getElementById("top_use_ratio_bucket_BarChart");
        let myLineChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: bucket_ls,
            datasets: [{
              label: "Use_Ratio",
              backgroundColor: "rgba(2,117,216,1)",
              borderColor: "rgba(2,117,216,1)",
              data: use_ratio_ls
            }],
          },
          options: {
            scales: {
              xAxes: [{
                time: {
                  unit: 'month'
                },
                gridLines: {
                  display: false
                },
                ticks: {
                  maxTicksLimit: 6
                }
              }],
              yAxes: [{
                ticks: {
                  min: 0,
                  max: 100,
                  maxTicksLimit: 5
                },
                gridLines: {
                  display: true
                }
              }],
            },
            legend: {
              display: false
            }
          }
        });
      
    }
    req.send();
  
  }