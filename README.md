__Support for power production and consumption values and counters from the AURUM Meetstekker web-page.__

Place the files ```__init__.py``` and ```manifest.json``` in the ```custom_components/aurum``` directory and add the following 
to the configuration.yaml file (example):

```
aurum:
   device: 192.168.0.110     # IP adress of the Aurum meetstekker
   broker: 192.168.0.111     # IP adress of the MQTT broker that will be used to connect to
   password: mqtt_password   # MQTT broker password
   username: mqtt_user       # MQTT username
   client: aurum             # MQTT client-id, optional, default set to 'aurum'
   scan_interval: 20         # reporting interval, optional, default 60 seconds (note: the Dutch Smart Meter refreshes every 10 seconds)
```

Sensors can be created via:
(you probably do not need them all, pick them according to how your system is set up)

```
sensor:
  - platform: mqtt
    name: Battery power #power on the AC-side of the inverter-charger
    unit_of_measurement: "W"
    state_topic: "homeassistant/sensor/aurum/powerBattery"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Consumed from Battery #total provided AC power from the batteries
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterOutBattery"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Stored in Battery #total stored AC power into the batteries
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterInBattery"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: uCHP power #energy from any electricity-producing device, other than from solar energy
    unit_of_measurement: "W"
    state_topic: "homeassistant/sensor/aurum/powerMCHP"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: uCHP production "total uCHP production
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterOutMCHP"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: uCHP consumption #total uCHP consumption
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterInMCHP"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: PV power
    unit_of_measurement: "W"
    state_topic: "homeassistant/sensor/aurum/powerSolar"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: PV consumption
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterOutSolar"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: PV production
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterInSolar"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: EV power
    unit_of_measurement: "W"
    state_topic: "homeassistant/sensor/aurum/powerEV"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: EV consumption
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterOutEV"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: EV production
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterInEV"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Main power #when there is no Smart Meter with P1-port, a suitable electricity-meter can be read out instead
    unit_of_measurement: "W"
    state_topic: "homeassistant/sensor/aurum/powerMain"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Main consumption #total E consumption
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterOutMain"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Main production #total E production
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterInMain"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: DSMR timestamp # when a Smart Meter with P1-port is present, the below data is coming from the Smart Meter
    state_topic: "homeassistant/sensor/aurum/smartMeterTimestamp"
  - platform: mqtt
    name: E net consumption
    unit_of_measurement: "W"
    state_topic: "homeassistant/sensor/aurum/powerElectricity"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: E dal in totals
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterElectricityInLow"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: E dal uit totals
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterElectricityOutLow"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: E piek in totals
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterElectricityInHigh"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: E piek uit totals
    unit_of_measurement: "kWh"
    state_topic: "homeassistant/sensor/aurum/counterElectricityOutHigh"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Gas rate #works only with an analog gas meter
    unit_of_measurement: "m3/hr"
    state_topic: "homeassistant/sensor/aurum/rateGas"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Gas totals #total gas consumption
    unit_of_measurement: "m3"
    state_topic: "homeassistant/sensor/aurum/counterGas"
    value_template: "{{ value_json | round(1) }}"
```

Please note: the MQTT messages are transmitted with the retain-function active. This makes these sensors compatible with the home Assistant Utility Meter: https://www.home-assistant.io/components/utility_meter/
