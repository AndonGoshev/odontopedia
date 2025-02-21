document.addEventListener("DOMContentLoaded", function () {
        const form = document.getElementById("book-slot-form");
        const dateSelect = document.getElementById("date-select");
        const timeSelect = document.getElementById("time-select");
        const focusAreaSelect = document.getElementById('focus-area-select')
        const descriptionInput = document.getElementById("description-input"); // New input field for description
        const submitButton = form.querySelector("button");
        const responseDiv = document.getElementById("booking-response");

        // Generate next 30 days dynamically for the date dropdown
        function populateDateDropdown() {
            const today = new Date();
            for (let i = 2; i < 30; i++) {
                let futureDate = new Date();
                futureDate.setDate(today.getDate() + i);
                let dateString = futureDate.toISOString().split("T")[0]; // Format YYYY-MM-DD

                let option = document.createElement("option");
                option.value = dateString;
                option.textContent = futureDate.toDateString();
                dateSelect.appendChild(option);
            }
        }

        // Helper function to clear a select element and add a default option
        function clearSelect(selectElement, defaultText) {
            while (selectElement.firstChild) {
                selectElement.removeChild(selectElement.firstChild);
            }
            let defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.disabled = true;
            defaultOption.selected = true;
            defaultOption.textContent = defaultText;
            selectElement.appendChild(defaultOption);
        }

        // Fetch available slots when a date is selected
        dateSelect.addEventListener("change", function () {
            const selectedDate = this.value;
            if (!selectedDate) return;

            // Clear time dropdown and show "Loading..." without innerHTML
            clearSelect(timeSelect, "Loading...");
            timeSelect.disabled = true;
            submitButton.disabled = true;

            fetch(`/bookings/available-slots/?date=${selectedDate}`)
                .then(response => response.json())
                .then(data => {
                    // Clear and set default "Choose a time" option
                    clearSelect(timeSelect, "Choose a time");

                    // Filter slots to only include those that match the selected date
                    const slotsForDate = data.available_slots.filter(slot => slot.date === selectedDate);
                    if (slotsForDate.length === 0) {
                        clearSelect(timeSelect, "No available slots");
                    } else {
                        slotsForDate.forEach(slot => {
                            let option = document.createElement("option");
                            option.value = slot.id; // Use slot ID for booking reference
                            option.textContent = slot.time; // Show time
                            timeSelect.appendChild(option);
                        });
                        timeSelect.disabled = false;
                    }
                })
                .catch(error => {
                    console.error("Error fetching time slots:", error);
                });
        });

        // Enable submit button when a time is selected
        timeSelect.addEventListener("change", function () {
            submitButton.disabled = !this.value;
        });

        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const selectedSlotId = timeSelect.value;
            const descriptionValue = descriptionInput.value.trim();
            const selectedFocusArea = focusAreaSelect.value; // Get focus area value

            // Validate description if necessary
            if (!descriptionValue) {
                responseDiv.textContent = "Please enter a description.";
                responseDiv.style.color = "red";
                return console.error('Description field cannot be empty.');
            }

            // You might also validate the focus area if needed:
            if (!selectedFocusArea) {
                responseDiv.textContent = "Please choose a focus area.";
                responseDiv.style.color = "red";
                return console.error('Focus area field cannot be empty.');
            }

            // Send slot ID, description, and focus area to the backend
            const payload = {
                slot_id: selectedSlotId,
                description: descriptionValue,
                focus_area: selectedFocusArea,
                date: dateSelect.value,
                time: timeSelect.options[timeSelect.selectedIndex].text,
            };

            fetch("/bookings/book-slot/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(payload)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message === "Booking successful") {
                        responseDiv.textContent = "Booking confirmed!";
                        responseDiv.style.color = "green";
                    } else {
                        responseDiv.textContent = "Booking failed: " + (data.error || "Unknown error");
                        responseDiv.style.color = "red";
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    responseDiv.textContent = "Booking failed: Network error";
                    responseDiv.style.color = "red";
                });
        });

        // Helper function to get CSRF token
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                let cookies = document.cookie.split(";");
                for (let i = 0; i < cookies.length; i++) {
                    let cookie = cookies[i].trim();
                    if (cookie.startsWith(name + "=")) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // Initialize the date dropdown
        populateDateDropdown();
    });
