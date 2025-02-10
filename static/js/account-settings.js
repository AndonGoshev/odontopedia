function showNotification(message) {
    var notification = document.getElementById("notification");
    notification.textContent = message;
    notification.style.display = "block";
    setTimeout(function () {
        notification.style.display = "none";
    }, 2000);
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

function editField(field) {
    document.getElementById(field + '_display_container').style.display = 'none';
    document.getElementById(field + '_edit').style.display = 'block';
}

function cancelEdit(field) {
    document.getElementById(field + '_edit').style.display = 'none';
    document.getElementById(field + '_display_container').style.display = 'block';
    // For text fields, reset input to current display value
    if (field !== 'profile_image') {
        document.getElementById(field + '_input').value = document.getElementById(field + '_display').textContent;
    } else {
        // For file inputs, simply clear the value
        document.getElementById(field + '_input').value = "";
    }
}

function saveField(field) {
    let newValue;
    if (field === 'profile_image') {
        let fileInput = document.getElementById(field + '_input');
        if (fileInput.files && fileInput.files[0]) {
            newValue = fileInput.files[0];
        } else {
            alert("No file selected.");
            return;
        }
    } else {
        newValue = document.getElementById(field + '_input').value;
    }
    updateFieldCustom(field, newValue);
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
                } else {
                    document.getElementById(field + '_display').textContent = newValue;
                }
                cancelEdit(field);
            } else if (data.error) {
                showNotification("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));
}
