document.addEventListener("DOMContentLoaded", function () {
    const notificationBell = document.getElementById("notificationBell");
    const notificationBadge = document.getElementById("notificationBadge");
    const notificationDropdown = document.getElementById("notificationDropdown");

    // Function to fetch live notifications
    function fetchNotifications() {
        fetch("/get_notifications")
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    notificationDropdown.innerHTML = data
                        .map(news => `<p><a href="${news.link}" target="_blank">${news.title}</a></p>`)
                        .join("");
                    notificationBadge.innerText = data.length;
                    notificationBadge.style.display = "inline-block";
                } else {
                    notificationDropdown.innerHTML = "<p>No new notifications</p>";
                    notificationBadge.style.display = "none";
                }
            })
            .catch(error => console.error("Error fetching notifications:", error));
    }

    // Update notifications every 10 seconds
    setInterval(fetchNotifications, 10000);

    // Show dropdown on click
    notificationBell.addEventListener("click", () => {
        notificationDropdown.style.display =
            notificationDropdown.style.display === "block" ? "none" : "block";
    });

    // Initial fetch
    fetchNotifications();
});
