const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("send");
const chatContainer = document.querySelector(".chat-container");


function returnTimestamp() {
  let currentDate = new Date(); /* Everytime there is a new message input, the currentDate will change */
  const dateDayMonYear = new Intl.DateTimeFormat("en-AU").format(currentDate);
  const dateHourMin = new Intl.DateTimeFormat("en-AU", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(currentDate);
  var dateString = dateDayMonYear + "\xa0\xa0" + dateHourMin;
  return dateString;
}

function restoreHistory() {
  
  // Each loop renders message and bot reply
  for(i = 0; i < prev_msgs.length; i+=2) {

    const message = prev_msgs[i]
    const msg_timestamp = prev_timestamps[i]
    
    const answer = prev_msgs[i+1]
    const answer_timestamp = prev_timestamps[i+1]

    renderMessagePair(message, msg_timestamp, answer, answer_timestamp) 

  }
}

  const bot = "Travelisor Assistant";

// Render query message and response 
function renderMessagePair(message, msg_timestamp, answer, answer_timestamp) {

  /* Creating a new div called messageContainer */
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message-container", "sent"); /* applying the CSS styling to the newly created div */

  /* Creating a new div for the messageHeader which will contain the username and timestamp of message post */
  const messageHeader = document.createElement("div");
  messageHeader.classList.add("message-header"); /* applying the CSS styling to the newly created div */

  /* Create a new div for the username which will be appended inside the message header */
  const usernameDiv = document.createElement("div");
  usernameDiv.classList.add("name"); /* Retrieve the styling for the username */
  usernameDiv.textContent = username; /* Apply the username for the content of the newly created div */

  /* Creating a new div for the timestamp which is adjacent to the username */
  const userTimestamp = document.createElement("div");
  userTimestamp.classList.add("timestamp"); /* Apply styling*/
  userTimestamp.textContent = msg_timestamp;

  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");
  messageDiv.textContent = message;

  const answerContainer = document.createElement("div");
  answerContainer.classList.add("message-container", "receiving");

  const response = document.createElement("div");
  response.classList.add("message");
  response.textContent = answer

  const botHeader = document.createElement("div");
  botHeader.classList.add("message-header");

  const botTimestamp = document.createElement("div");
  botTimestamp.classList.add("timestamp"); /* Apply styling*/
  botTimestamp.textContent = answer_timestamp;

  const botDiv = document.createElement("div");
  botDiv.classList.add("name"); /* Retrieve the styling for the username */
  botDiv.textContent = bot; /* Apply the username for the content of the newly created div */

  chatContainer.appendChild(messageHeader); /* Add the 'messageHeader' div inside the chatContainer div */
  messageHeader.appendChild(usernameDiv); /* Add the 'usernameDiv' inside the messageHeader div */
  messageHeader.appendChild(userTimestamp); /* Add the 'timestamp' div inside the messageHeader div */
  chatContainer.appendChild(messageContainer); /* Add the 'messageContainter' div inside the chatContainer div */
  messageContainer.appendChild(messageDiv); /* Add the 'messageDiv' inside the messageContainer div */

  // Same as the user message just for the bot response
  chatContainer.appendChild(botHeader);
  botHeader.appendChild(botDiv);
  botHeader.appendChild(botTimestamp);
  chatContainer.appendChild(answerContainer);
  answerContainer.appendChild(response);

  messageInput.value = "";
  messageInput.focus();
}

$.ajax({
  url: "/get_countries",
  method: "GET",
  success: function (response) {
    var countries = response.countries;
    var dropdown = $("#country-dropdown");

    // Populate the dropdown with options
    $.each(countries, function (index, country) {
      var option = $("<option>").text(country);
      dropdown.append(option);
    });
  },
  error: function (error) {
    console.log(error);
  },
});
$("#country-dropdown").on("change", function() {
  var placesList = $("#places");
  // Clear existing content whenever a new country is selected
  placesList.empty();
  $.ajax({
    url: "/places",
    method: "GET",
    data: { country: $('#country-dropdown').val() },
    success: function(response) {
      var places = response.places;
      if (places.length > 0) {
        for (var i = 0; i < places.length; i++) {
          var place = places[i];
          var listItem = $("<li>").text(place);
          placesList.append(listItem);
        }
      } else {
        var foundNoPlaces = $("<li>").text("No places found.");
        placesList.append(foundNoPlaces);
      }
    },
    error: function(error) {
      console.log(error);
    }
  });
});

sendBtn.addEventListener("click", (event) => {
  event.preventDefault(); /*Prevent form from being normally submitted, thus stopping refresh everytime you click the button*/
  const message = messageInput.value.trim();
  if (message) {
    console.log(event);
    console.log(message);

    const answerContainer = document.createElement("div");
    answerContainer.classList.add("message-container", "receiving");

    const response = document.createElement("div");
    response.classList.add("message");

    const botHeader = document.createElement("div");
    botHeader.classList.add("message-header");

    const botTimestamp = document.createElement("div");
    botTimestamp.classList.add("timestamp"); /* Apply styling*/
    botTimestamp.textContent = returnTimestamp();

    const botDiv = document.createElement("div");
    botDiv.classList.add("name"); /* Retrieve the styling for the username */
    botDiv.textContent = bot; /* Apply the username for the content of the newly created div */

    var i = 0;
    var speed = 10;
    let answer = "";
    const $inputButton = $('#send'); /* send button */

    // Define timestamp earlier so it can be included in ajax request
    const timestamp = returnTimestamp()

      // AJAX GET REQUEST TO OBTAIN THE RESPONSE
    $.ajax({
      url: "",
      type: "get",
      contentType: "application/json",
      data: {
        msg: message,
        timestamp: timestamp
      },
      beforeSend: function () {
        $inputButton.prop("disabled", true);
      },
      success: reply
    })

    // Success function for ajax request:
    //    Gets reply from the server and types it as the bot assistant
    function reply(response) {
      if (message.length > 1) {
        answer = response.reply
        console.log(answer);
      } else {
        answer = "Sorry, but I cannot understand your question. Feel free to send another";
        console.log(answer);
      }
      typing();
    }

    function typing() {
      $inputButton.prop('disabled', true); /* Disable the button once the typing function has been called */
      if (i < answer.length) {
        response.textContent += answer[i];
        chatContainer.scrollTop = chatContainer.scrollHeight;
        i++;
        setTimeout(typing, speed);
        console.log("typing is working");
      } else {
        $inputButton.prop('disabled', false);  /* Enable the button once characters displayed is no longer under the answer length (hence, finished typing)*/
      }
    } 

    //renderMessagePair(message, timestamp, answer, timestamp)
        /* Creating a new div called messageContainer */
        const messageContainer = document.createElement("div");
        messageContainer.classList.add("message-container", "sent"); /* applying the CSS styling to the newly created div */
    
        /* Creating a new div for the messageHeader which will contain the username and timestamp of message post */
        const messageHeader = document.createElement("div");
        messageHeader.classList.add("message-header"); /* applying the CSS styling to the newly created div */
    
        /* Create a new div for the username which will be appended inside the message header */
        const usernameDiv = document.createElement("div");
        usernameDiv.classList.add("name"); /* Retrieve the styling for the username */
        usernameDiv.textContent = username; /* Apply the username for the content of the newly created div */
    
        /* Creating a new div for the timestamp which is adjacent to the username */
        const userTimestamp = document.createElement("div");
        userTimestamp.classList.add("timestamp"); /* Apply styling*/
        userTimestamp.textContent = timestamp;
    
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message");
        messageDiv.textContent = message;
    
        chatContainer.appendChild(messageHeader); /* Add the 'messageHeader' div inside the chatContainer div */
        messageHeader.appendChild(usernameDiv); /* Add the 'usernameDiv' inside the messageHeader div */
        messageHeader.appendChild(userTimestamp); /* Add the 'timestamp' div inside the messageHeader div */
        chatContainer.appendChild(messageContainer); /* Add the 'messageContainter' div inside the chatContainer div */
        messageContainer.appendChild(messageDiv); /* Add the 'messageDiv' inside the messageContainer div */
    
        // Same as the user message just for the bot response
        chatContainer.appendChild(botHeader);
        botHeader.appendChild(botDiv);
        botHeader.appendChild(botTimestamp);
        chatContainer.appendChild(answerContainer);
        answerContainer.appendChild(response);
        
        messageInput.value = "";
        messageInput.focus();
  }
});

// Allows the enter key to act as a click so the user doesn't have to always manually click the send button
messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendBtn.click();
  }
});

const startChatBtn = document.getElementById("start-new-btn");
const taskbarContainer = document.querySelector(".recent-chats");

// For the sidebar, when you click on a the link button, will put the focus CSS on that parent div until you click another link
// Ensures that the user understands which conversation they are typing in
function applyStyling() {
  $(".link-btn-class").on("click", function () {
    // Remove focus from any previously focused item
    $(".new-chat").removeClass("focus");
    // Add focus to the clicked item
    $(this).closest(".new-chat").addClass("focus");
  });

  // Renaming chat, double click the text and will allow the user to change the name
  $(".chat-name").on("dblclick", function (e) {
    e.preventDefault();
    // Store the previous name in a data attribute
    var previousName = $(this).text().trim();
    $(this).data("previousName", previousName); /* Store the name before the editing process */
    $(this).attr("contenteditable", "true");
    $(this).addClass("editing");
    $(this).focus();
  });

  // Set the max character length so it doesn't overflow, used the class editing to know if the user is in the current process of changing the name
  $(".chat-name").on("keydown", function (event) {
    if ($(this).hasClass("editing")) {
      var newName = $(this).text().trim();
      var maxLength = 27;
      // If the name is over or equal to the max character limit, then prevent anymore text from being applied. Although
      // allow the use of the backspace and delete keys
      if (newName.length >= maxLength && event.keyCode !== 8 && event.keyCode !== 46) {
        event.preventDefault();
        return;
      }
    }
    // If the user clicks the Enter key when editing the name it will save the new name if there is some amount of characters
    // If the field is empty when the user clicks empty, it'll will restore the previous name to prevent creating empty fields
    if (event.key === "Enter") {
      event.preventDefault();
      var newName = $(this).text().trim();
      if (newName !== "") {
        $(this).attr("contenteditable", "false").blur();
      } else {
        // Get the previous name from the data attribute and set it back
        var previousName = $(this).data("previousName");
        $(this).text(previousName);
        $(this).attr("contenteditable", "false").blur();
      }
    }
  });

  // If the user clicks out of the changable text state, then the name will either save if there is some amount of characters or
  // restore back to the previous name
  $(".chat-name").on("focusout", function () {
    var newName = $(this).text().trim();
    if (newName === "") {
      // Get the previous name from the data attribute and set it back
      var previousName = $(this).data("previousName");
      $(this).text(previousName);
    }
    $(this).attr("contenteditable", "false").removeClass("focus");
  });
}

startChatBtn.addEventListener("click", (event) => {
  event.preventDefault();
  console.log(event);

  var chatName = "Double click to rename";

  const list = document.createElement("ul");
  list.classList.add("chat-list");

  const newChat = document.createElement("li");
  newChat.classList.add("new-chat");

  const chatSpanName = document.createElement("span");
  chatSpanName.classList.add("chat-name");
  chatSpanName.textContent = chatName;

  const chatLink = document.createElement("a");
  chatLink.classList.add("link-btn-class");

  const deleteBtn = document.createElement("button");
  deleteBtn.classList.add("delete-chat-class");

  // Delete the parent div when the user clicks on the delete icon
  deleteBtn.addEventListener("click", () => {
    const parent = event.target.parentNode;
    // to avoid an error, first check if newChat exists
    if (parent) {
      // Remove any of the margins and padding that was left behind to ensure that a newly created
      // chat doesn't add to the space between
      newChat.style.margin = "0";
      newChat.style.padding = "0";
      newChat.parentElement.style.margin = "0";
      newChat.parentElement.style.padding = "0";
      newChat.remove();
    }
  });

  taskbarContainer.appendChild(list);
  list.appendChild(newChat);
  newChat.appendChild(chatSpanName);
  newChat.appendChild(chatLink);
  newChat.appendChild(deleteBtn);
  applyStyling();
});

// Obtain the menu (hamburger) icon and the sidebar
const menuToggle = document.getElementById("sidebar-toggle");
const sidebar = document.querySelector(".taskbar");

// When the icon is clicked, enable the active CSS class selector
menuToggle.addEventListener("click", () => {
  sidebar.classList.toggle("is-active");
});

// Only run history restoration if history exists
if (prev_msgs.length > 0) {
  console.log("Restoring history...")
  restoreHistory()
}
