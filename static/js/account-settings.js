function editField(field) {
    let input = document.getElementById(field + '_input');
    let editBtn = document.getElementById(field + '_edit_btn');
    let saveBtn = document.getElementById(field + '_save_btn');
    let cancelBtn = document.getElementById(field + '_cancel_btn');

    // Store original value for potential cancellation
    input.setAttribute('data-original-value', input.value);

    input.removeAttribute("readonly");
    input.focus();

    editBtn.style.display = "none";
    saveBtn.style.display = "inline";
    cancelBtn.style.display = "inline";
}

function cancelEdit(field) {
    let input = document.getElementById(field + '_input');
    let editBtn = document.getElementById(field + '_edit_btn');
    let saveBtn = document.getElementById(field + '_save_btn');
    let cancelBtn = document.getElementById(field + '_cancel_btn');

    // Revert to original value
    input.value = input.getAttribute('data-original-value');
    input.setAttribute("readonly", true);

    // Show only the edit button
    editBtn.style.display = "inline";
    saveBtn.style.display = "none";
    cancelBtn.style.display = "none";
}

function saveField(field) {
    let editBtn = document.getElementById(field + '_edit_btn');
    let saveBtn = document.getElementById(field + '_save_btn');
    let cancelBtn = document.getElementById(field + '_cancel_btn');
    let input = document.getElementById(field + '_input');
    let newValue = input.value;
    updateFieldCustom(field, newValue);

    editBtn.style.display = "inline";
    saveBtn.style.display = "none";
    cancelBtn.style.display = "none";
        input.setAttribute("readonly", true);
}

function toggleProfileImageEdit() {
    // Toggle the visibility of the file input controls
    let editDiv = document.getElementById("profile_image_edit");
    editDiv.style.display = (editDiv.style.display === "none") ? "block" : "none";
}

function cancelProfileImageEdit() {
    // Hide the edit controls and clear the file input
    document.getElementById("profile_image_edit").style.display = "none";
    document.getElementById("profile_image_input").value = "";
}

function updateFieldCustom(field, newValue) {
    let formData = new FormData();
    formData.append("field", field);

    if (field === "profile_image") {
        let fileInput = document.getElementById(field + '_input');
        if (fileInput.files && fileInput.files[0]) {
            formData.append("profile_image", fileInput.files[0]);
        } else {
            alert("No file selected.");
            return;
        }
    } else {
        formData.append("value", newValue);
    }

    // Debug: Log FormData contents
    console.log("Updating field:", field);
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    fetch(accountSettingsUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showNotification(data.message);
            if (field === "profile_image" && data.value) {
                document.getElementById("profile_image_display").src = data.value;
                // Use the dedicated function for profile image so that the image stays displayed
                cancelProfileImageEdit();
            } else {
                document.getElementById(field + '_display').textContent = newValue;
                cancelEdit(field);
            }
        } else if (data.error) {
            showNotification("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

function showNotification(message) {
    var notification = document.getElementById("notification");
    notification.textContent = message;
    notification.style.display = "block";
    setTimeout(function () {
        notification.style.display = "none";
    }, 2000);
}
