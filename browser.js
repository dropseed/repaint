import morphdom from "morphdom";

const RELOAD_EVENT = "browser-reload";
const CONNECT_EVENT = "browser-connect";
const port = document.currentScript.getAttribute("data-port") || "8765";
const ws = new WebSocket("ws://localhost:" + port);

ws.onopen = function() {
    ws.send(JSON.stringify({
        "type": CONNECT_EVENT,
        "url": window.location.pathname,
    }));
    console.log("Connected to Repaint websocket", ws);
};
ws.onerror = function(e) {
    console.log("Repaint websocket error", e);
};
ws.onclose = function(e) {
    console.log("Repaint websocket closed", e);
};
ws.onmessage = function (event) {
    var data = JSON.parse(event.data);
    if (data.type == RELOAD_EVENT) {
        console.log("Repaint reload received", event)

        fetch(window.location.pathname)
            .then(function(response) {
                return response.text();
            })
            .then(function(text) {
                // morphdom the new content
                morphdom(document.documentElement, text);
            });
    }
};
