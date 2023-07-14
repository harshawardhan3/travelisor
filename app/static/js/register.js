// Obtaining variable values by retrieving the input data from the id's
const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const button = document.getElementById("register-button");
const errorElement = document.getElementById("error");
const firstName = document.getElementById("first-name");
const lastName = document.getElementById("last-name");

// Run event function once the button is clicked. Button type is "submit"
// Console logs to check whether the arguments are performing as intended
button.addEventListener("click", (e) => {
  // Creates the array of error messages
  let messages = [];
  if (firstName.value === "" || firstName.value == null) {
    messages.push("First Name is required");
    console.log("firstName not provided");
  }
  if (lastName.value === "" || lastName.value == null) {
    messages.push("Last Name is required");
    console.log("lastName not provided");
  }

  if (username.value === "" || username.value == null) {
    messages.push("Username is required");
    console.log("Username not provided");
    // Checking if the length is above 5 or below 15
  } else if (username.value.length > 5 && username.value.length < 15) {
    console.log("Username is valid");
    // Checking if the Username length is below or equal to 5 characters
  } else if (username.value.length <= 5) {
    messages.push("Username must be greater than 5 characters");
    console.log("Username is not valid: Under 5 characters");
    // Checking if length is above or equal to 15 characters
  } else if (username.value.length >= 15) {
    messages.push("Username must be less than 15 characters");
    console.log("Username is not valid: More then 15 characters");
  }
  // Checking if the input text field for email is empty
  if (email.value === "" || email.value == null) {
    messages.push("E-mail is required");
    console.log("E-mail not provided");
    // Checking if the email entry is not empty and that it includes the @ symbol
  } else if (email.value !== "" && email.value.includes("@")) {
    console.log("E-mail is valid");
  } else {
    messages.push("E-mail requires @ symbol");
    console.log("E-mail is not valid: Missing @ symbol");
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
