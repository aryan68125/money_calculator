//this javascript file will detect when the user starts typing in the from field of the register page
console.log('register javascript working');
const usernameField = document.querySelector('#usernameField'); //select the input field by id from our register.html form

//get the feedback field from the front end register.html form
const feedbackArea = document.querySelector('.invalid_feedback'); //select via class

//get the email field from the frontend register.html form
const emailField = document.querySelector('#emailField'); //select via id

//declare emailFeedbackArea here
const emailFeedbackArea = document.querySelector('.emailFeedBackArea');

//get the passwordField via id
const passwordField = document.querySelector('#passwordField'); //get the password class input field via id

//get the passwordField2 via id
const passwordField2 = document.querySelector('#passwordField2'); //get the password2 class input field via id

//now get password show toggle field via class
const showPasswordToggle = document.querySelector('.showPasswordToggle');

//now get the submit button via class
const submitbtn = document.querySelector('.submit-btn');

//add event listener to the password field in the register.html form inorder to show ow hide password using show toggle
showPasswordToggle.addEventListener('click', (e) => {
  //now here we want to change SHOW to HIDE when the user clicks on it
  if(showPasswordToggle.textContent ==='SHOW')
  {
    //if true then set showPasswordToggle.textContent to HIDE
    showPasswordToggle.textContent = 'HIDE';

    //update the passsword with the actual password text and replace the **** that hides the password
    passwordField.setAttribute('type','text');
  }
  else
  {
    //if false then set showPasswordToggle.textContent to SHOW
    showPasswordToggle.textContent = 'SHOW';
    //update the passsword with the actual password text and replace the password with **** that hides the password
    passwordField.setAttribute('type','password');
  }
});

//checking if password and password2 is matching or not
var check = function() {
  if (document.getElementById('passwordField').value !=
    document.getElementById('passwordField2').value) {

      document.getElementById('message').style.color = '#8a1253';
      document.getElementById('message').innerHTML = 'not matching';

      //disable the submit button if the email address entered by the user is not valid
      submitbtn.setAttribute('disabled', 'disabled');
      submitbtn.disabled=true;

  } else {

    document.getElementById('message').style.color = '#9fd3c7';
    document.getElementById('message').innerHTML = 'matching';

    //enable the submit button if the email address entered by the user is valid
    submitbtn.removeAttribute('disabled');
  }
}

//add an eventListener to emailField
emailField.addEventListener('keyup', (e) => {

  console.log('1111',1111); //for debugging purposes
  //now here we need to pick out what the user is typing in the frontend in register.html form
  const emailVal = e.target.value;
  console.log('emailVal',emailVal); //log what the user is typing on the console of the web browser

  //before we make an api call here we need to set them to remove is-invalid class
  emailField.classList.remove('is-invalid') //is-invalid is a bootstrap class that will get added if the data.username_error is True
  //by default feedbackArea display is set to none so here we need to display feedbackArea to block to actually make it visible to user in the front-end register.html
  emailFeedbackArea.style.display = 'none';

  //check if the username is empty or not
  if(emailVal.length>0){
            //now here we can use our api call to validate the username in register.html form
            //it allows you to do things that you did in the Postman
            //fetch('url') url will be a dynamic url sincs i am already in the application i.e this javascript is running on the same server
            //sincs it is going to be a post request we are going to specify the things we are going to send to the (front-end)
            fetch('/authentication/validate-email/',{
              //we are required to send a body to the frontend and a body requires a key and a value
              //manually String a file when using fetch
              body: JSON.stringify({email: emailVal}),
              method:'POST' ,
            }).then(res => res.json()).then(data => {
                console.log('data', data);
                if(data.email_error)
                {
                  //disable the submit button if the email address entered by the user is not valid
                  submitbtn.setAttribute('disabled', 'disabled');
                  submitbtn.disabled=true;

                  emailField.classList.add('is-invalid') //is-invalid is a bootstrap class that will get added if the data.username_error is True
                  //by default feedbackArea display is set to none so here we need to display feedbackArea to block to actually make it visible to user in the front-end register.html
                  emailFeedbackArea.style.display = 'block';
                  emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`
                }
                else {
                  //enable the submit button if the email address entered by the user is valid
                  submitbtn.removeAttribute('disabled');
                }
            });   //map the response with json
  }

});

//add an eventListener to usernameField
usernameField.addEventListener('keyup', (e) => { //(e) it is an anonymous function which is going to return an event e
  console.log('777777',777777); //for debugging purposes
  //now here we need to pick out what the user is typing in the frontend in register.html form
  const usernameVal = e.target.value;
  console.log('usernameVal',usernameVal); //log what the user is typing on the console of the web browser

  //before we make an api call here we need to set them to remove is-invalid class
  usernameField.classList.remove('is-invalid') //is-invalid is a bootstrap class that will get added if the data.username_error is True
  //by default feedbackArea display is set to none so here we need to display feedbackArea to block to actually make it visible to user in the front-end register.html
  feedbackArea.style.display = 'none';

  //check if the username is empty or not
  if(usernameVal.length>0){
            //now here we can use our api call to validate the username in register.html form
            //it allows you to do things that you did in the Postman
            //fetch('url') url will be a dynamic url sincs i am already in the application i.e this javascript is running on the same server
            //sincs it is going to be a post request we are going to specify the things we are going to send to the (front-end)
            fetch('/authentication/validate-username/',{
              //we are required to send a body to the frontend and a body requires a key and a value
              //manually String a file when using fetch
              body: JSON.stringify({username: usernameVal}),
              method:'POST' ,
            }).then(res => res.json()).then(data => {
                console.log('data', data);
                if(data.username_error)
                {
                  //disable the submit button if the email address entered by the user is not valid
                  submitbtn.setAttribute('disabled', 'disabled');
                  submitbtn.disabled=true;

                  usernameField.classList.add('is-invalid') //is-invalid is a bootstrap class that will get added if the data.username_error is True
                  //by default feedbackArea display is set to none so here we need to display feedbackArea to block to actually make it visible to user in the front-end register.html
                  feedbackArea.style.display = 'block';
                  feedbackArea.innerHTML = `<p>${data.username_error}</p>`
                }
                else {
                  //enable the submit button if the email address entered by the user is valid
                  submitbtn.removeAttribute('disabled');
                }
            });   //map the response with json
  }
}); //keyup is fired everytime when the user type anything on this username field
