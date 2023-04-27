$(document).ready(function () {
  const ctx = document.getElementById("myChart").getContext("2d");
  const ctx_2 = document.getElementById("myChart_2").getContext("2d");
  const ctx_3 = document.getElementById("H_myChart").getContext("2d");
  const ctx_4 = document.getElementById("H_myChart_2").getContext("2d");

  const myChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [{ label: "Temperature",  },
    ],},
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });

  const myChart_2 = new Chart(ctx_2, {
    type: "line",
    data: {
      datasets: [{ label: "Predicted Temperature",  },
    ],},
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });


  const H_myChart = new Chart(ctx_3, {
    type: "line",
    data: {
      datasets: [{ label: "Humidity",  },
    ],},
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });

  const H_myChart_2 = new Chart(ctx_4, {
    type: "line",
    data: {
      datasets: [{ label: "Predicted Humidity",  },
    ],},
    options: {
      borderWidth: 3,
      borderColor: ['rgba(255, 99, 132, 1)',],
    },
  });

  function addData(Chart, label, data) {
    Chart.data.labels.push(label);
    Chart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    Chart.update();
  }

  function removeFirstData(Chart) {
    Chart.data.labels.splice(0, 1);
    Chart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 10;
  //connect to the socket server.
  //   var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();

  //receive details from server
  socket.on("updateSensorData", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.temp);
    console.log(msg)
    // Show only MAX_DATA_COUNT data
    if (myChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(myChart);
    }
    addData(myChart, msg.date, msg.temp);
  });

  socket.on("P_updateSensorData", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.pred);
    console.log(msg)
    // Show only MAX_DATA_COUNT data
    if (myChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(myChart_2);
    }
    addData(myChart_2, msg.date, msg.pred);
  });

  socket.on("H_updateSensorData", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.hum);
    console.log(msg)
    // Show only MAX_DATA_COUNT data
    if (H_myChart.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(H_myChart);
    }
    addData(H_myChart, msg.date, msg.hum);
  });

  socket.on("PH_updateSensorData", function (msg) {
    console.log("Received sensorData :: " + msg.date + " :: " + msg.hum_pred);
    console.log(msg)
    // Show only MAX_DATA_COUNT data
    if (H_myChart_2.data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(H_myChart_2);
    }
    addData(H_myChart_2, msg.date, msg.hum_pred);
  });
});