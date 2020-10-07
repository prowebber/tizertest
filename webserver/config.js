var ws = new WebSocket("ws://" + location.hostname + ":80");

// When a message is received
ws.onmessage = function (evt) {
    document.getElementById("output").value = evt.data;
};


function init() {
    window.addEventListener('click', eventConfig);
}

function eventConfig(e) {
    let d = {
        'div': e.target.closest('div'),
    }

    if (e.type == 'click') {
        if (d.div && d.div.id == 'submit') {

            var data = {
                'action': 'save_settings',
                'wifi_ssid': document.getElementById('wifi_ssid').value,
                'wifi_pass': document.getElementById('wifi_pass').value,
            };

            console.log("clicked");
            console.log("sending...", data)
            // ws.send("Hello");
            ws.send(JSON.stringify(data))
        }
    }
}

init();