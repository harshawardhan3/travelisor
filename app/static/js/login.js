// Obtaining variable values by retrieving the input data from the id's
const usernameEmail = document.getElementById("username-email");
const password = document.getElementById("password");
const button = document.getElementById("login-button");
const errorElement = document.getElementById("error");


// Run event function once the button is clicked. Button type is "submit"
// Console logs to check whether the arguments are performing as intended
button.addEventListener("click", (e) => {
  // Creates the array of error messages
  let messages = [];

  if (usernameEmail.value.includes("@")) {
    console.log("Email has been provided");
  } else if (usernameEmail.value === '' || usernameEmail.value == null) {
      messages.push("Username/Email is required");
      console.log("Neither email or username provided");
  }
  
  // Checking if the input text field for email is empty
  if (password.value === "" || password.value == null) {
    messages.push("Password is required");
    console.log("Password not provided");
    // Checking if the length is above 6 or below 20
  } else if (password.value.length > 6 && password.value.length < 20) {
    console.log("Password is valid");
    // Checking if the password length is below or equal to 6 characters
  } else if (password.value.length <= 6) {
    messages.push("Password must be greater than 6 characters");
    console.log("Password is not valid: Under 6 characters");
    // Checking if length is above or equal to 20 characters
  } else if (password.value.length >= 20) {
    messages.push("Password must be less than 20 characters");
    console.log("Password is not valid: More then 20 characters");
  }

    // Only display error message if the array is not empty
  // Only display the first message in the array
  if (messages.length > 0) {
    // Prevent the submission of the form which is the usual action once a submit button is toggled
    // Instead display the error message if the inputs don't meet the requirements
    e.preventDefault();
    errorElement.innerText = messages[0];
  }

});