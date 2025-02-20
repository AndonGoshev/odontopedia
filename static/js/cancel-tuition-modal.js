document.addEventListener("DOMContentLoaded", function () {
    const cancelButtons = document.querySelectorAll(".cancel-tuition-button");
    const modal = document.getElementById("tuition-cancel-modal");
    const confirmButton = document.getElementById("tuition-confirm-cancel");
    const closeButton = document.getElementById("tuition-close-modal");

    let selectedBookingId = null;

    cancelButtons.forEach(button => {
        button.addEventListener("click", function () {
            selectedBookingId = this.getAttribute("data-booking-id");
            modal.style.display = "block"; // Show modal
        });
    });

    // Handle "Yes, Cancel" button
    confirmButton.addEventListener("click", function () {
        if (!selectedBookingId) return;

        fetch("/bookings/cancel-tuition/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),  // Ensure CSRF token is included
            },
            body: JSON.stringify({ booking_id: selectedBookingId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Tuition session cancelled successfully!");
                location.reload(); // Refresh the page
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => console.error("Error:", error));
    });

    // Handle "No" button to close the modal
    closeButton.addEventListener("click", function () {
        modal.style.display = "none";
        selectedBookingId = null;
    });

    // Function to get CSRF token from cookies
    function getCSRFToken() {
        let name = "csrftoken=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let cookies = decodedCookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let c = cookies[i].trim();
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
});
