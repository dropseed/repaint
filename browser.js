import morphdom from "morphdom";

const RELOAD_EVENT = "browser-reload";
const RELOAD_ASSETS_EVENT = "browser-reload-assets";
const CONNECT_EVENT = "browser-connect";

const port = document.currentScript.dataset["repaintPort"] || "8765";
const ws = new WebSocket("ws://localhost:" + port);

function reload() {
    fetch(window.location.pathname)
        .then(function(response) {
            return response.text();
        })
        .then(function(text) {
            morphdom(document.documentElement, text);
        });
}

function reloadAssets(assets) {
    for (const asset of assets) {
        if (asset.endsWith(".css")) {
            for (const stylesheet of document.styleSheets) {
                if (stylesheet.href === window.location.origin + "/" + asset) {
                    // Makes the stylesheet reload without changing anything
                    stylesheet.ownerNode.href += "";
                }
            }
        } else {
            console.log("Repaint unknown asset type", asset);
        }
    }
}

ws.onopen = function() {
    ws.send(JSON.stringify({
        "type": CONNECT_EVENT,
        "url": window.location.pathname,
    }));
    console.log("Connected to Repaint", ws);
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
        reload();
    }

    if (data.type == RELOAD_ASSETS_EVENT) {
        console.log("Repaint asset reload received", event)
        reloadAssets(data["assets"]);
    }
};
