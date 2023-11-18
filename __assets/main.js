document.addEventListener("DOMContentLoaded", function() {
    // toggle theme
    try {
        var theme = document.querySelector("#theme");
        theme.addEventListener("change", function() {
            if (theme.checked == true) {
                theme.checked = true;
                document.querySelector("html").classList = "styling dark";
                localStorage.setItem("dark", "true");
            } else {
                theme.checked = false;
                document.querySelector("html").classList = "styling";
                localStorage.setItem("dark", "false");
            }
            // save to local storage
            // if (document.querySelector("html").classList.contains("dark")) {
            //     localStorage.setItem("dark", "true");
            // } else {
            //     localStorage.setItem("dark", "false");
            // }
        });
    } catch {}
    // toggle styling
    // try {
    //     var styling = document.querySelector("#styling");
    //     styling.addEventListener("click", function() {
    //         document.querySelector("html").classList.toggle("styling");
    //         // save to local storage
    //         if (document.querySelector("html").classList.contains("styling")) {
    //             localStorage.setItem("styling", "true");
    //         } else {
    //             localStorage.setItem("styling", "false");
    //         }
    //     });
    // } catch {}
    // check local storage
    if (localStorage.getItem("dark") == "true") {
        document.querySelector("html").classList = "styling dark";
        var theme = document.querySelector("#theme");
        theme.checked = true;
    } else {
        // init local storage
        if (document.querySelector("html").classList.contains("dark")) {
            document.querySelector("html").classList = "styling dark";
            var theme = document.querySelector("#theme");
            theme.checked = true;
            // persist
            localStorage.setItem("dark", "true");
        } else {
            document.querySelector("html").classList = "styling";
            var theme = document.querySelector("#theme");
            theme.checked = false;
            // persist
            localStorage.setItem("dark", "false");
        }
    }
    // if (localStorage.getItem("styling") == "true") {
    //     document.querySelector("html").classList.add("styling");
    // }
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
                try {
                    // document.querySelector("#dom_time").innerHTML = domContentLoadedTime + " seconds";
                    document.querySelector("#dom_time").innerHTML = domContentLoadedTime + " ms";
                    // write to load_time
                    // document.querySelector("#load_time").innerHTML = loadTime + " seconds";
                    document.querySelector("#load_time").innerHTML = loadTime + " ms";
                } catch {}
            } else {
                setTimeout(showPageLoadTime, 100);
            }
        }
    }
    // call the function when the page has fully loaded
    window.addEventListener("load", showPageLoadTime);
});