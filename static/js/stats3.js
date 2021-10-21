//create a function that will be rendering the chart
const renderChart_past_twelve_months = (data ,labels)=>{

  //logic related to rendering the chart
  var ctx = document.getElementById('myChart3').getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'pie', //type of chart that we want to display
      data: {
        //['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
          labels: labels, //labels of the data what we are showing Dynamically supplied by the function
          datasets: [{
            //I can passin a label for a dataset
            //lets sat I want to compare expenses and income so I am going to have an array for each of the configurations for each of the data
              label: 'Last twelve month Expenses',
              //[12, 19, 3, 5, 2, 3] is the data which is gonna be dynamic
              //now I am going to create a function that will be rendering this chart
              data: data, //data of the data what we are showing Dynamically supplied by the function
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(139,0,0, 0.5)',
                  'rgba(255,140,0, 0.5)',
                  'rgba(154,205,50, 0.5)',
                  'rgba(47,79,79, 0.5)',
                  'rgba(25,25,112, 0.5)',
                  'rgba(138,43,226, 0.5)',
                  'rgba(139,0,139, 0.5)',
                  'rgba(139,69,19, 0.5)',
                  'rgba(112,128,144, 0.5)',
                  'rgba(0,206,209, 0.5)',
                  'rgba(46,139,87, 0.5)',
                  'rgba(128,128,0, 0.5)',
                  'rgba(0,255,0, 0.5)',
                  'rgba(189,183,107, 0.5)',
                  'rgba(70,130,180, 0.5)',
                  'rgba(100,149,237, 0.5)',
                  'rgba(0,191,255, 0.5)',
                  'rgba(30,144,255, 0.5)',
                  'rgba(106,90,205, 0.5)',
                  'rgba( 216,191,216, 0.5)',
                  'rgba(199,21,133, 0.5)',
                  'rgb(51, 71, 86,0.5)',
                  'rgb(63, 7, 19, 0.5)',
                  'rgb(74, 64, 58, 0.54)',
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(128,0,0,1)',
                  'rgba(255,140,0, 1)',
                  'rgba(154,205,50, 1)',
                  'rgba(47,79,79, 1)',
                  'rgba(25,25,112, 1)',
                  'rgba(138,43,226, 1)',
                  'rgba(139,0,139, 1)',
                  'rgba(139,69,19, 1)',
                  'rgba(112,128,144, 1)',
                  'rgba(0,206,209, 1)',
                  'rgba(46,139,87, 1)',
                  'rgba(128,128,0, 1)',
                  'rgba(0,255,0, 1)',
                  'rgba(189,183,107, 1)',
                  'rgba(70,130,180, 1)',
                  'rgba(100,149,237, 1)',
                  'rgba(0,191,255, 1)',
                  'rgba(30,144,255, 1)',
                  'rgba(106,90,205, 1)',
                  'rgba(216,191,216, 1)',
                  'rgba(199,21,133, 1)',
                  'rgb(51, 71, 86, 1)',
                  'rgb(63, 7, 19, 1)',
                  'rgb(74, 64, 58, 1)',
              ],
              borderWidth: 1
          }]
      },
      options: {
          title: {
            display:true,
            text: 'Expenses per category',
          }
      }
  }); //logic for creating a chart

};

//calling renderChart function that will render our charts in the fronend in the expense summary page
//add a listener for when the expense summary page is loaded
const getChartData3 = ()=>{
  console.log('get past 12 month summary');
  //here we will make an api call that will return for us the data and render the chart
  //for us to do an api call we will use fetch. fetch takes in the url
  fetch('/summary_past_twelve_months')
    .then((res) => res.json())
    .then((results) => {
      console.log('past 12 month summary results',results);

      //getting the data from json response from the backend
      const category_data = results.expense_catagory_data;
      //labels are the keys and values are the expenses amount
      const [labels,data]=[Object.keys(category_data), Object.values(category_data)];

      //now call this renderChart function to render the chart it takes in two arrays or a list [], []
      //data and labels are both lists
      renderChart_past_twelve_months(data,labels);
    });
};
document.onload = getChartData3();
