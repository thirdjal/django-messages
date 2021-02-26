const moveButtons = document.getElementsByClassName("move-btn");

const readTogglers = document.getElementsByClassName("read-toggler");
const unreadCounters = document.getElementsByClassName(
  "unread-messages-counter"
);
const attachmentDeleteBtn = document.getElementsByClassName(
  "delete-attachment"
);

for (let i = 0; i < moveButtons.length; i++) {
  moveButtons[i].addEventListener("click", function () {
    const messageId = this.dataset.message;
    const action = this.dataset.action;
    console.log("Moving ", messageId, " to ", action);
    updateServer(messageId, action).then((json) => {
      updateMoveButtons(messageId, json["folder"]);
    });
  });
}

for (let i = 0; i < readTogglers.length; i++) {
  readTogglers[i].addEventListener("click", function () {
    const messageId = this.dataset.message;
    const action = this.dataset.action;
    console.log("Marking ", messageId, " as ", action);
    updateServer(messageId, action).then((json) => {
      swapReadTogglers(messageId, json["is_read"]);
    });
  });
}

for (let i = 0; i < attachmentDeleteBtn.length; i++) {
  attachmentDeleteBtn[i].addEventListener("click", function () {
    const attachmentId = this.dataset.attachment;
    console.log("removing", attachmentId);
    removeAttachment(attachmentId);
  });
}

function removeAttachment(attachmentId) {
  console.log("Removing attachment");
  let response = fetch(delete_url, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    credentials: "same-origin",
    body: JSON.stringify({
      attachment_id: attachmentId,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      console.log(json);
      document.getElementById(`attachment-${attachmentId}`).remove();
      return json;
    })
    .then((json) => {
      console.log("updating counter");
      document.getElementById("attachment-counter").innerHTML--;
    });
}

function updateServer(messageId, action) {
  // Invoke the server's API to inform the server of the current user's intention
  console.log("Updating the server for message", messageId, "to", action);
  let response = fetch(update_url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    credentials: "same-origin",
    body: JSON.stringify({
      message_id: messageId,
      action: action,
    }),
  })
    .then((response) => {
      return response.json();
    })

    .then((json) => {
      console.log(json);
      updateUnreadCounters(json["unread_count"]["count"]);
      return json;
    });
  return response;
}

function updateMoveButtons(messageId, folder) {
  const archiveTitle = "Archive this message";
  const deleteTitle = "Delete this message";
  const recoverTitle = "Recover this message";
  const unarchiveTitle = "Move this message to Inbox";

  console.log("Toolbar icons for ", messageId, "to", folder);
  const messageMoveButtons = document.querySelectorAll(
    `.move-btn[data-message="${messageId}"]`
  );
  console.log(messageMoveButtons);
  switch (folder) {
    case 1:
      messageMoveButtons[0].classList.remove("active");
      messageMoveButtons[0].setAttribute("data-action", "archive");
      messageMoveButtons[0].setAttribute("title", archiveTitle);
      messageMoveButtons[0].setAttribute("data-original-title", archiveTitle);
      messageMoveButtons[1].classList.remove("active");
      messageMoveButtons[1].setAttribute("data-action", "delete");
      messageMoveButtons[1].setAttribute("title", deleteTitle);
      messageMoveButtons[1].setAttribute("data-original-title", deleteTitle);
      break;
    case 2:
      messageMoveButtons[0].classList.add("active");
      messageMoveButtons[0].setAttribute("data-action", "unarchive");
      messageMoveButtons[0].setAttribute("title", unarchiveTitle);
      messageMoveButtons[0].setAttribute("data-original-title", unarchiveTitle);

      messageMoveButtons[1].classList.remove("active");
      messageMoveButtons[1].setAttribute("data-action", "delete");
      messageMoveButtons[1].setAttribute("title", deleteTitle);
      messageMoveButtons[1].setAttribute("data-original-title", deleteTitle);
      break;
    case 3:
      messageMoveButtons[0].classList.remove("active");
      messageMoveButtons[0].setAttribute("data-action", "archive");
      messageMoveButtons[0].setAttribute("title", archiveTitle);
      messageMoveButtons[0].setAttribute("data-original-title", archiveTitle);
      messageMoveButtons[1].classList.add("active");
      messageMoveButtons[1].setAttribute("data-action", "recover");
      messageMoveButtons[1].setAttribute("title", recoverTitle);
      messageMoveButtons[1].setAttribute("data-original-title", recoverTitle);
      break;
  }
}

function updateUnreadCounters(count) {
  // Ensure any message unread counters reflect the current number of unread messages
  // based on the number given from the server. In addition, alternatively display or
  // hide those counters when there are no unread messages.
  console.log("Updating unread counters");
  for (let i = 0; i < unreadCounters.length; i++) {
    unreadCounters[i].innerHTML = count;
    if (count <= 0) {
      unreadCounters[i].classList.add("d-none");
    } else {
      unreadCounters[i].classList.remove("d-none");
    }
  }
}

function swapReadTogglers(messageId, isRead) {
  // Alternatively hide and show the 'mark as read' and 'mark-as-unread' elements for
  // a given message, based on the response from the server
  console.log("Updating read status icon to ", isRead);
  const messageTogglers = document.querySelectorAll(
    `.read-toggler[data-message="${messageId}"]`
  );
  if (isRead == true) {
    // TODO: be smarter about how we are selecting the toggler. This is assuming order in the DOM
    messageTogglers[0].classList.add("d-none");
    messageTogglers[1].classList.remove("d-none");
  } else if (isRead == false) {
    messageTogglers[0].classList.remove("d-none");
    messageTogglers[1].classList.add("d-none");
  }
}
