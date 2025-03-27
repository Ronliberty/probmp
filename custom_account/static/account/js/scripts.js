document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".sidebar-link a");
    const mainContent = document.querySelector("main");

    links.forEach(link => {
        link.addEventListener("click", async (event) => {
            event.preventDefault();

            const url = link.getAttribute("href");

            // Skip the logout link
            if (url === "") {
                console.log("Logout clicked. No action taken.");
                return;
            }

            try {
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(`Error fetching the template: ${response.status} ${response.statusText}`);
                }

                const template = await response.text();
                mainContent.innerHTML = template;
            } catch (error) {
                console.error("Error loading template:", error);

                // Optionally, display an error message in the main section
                mainContent.innerHTML = `<div style="color: red;">Failed to load content. Please try again later.</div>`;
            }
        });
    });
});
