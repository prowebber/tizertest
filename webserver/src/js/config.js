(function () {
    'use strict';

    function init() {
      window.addEventListener('click', eventConfig);

      window.onload = function () {
        populateData();
      };
    }

    function populateData() {
      var wifiText = 'Not connected to internet';
      document.getElementById('wifi_status').innerHTML = wifiText;
    }

    function eventConfig(e) {
      let d = {
        'div': e.target.closest('div')
      };

      if (e.type == 'click') {
        if (d.div) {
          if (d.div.id == 'submit') {
            var data = {
              'cmd': 'save_settings',
              'wifi_ssid': document.getElementById('wifi_ssid').value,
              'wifi_pass': document.getElementById('wifi_pass').value
            };
            console.log("Saving settings...");
          } else if (d.div.id == 'reset_bag') {
            var data = {
              'cmd': 'reset_bag',
              'volume_ml': 500
            };
            console.log("Saving settings...");
            document.getElementById("output").value = "Reset Bag";
          }
        }
      }
    }

    init();

}());
