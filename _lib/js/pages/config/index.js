import {default as l} from './src/common'


var ws = new WebSocket("ws://" + location.hostname + ":80");

// When a message is received
ws.onmessage = function (evt) {
    l.getDom('output').value = evt.data;
};

function init() {
    window.addEventListener('click', eventConfig);
    window.addEventListener('submit', eventConfig);

    window.onload = function () {
        populateData();
        l.loading.hide();
    }
}


function populateData() {
    // Test
    let mlSprayed = parseInt(params['ml_sprayed'], 10);
    let bagLevel = Math.round(((500 - mlSprayed) / 500) * 100);
    let bagPctMsg = bagLevel + "% remaining";
    let totalSprays = Math.round(mlSprayed / 0.8, 2);
    let spraysInBag = Math.round(500 / 0.8);

    /* Set params for user's screen */

    // Usage info
    l.getDom('bag_pct_msg').innerHTML = bagPctMsg;
    l.getDom('bag_level').value = bagLevel;
    l.getDom('volume_sprayed').innerHTML = mlSprayed + 'ml';
    l.getDom('total_sprays').innerHTML = totalSprays;
    l.getDom('c_total').innerHTML = spraysInBag;

    // Wifi info
    l.getDom('wifi_ssid').value = params['ssid'];
    l.getDom('wifi_pass').value = params['pass'];
    l.getDom('has_wifi').innerHTML = (params['has_wifi'] == '1') ? 'Connected to internet' : 'Not connected to internet';

    // Other settings
    l.getDom('melody_status').value = params['melody'];
    l.getDom('spray_time_ms').value = parseInt(params['spray_time'], 10);
}

function eventConfig(e) {
    let d = {
        'a': e.target.closest('a'),
        'button': e.target.closest('button'),
        'div': e.target.closest('div'),
        'form': e.target.closest('form'),
    }

    if(e.type == 'submit'){
        if(d.form && d.form.id == 'form_config'){
            e.preventDefault();

            let data = {
                'cmd': 'save_settings',
                'melody_status': l.getDom('melody_status').value,
                'spray_time': l.getDom('spray_time_ms').value,
                'wifi_ssid': l.getDom('wifi_ssid').value,
                'wifi_pass': l.getDom('wifi_pass').value,
            };

            console.log("Saving settings...");
            ws.send(JSON.stringify(data));
        }
    }

    if (e.type == 'click') {
        if (d.button) {
            if (d.button.id == 'reset_bag') {
                console.log("Resetting bag...");
                ws.send(JSON.stringify({
                    'cmd': 'reset_bag',
                    'volume_ml': 500,
                }));

                let spraysInBag = Math.round(500 / 0.8);

                l.getDom('bag_level').value = 100;                  // Reset bag level
                l.getDom('volume_sprayed').innerHTML = '0ml';       // Volume sprayed
                l.getDom('total_sprays').innerHTML = 0;
                l.getDom('c_total').innerHTML = spraysInBag;

                l.getDom("output").value = "Reset Bag";
            }
        }
    }
}

init();