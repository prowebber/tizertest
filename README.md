# Current Setup

## Known Bugs

### WiFi broadcast cannot restart without doing a soft reboot
   * It stops after the message 'clock synced to UTC'

### WiFi broadcast won't keep open connection with Android devices
When Android interacts with the WebSocket connection the following happens:
* ECP will not complete the request
* Android disconnects or hangs
* The ECP needs to be restarted

#### Steps to reproduce
1. Broadcast WiFi from device
2. Connect to device via Android and go to `192.168.4.1`
3. Click any of the buttons that use WebSocket connection
4. The

### Status Alerts


| Mode            | LED          | Melody             |
|:----------------|:-------------|:-------------------|
| WiFi connecting | Double blink |                    |
| Low fluid       | Single blink |                    |
|                 | Double blink | One note per blink |
|                 | Single blink | One note per blink |

### Config Params

| Param            |  Type  | Description                                                                              | Enabled |
|:-----------------|:------:|:-----------------------------------------------------------------------------------------|:-------:|
| `unit_id`        | string | The ID of the device                                                                     |         |
| `bag_id`         |  int   | The ID of the doypack                                                                    |         |
| `enable_led`     |  int   |                                                                                          |         |
| `enable_wifi`    |  bool  |                                                                                          |         |
| `mute`           |  bool  |                                                                                          |         |
| `ota_github_url` | string | The URL of the GitHub repo to update the project from                                    |         |
| `ota_tgt_dir`    | string | The default directory to update via OTA                                                  |         |
| `pump_delay`     |  int   | How many milliseconds the pump waits before turning on after the spray button is pressed |   Yes   |
| `pump_ms`        |  int   | How long (in milliseconds) the pump runs for each spray burst                            |   Yes   |
| `relay_delay`    |  int   | How long to wait after the pump starts before the relay opens                            |   Yes   |
| `relay_ms`       |  int   | How long the relay is open                                                               |   Yes   |
| `bag_spray_ms `  |  int   | Total tiem (in milliseconds) the current doypack has sprayed solution                    |         |
| `unit_spray_ms`  |  int   | Total time (in milliseconds) the unit has sprayed solution                               |         |
| `wifi_on_boot`   |  bool  | True if the unit automatically connects to WiFi when turned on                           |   Yes   |
| `has_wifi`       |  bool  | True if the unit is connected to the WiFi network                                        |   Yes   |
| `wifi_ssid`      | string | The name of the WiFi network the ShoeTizer connects to for internet access               |   Yes   |
| `wifi_pass`      | string | The password for the WiFi network                                                        |   Yes   |


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
with open('main.py', 'r') as f:
    print(f.read())
    
for f in os.listdir():
    print(f)
```



## WebSockets

**Ref**
* https://github.com/BetaRavener/upy-websocket-server

#### WebSocket Multi
1. Connect to the ESP WiFi network
2. In REPL call `setup()` in the main.py
3. Open the browser and go to: 192.168.4.1



## Features

### Working Features


### Future Features

#### Keep Track of Doypack Usage
Know how much fluid is remaining in each doypack.  Be able to show the user the level of
remaining solution.  Alert the user if the solution is running low.

#### Keep Track of Device Usage
Know how frequently devices are being used.  Helpful to determine lifespan of units or
components.

#### Know what software version each device is using
We know which devices are using what version.  Use the API to push the tizer software version to the database.
Probably need to push this to the 'usage' database tables as well so we can monitor how different versions
are used.  Wouldn't be a bad idea to include the current version in the `config.txt` file.

#### Detect Overuse
If the device is used too heavily/frequently within a small time window, alert the
user the spray area may need to be dried.
