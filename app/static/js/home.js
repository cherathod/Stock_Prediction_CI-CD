// Select the input field and search icon
const searchBox = document.getElementById("searchBox");
const searchIcon = document.getElementById("searchIcon");

// Event 1: Detect user typing in the search box
searchBox.addEventListener("input", function () {
    console.log("User typed:", searchBox.value);
});

// Event 2: Trigger search on Enter key press
searchBox.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        alert("Searching for: " + searchBox.value);
    }
});

// Event 3: Click on search icon to trigger search
searchIcon.addEventListener("click", function () {
    alert("Searching for: " + searchBox.value);
});

// Event 4: Clear search input on double click
searchBox.addEventListener("dblclick", function () {
    searchBox.value = "";
    console.log("Search box cleared.");
});