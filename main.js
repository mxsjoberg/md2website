document.addEventListener("DOMContentLoaded", function() {
    // toggle invert
    var invert = document.querySelector("#invert");
    invert.addEventListener("click", function() {
        document.querySelector("html").classList.toggle("invert");
        // save to local storage
        if (document.querySelector("html").classList.contains("invert")) {
            localStorage.setItem("invert", "true");
        } else {
            localStorage.setItem("invert", "false");
        }
    });
    // check local storage
    if (localStorage.getItem("invert") == "true") {
        document.querySelector("html").classList.add("invert");
    }
});

