(function () {
    'use strict';

    /**
     * Get the DOM of an element
     */
    function ctd(target) {
      // If this is an Element, return the DOM
      if (target && target.nodeName) return target; // If this is an Element, return the DOM
      // If this is a string reference

      if (typeof target === 'string' || target instanceof String) {
        let dom = document.getElementById(target); // See if the string is an element's HTML ID

        if (dom) {
          // If the string is an element's HTML ID; return the DOM
          return dom;
        }
      } else {
        // If attempting to fetch the target
        throw new Error('DOM not found'); // Throw an error
      }
    }

    const l = {
      getDom: function (target) {
        return ctd(target);
      }
    };
    var ws = new WebSocket("ws://" + location.hostname + ":80"); // When a message is received

    ws.onmessage = function (evt) {
      l.getDom('output').value = evt.data;
    };

    function init() {
      window.addEventListener('click', eventConfig);

      window.onload = function () {
        populateData();
      };
    }

    function populateData() {
      // Test
      let mlSprayed = parseInt(params['ml_sprayed'], 10);
      let bagLevel = Math.round((500 - mlSprayed) / 500) * 100;
      let bagPctMsg = bagLevel + "% remaining"; // Set params for user's screen

      l.getDom('bag_pct_msg').innerHTML = bagPctMsg;
      l.getDom('bag_level').value = bagLevel;
      l.getDom('wifi_ssid').value = params['ssid'];
      l.getDom('wifi_pass').value = params['pass'];
      l.getDom('wifi_status').innerHTML = params['wifi_status'] == '1' ? 'Connected to internet' : 'Not connected to internet';
    }

    function eventConfig(e) {
      let d = {
        'a': e.target.closest('a'),
        'button': e.target.closest('button'),
        'div': e.target.closest('div')
      };

      if (e.type == 'click') {
        if (d.button) {
          e.preventDefault();

          if (d.button.id == 'submit') {
            var data = {
              'cmd': 'save_settings',
              'wifi_ssid': l.getDom('wifi_ssid').value,
              'wifi_pass': l.getDom('wifi_pass').value
            };
            console.log("Saving settings...");
            ws.send(JSON.stringify(data));
          } else if (d.button.id == 'reset_bag') {
            console.log("Resetting bag...");
            ws.send(JSON.stringify({
              'cmd': 'reset_bag',
              'volume_ml': 500
            }));
            l.getDom("output").value = "Reset Bag";
          }
        }
      }
    }

    init();

}());
