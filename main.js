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
    // loading time
    function showPageLoadTime() {
        // Check if the browser supports the performance API
        if (window.performance && window.performance.timing) {
            // Get the timing object
            var timing = window.performance.timing;

            // Check if the necessary timing events are available
            if (timing.loadEventEnd > 0 && timing.navigationStart > 0) {
                // Calculate the page load time
                var loadTime = (timing.loadEventEnd - timing.navigationStart) / 1000;

                // Log the result in the console
                // console.log("Page load time: " + loadTime + " seconds");
                // write to load_time
                document.querySelector("#load_time").innerHTML = loadTime + " seconds";
            } else {
                // Retry after 100 milliseconds if timing data is not available yet
                setTimeout(showPageLoadTime, 100);
            }
        } else {
            // console.log("Page load time measurement is not supported in this browser.");
        }
    }

    // Call the function when the page has fully loaded
    window.addEventListener("load", showPageLoadTime);
});

