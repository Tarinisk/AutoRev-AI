const SERVER_URL = "http://localhost:5000/cmd";

async function send(cmd) {
    console.log("SEND", cmd);
    const statusDisplay = document.getElementById('status-msg');
    if (statusDisplay) statusDisplay.innerText = ">> " + cmd;

    try {
        const response = await fetch(SERVER_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cmd })
        });
        const data = await response.json();
        return data;
    } catch (err) {
        console.error(err);
        if (statusDisplay) {
            statusDisplay.innerText = "ERROR: Check Server Connection";
            statusDisplay.style.color = "#ff3366";
        }
        return null;
    }
}

// Helper to set active nav link
document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;
    const page = path.split("/").pop();
    const links = document.querySelectorAll(".nav-links a");
    
    links.forEach(link => {
        if (link.getAttribute("href") === page) {
            link.classList.add("active");
        }
    });
});

// Toggle live feed (for nav button)
function toggleLiveFeed() {
    // Navigate to live feed only page
    window.location.href = 'livefeed.html';
}