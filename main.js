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
    // toggle styling
    var styling = document.querySelector("#styling");
    styling.addEventListener("click", function() {
        document.querySelector("html").classList.toggle("styling");
        // save to local storage
        if (document.querySelector("html").classList.contains("styling")) {
            localStorage.setItem("styling", "true");
        } else {
            localStorage.setItem("styling", "false");
        }
    });
    // check local storage
    if (localStorage.getItem("invert") == "true") {
        document.querySelector("html").classList.add("invert");
    }
    if (localStorage.getItem("styling") == "true") {
        document.querySelector("html").classList.add("styling");
    }
    // loading time
    function showPageLoadTime() {
        // check if the browser supports the performance API
        if (window.performance && window.performance.timing) {
            var timing = window.performance.timing;
            // check if the necessary timing events are available
            if (timing.loadEventEnd > 0 && timing.navigationStart > 0) {
                // calculate the DOMContentLoaded time in seconds
                // var domContentLoadedTime = (timing.domContentLoadedEventEnd - timing.navigationStart) / 1000;
                var domContentLoadedTime = timing.domContentLoadedEventEnd - timing.navigationStart;
                // calculate the page load time in seconds
                // var loadTime = (timing.loadEventEnd - timing.navigationStart) / 1000;
                var loadTime = timing.loadEventEnd - timing.navigationStart;
                // write to dom_time
                // document.querySelector("#dom_time").innerHTML = domContentLoadedTime + " seconds";
                document.querySelector("#dom_time").innerHTML = domContentLoadedTime + " ms";
                // write to load_time
                // document.querySelector("#load_time").innerHTML = loadTime + " seconds";
                document.querySelector("#load_time").innerHTML = loadTime + " ms";
            } else {
                setTimeout(showPageLoadTime, 100);
            }
        }
    }
    // call the function when the page has fully loaded
    window.addEventListener("load", showPageLoadTime);
});