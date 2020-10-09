var ws = new WebSocket("ws://" + location.hostname + ":80");

// When a message is received
ws.onmessage = function (evt) {
    document.getElementById("output").value = evt.data;
};


function init() {
    window.addEventListener('click', eventConfig);

    window.onload = function () {
        populateData();
    }
}


function populateData() {

    document.getElementById('wifi_ssid').value = params['ssid'];
    document.getElementById('wifi_pass').value = params['pass'];

    var wifiStatus = params['wifi_status'];
    console.log("WifiStatus: " + wifiStatus);

    var wifiText = 'Not connected to internet';

    if (wifiStatus == '1') {
        wifiText = 'Connected to internet'
    }

    document.getElementById('wifi_status').innerHTML = wifiText;

    // ws.send(JSON.stringify(data))
}

function eventConfig(e) {
    let d = {
        'div': e.target.closest('div'),
    }

    if (e.type == 'click') {
        if (d.div) {
            if (d.div.id == 'submit') {
                var data = {
                    'cmd': 'save_settings',
                    'wifi_ssid': document.getElementById('wifi_ssid').value,
                    'wifi_pass': document.getElementById('wifi_pass').value,
                };

                console.log("Saving settings...");
                // ws.send("Hello");
                ws.send(JSON.stringify(data));
            } else if (d.div.id == 'reset_bag') {
                var data = {
                    'cmd': 'reset_bag',
                    'volume_ml': 500,
                };

                console.log("Saving settings...");
                ws.send(JSON.stringify(data));
            }
        }
    }
}

init();