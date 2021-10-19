const searchField = document.getElementById('searchField');

//get access to the default-table
const tableDefault = document.querySelector('.default-table');

//get pagination via class
const paginationContainer = document.querySelector('.pagination-container');

//search the table-output via class
const tableOutput = document.querySelector('.table-output');

const tableOutputBody = document.querySelector('.table-body');

const noResult = document.querySelector('.noResult');

//tableOutput hide the output table by default
tableOutput.style.display = 'none';

//detect when the user is typing so in order to that we will use an EventListener with a 'keyup'
searchField.addEventListener('keyup' , (e) =>{
  //now here we will pick out what the user is searching for
  const searchValue = e.target.value;
  //trim() will remove the white spaces that the user will send in whjen searching for the expenses in the searchField
  if(searchValue.trim().length>0){
    console.log('searchValue',searchValue);
    //hide pagination if the result are there
    paginationContainer.style.display = 'none';

    //clear out previous search results from the tableOutput's tableOutputBody
    tableOutputBody.innerHTML = "";

    //now here we need to make a request using fetch api
    //now here we can use our api call to validate the username in register.html form
    //it allows you to do things that you did in the Postman
    //fetch('url') url will be a dynamic url sincs i am already in the application i.e this javascript is running on the same server
    //sincs it is going to be a post request we are going to specify the things we are going to send to the (front-end)
    fetch('/income/search-income',{
      //we are required to send a body to the frontend and a body requires a key and a value
      //manually String a file when using fetch
      body: JSON.stringify({searchText: searchValue}),
      method:'POST' ,
    }).then(res => res.json()).then(data => {
        console.log('data',data);

        //once we get the results we will hide the normal table in index.html and show the output table used by our search functionality tableOutput
        tableOutput.style.display = 'block';
        //tableDefault hide the output table by default
        tableDefault.style.display = 'none';

        //show default table if the search result is empty
        if (data.length===0)
        {
          noResult.style.display = 'block';
          //once we get the results we will hide the normal table in index.html and show the output table used by our search functionality tableOutput
          tableOutput.style.display = 'none';
        }
        else{
          data.forEach((item)=>{
            noResult.style.display = 'none';
            //append some rows to the table body in the tableOutput table
            tableOutputBody.innerHTML +=
            `
               <tr>
               <td>${item.amount}</td>
               <td>${item.source}</td>
               <td>${item.description}</td>
               <td>${item.date}</td>
               </tr>
            `;
          });
        }
    });   //map the response with json

  }
  else{
    //cear out htis field once the search is complete
    tableOutput.style.display = 'none';
    //tableDefault show the output table by default
    tableDefault.style.display = 'block';
    //show pagination if the result are there
    paginationContainer.style.display = 'block';
  }
})
