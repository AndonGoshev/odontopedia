document.addEventListener("DOMContentLoaded", function () {
    const cancelButtons = document.querySelectorAll(".cancel-tuition-button");

    cancelButtons.forEach(button => {
        const date = button.getAttribute("data-date");  // Get date from button
        const time = button.getAttribute("data-time");  // Get time from button

        const sessionDateTime = new Date(`${date}T${time}`);  // Convert to Date object
        const now = new Date();

        const diffHours = (sessionDateTime - now) / (1000 * 60 * 60); // Difference in hours

        if (diffHours < 24) {
            button.disabled = true;  // Disable if less than 24h left
        }
    });
});