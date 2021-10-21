//get access to the expense summary chart for past-one-month
const myChart_title = document.getElementById('myChart_title');
const myChart = document.getElementById('myChart');

//get access to the expense summary chart for past-six-month
const myChart2_title = document.getElementById('myChart2_title');
const myChart2 = document.getElementById('myChart2');

//get access to the expense summary chart for past-twelve-month
const myChart3_title = document.getElementById('myChart3_title');
const myChart3 = document.getElementById('myChart3');

//hide past 1 month, past 6 month and past 12 month expenses chart summary by default
myChart_title.style.display = 'none';
myChart.style.display = 'none';

myChart2_title.style.display = 'none';
myChart2.style.display = 'none';

myChart3_title.style.display = 'none';
myChart3.style.display = 'none';

//button to show the expense summary chart for past-one-month
document.getElementById("pastOneMonth").addEventListener("click", function() {
  // document.getElementById("myChart").innerHTML = "Hello World";
  myChart_title.style.display = 'block';
  myChart.style.display = 'block'; //past 1 month expense chart summary

  myChart2_title.style.display = 'none';
  myChart2.style.display = 'none'; //past 6 month expense chart summary

  myChart3_title.style.display = 'none';
  myChart3.style.display = 'none'; //past 12 month expense chart summary
});

//button to show the expense summary chart for past-six-months
document.getElementById("pastSixMonths").addEventListener("click", function() {
  // document.getElementById("myChart").innerHTML = "Hello World";
  myChart_title.style.display = 'none';
  myChart.style.display = 'none';   //past 1 month expense chart summary

  myChart2_title.style.display = 'block';
  myChart2.style.display = 'block'; //past 6 month expense chart summary

  myChart3_title.style.display = 'none';
  myChart3.style.display = 'none';  //past 12 month expense chart summary
});

//button to show the expense summary chart for past-twelve-months
document.getElementById("pastTwelveMonths").addEventListener("click", function() {
  // document.getElementById("myChart").innerHTML = "Hello World";
  myChart_title.style.display = 'none';
  myChart.style.display = 'none'; //past 1 month expense chart summary

  myChart2_title.style.display = 'none';
  myChart2.style.display = 'none'; //past 6 month expense chart summary

  myChart3_title.style.display = 'block';
  myChart3.style.display = 'block'; //past 12 month expense chart summary
});
