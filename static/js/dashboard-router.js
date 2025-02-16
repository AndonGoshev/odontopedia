document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll("#sidebar-router a");
    const sections = document.querySelectorAll("#work-field-container > div");


    function showSection(target) {
        sections.forEach(section => {
            section.style.display = section.id === target ? "block" : "none";
        });

        links.forEach(link => {
            link.classList.toggle("active", link.getAttribute("data-target") === target);
        });
    }

    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const target = this.getAttribute("data-target");
            showSection(target);
        });
    });

    // Show the first section by default
    showSection("tuitions-wrapper");
});