# Current Setup

### Config Params




| Param                       |  Type  | Description                                                                              | Enabled |
|:----------------------------|:------:|:-----------------------------------------------------------------------------------------|:-------:|
| `ota_github_url`            | string | The URL of the GitHub repo to update the project from                                    |         |
| `enable_led`                |  bool  |                                                                                          |         |
| `melody_on_boot`            |  bool  |                                                                                          |         |
| `melody_on_spray`           |  bool  |                                                                                          |         |
| `enable_wifi`               |  bool  |                                                                                          |         |
| `pump_delay_ms`             |  int   | How many milliseconds the pump waits before turning on after the spray button is pressed |   Yes   |
| `pump_run_time_ms`          |  int   | How long (in milliseconds) the pump runs for each spray burst                            |   Yes   |
| `relay_delay_ms`            |  int   | How long to wait after the pump starts before the relay opens                            |   Yes   |
| `relay_open_time_ms`        |  int   | How long the relay is open                                                               |   Yes   |
| `spray_burst_count`         |  int   | How many times the nozzle sprays when the spray button is pressed                        |         |
| `total_unit_spray_time`     |  int   | Total time (in milliseconds) the unit has sprayed solution                               |         |
| `total_doypack_spray_time ` |  int   | Total tiem (in milliseconds) the current doypack has sprayed solution                    |         |
| `wifi_connect_on_boot`      |  bool  | True if the unit automatically connects to WiFi when turned on                           |   Yes   |
| `wifi_status`               |  bool  | True if the unit is connected to the WiFi network                                        |   Yes   |
| `wifi_ssid`                 | string | The name of the WiFi network the ShoeTizer connects to for internet access               |   Yes   |
| `wifi_pass`                 | string | The password for the WiFi network                                                        |   Yes   |


```
Needed Features
|-- Button on unit to enable WiFi broadcast so users can edit the settings
|-- Easy way for people to specify the bag has been replaced with a new one
```



### OTA Update
* In REPL run `foce_ota()`.  This will pull the most recent commit to the master branch.
* Run `force_ota('dir_name')` if you want to update a specific directory with the same dir in master branch



#### REPL Commands
```python
# View contents of a directory
import os
os.listdir()

# Remove file
import os
os.remove('/ota_updater/main.py')

# View contents of file
with open('/next/.version_on_reboot', 'r') as f:
    print(f.read())
    
for f in os.listdir():
    print(f)
```



## WebSockets

**Ref**
* https://github.com/BetaRavener/upy-websocket-server

###  Testing WebSocket
1. Connect to the ESP WiFi network
2. In REPL run `import websocket_demo`
3. Open the browser and go to: 192.168.4.1


#### WebSocket Multi
1. Connect to the ESP WiFi network
2. In REPL run `import multiserver.websocket_multi_demo` `import websocket_multi_demo`
3. Open the browser and go to: 192.168.4.1