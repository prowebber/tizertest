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
    let mlSprayed = parseInt(params['ssid'], 10);
    let bagLevel = Math.round((500 - mlSprayed) / 500)

    // Set params for user's screen
    document.getElementById('bag_level').value = bagLevel;
    document.getElementById('wifi_ssid').value = params['ssid'];
    document.getElementById('wifi_pass').value = params['pass'];
    document.getElementById('wifi_status').innerHTML = (params['wifi_status'] == '1') ? 'Connected to internet' : 'Not connected to internet';
}

function eventConfig(e) {
    let d = {
        'a': e.target.closest('a'),
        'button': e.target.closest('button'),
        'div': e.target.closest('div'),
    }

    if (e.type == 'click') {
        if (d.button) {
            if (d.button.id == 'submit') {
                e.preventDefault();
                var data = {
                    'cmd': 'save_settings',
                    'wifi_ssid': document.getElementById('wifi_ssid').value,
                    'wifi_pass': document.getElementById('wifi_pass').value,
                };

                console.log("Saving settings...");
            }
            else if (d.button.id == 'reset_bag') {
                e.preventDefault();
                var data = {
                    'cmd': 'reset_bag',
                    'volume_ml': 500,
                };

                console.log("Resetting bag...");
                ws.send(JSON.stringify({
                    'cmd': 'reset_bag',
                    'volume_ml': 500,
                }));

                document.getElementById("output").value = "Reset Bag";
                console.log("Reset...");
            }
        }
    }
}

init();