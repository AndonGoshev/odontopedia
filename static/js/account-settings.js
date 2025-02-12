function updateCharCount() {
    let textarea = document.getElementById("bio_input");
    let counter = document.getElementById("char_count");
    let saveBtn = document.getElementById("bio_save_btn");

    let charCount = textarea.value.length;


    counter.textContent = charCount + " / 500";

    // Disable the save button if the character count exceeds 500
    if (charCount > 500) {
        saveBtn.disabled = true;
    } else {
        saveBtn.disabled = false;
    }
}

// Initialize the counter when the page loads
document.addEventListener("DOMContentLoaded", function () {
    // Debug: log when the page is fully loaded
    updateCharCount(); // Set counter based on existing bio text

    let bioInput = document.getElementById("bio_input");
    bioInput.addEventListener("input", updateCharCount); // Update counter while typing
});

// Edit the bio field
function editField(field) {
    let input = document.getElementById(field + '_input');
    let editBtn = document.getElementById(field + '_edit_btn');
    let saveBtn = document.getElementById(field + '_save_btn');
    let cancelBtn = document.getElementById(field + '_cancel_btn');

    // Store original value for potential cancellation
    input.setAttribute('data-original-value', input.value);

    // Enable the text area and focus
    input.removeAttribute("readonly");
    input.focus();

    // Show/hide the necessary buttons
    editBtn.style.display = "none";
    saveBtn.style.display = "inline";
    cancelBtn.style.display = "inline";


    updateCharCount(); // Update count when entering edit mode
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

    // If the character count exceeds 500, prevent saving
    if (newValue.length > 500) {
        alert("The field cannot exceed 500 characters.");
        return;  // Stop execution here, don't submit the form
    }

    updateFieldCustom(field, newValue);

    editBtn.style.display = "inline";
    saveBtn.style.display = "none";
    cancelBtn.style.display = "none";
    input.setAttribute("readonly", true);
}

function editProfileImage() {
    // Show the file input and Cancel/Save buttons; hide the Change button.
    document.getElementById("profile_image_edit").style.display = "block";
    document.getElementById("profile_image_cancel_btn").style.display = "inline";
    document.getElementById("profile_image_save_btn").style.display = "inline";
    document.getElementById("profile_image_change_btn").style.display = "none";
}

function cancelProfileImageEdit() {
    // Hide file input and Cancel/Save buttons; show Change button.
    document.getElementById("profile_image_edit").style.display = "none";
    document.getElementById("profile_image_cancel_btn").style.display = "none";
    document.getElementById("profile_image_save_btn").style.display = "none";
    document.getElementById("profile_image_change_btn").style.display = "inline";
    // Clear the file input value
    document.getElementById("profile_image_input").value = "";
}

function toggleProfileImageEdit() {
    // Toggle the visibility of the file input controls
    let editDiv = document.getElementById("profile_image_edit");
    editDiv.style.display = (editDiv.style.display === "none") ? "block" : "none";
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

    fetch(accountSettingsUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            // "Content-Type": "application/json",
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
                document.getElementById(field + '_input').value = newValue;
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


function saveProfileImage() {
    let fileInput = document.getElementById("profile_image_input");

    if (!fileInput.files.length) {
        alert("Please select an image before saving.");
        return;
    }

    let formData = new FormData();
    formData.append("field", "profile_image");
    formData.append("profile_image", fileInput.files[0]);


    fetch(accountSettingsUrl, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showNotification(data.message);

            // Update the profile image preview
            if (data.value) {
                document.getElementById("profile_image_display").src = data.value;
            }

            // Hide file input and buttons after saving
            cancelProfileImageEdit();
        } else if (data.error) {
            showNotification("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error saving profile image:", error);
    });
}


document.addEventListener("DOMContentLoaded", function () {
    let universitySelect = document.getElementById("university_input");
    let editBtn = document.getElementById("university_edit_btn");
    let saveBtn = document.getElementById("university_save_btn");
    let cancelBtn = document.getElementById("university_cancel_btn");

    // Fetch university choices and user data from the backend
    fetch('/accounts/get-university-data/')
    .then(response => {

        return response.json(); // Read response as JSON
    })
    .then(data => {
        let universityChoices = data.universities;
        let userUniversity = data.user_university;


        // Populate dropdown options
        universityChoices.forEach(university => {
            let option = document.createElement("option");
            option.value = university;
            option.textContent = university;
            universitySelect.appendChild(option);
        });

        // Set the user's saved university as the default selected option
        if (userUniversity && universityChoices.includes(userUniversity)) {
            universitySelect.value = userUniversity;
        }

        // Store the original value for cancel functionality
        universitySelect.setAttribute("data-original-value", universitySelect.value);
    })
    .catch(error => console.error("Error fetching university data:", error));

    // Edit button functionality
    editBtn.addEventListener("click", function () {
        universitySelect.removeAttribute("disabled");
        editBtn.style.display = "none";
        saveBtn.style.display = "inline";
        cancelBtn.style.display = "inline";
    });

    // Save button functionality
    saveBtn.addEventListener("click", function () {
        let selectedValue = universitySelect.value;
        updateFieldCustom("university", selectedValue);

        // Disable field and revert buttons
        universitySelect.setAttribute("disabled", true);
        editBtn.style.display = "inline";
        saveBtn.style.display = "none";
        cancelBtn.style.display = "none";

        // Store the new original value
        universitySelect.setAttribute("data-original-value", selectedValue);
    });

    // Cancel button functionality
    cancelBtn.addEventListener("click", function () {
        universitySelect.value = universitySelect.getAttribute("data-original-value"); // Revert value
        universitySelect.setAttribute("disabled", true);
        editBtn.style.display = "inline";
        saveBtn.style.display = "none";
        cancelBtn.style.display = "none";
    });
});


