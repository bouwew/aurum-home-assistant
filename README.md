__Support for power production and consumption values and counters from the AURUM Meetstekker web-page.__

Place the file aurum.py in the custom_components directory and add the following 
to the configuration.yaml file (example):

```
aurum:
   device: 192.168.0.110     # ip adress of the meetstekker
   broker: 192.168.0.111     # ip adress of the MQTT broker you will use
   password: mqtt_password   # MQTT broker password
   username: mqtt_user       # MQTT username
   scan_interval: 20         # reporting interval, default 60 seconds (note: the Dutch Smart Meter refreshes every 10 seoconds)
```

Sensors can be created via:
(you probably do not need them all, pick them according to how your system is set up)

```
sensor:
  - platform: mqtt
    name: Battery power #power on the AC-side of the inverter-charger
    unit_of_measurement: "W"
    state_topic: "aurum/powerBattery"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Consumed from Battery #total provided AC power from the batteries
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterOutBattery"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Stored in Battery #total stored AC power into the batteries
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterInBattery"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: uCHP power #energy from any electricity-producing device, other than from solar energy
    unit_of_measurement: "W"
    state_topic: "aurum/powerMCHP"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: uCHP production "total uCHP production
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterOutMCHP"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: uCHP consumption #total uCHP consumption
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterInMCHP"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: PV power
    unit_of_measurement: "W"
    state_topic: "aurum/powerSolar"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: PV consumption
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterOutSolar"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: PV production
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterInSolar"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: EV power
    unit_of_measurement: "W"
    state_topic: "aurum/powerEV"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: EV consumption
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterOutEV"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: EV production
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterInEV"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Main power #when there is no Smart Meter with P1-port, a suitable electricity-meter can be read out instead
    unit_of_measurement: "W"
    state_topic: "aurum/powerMain"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Main consumption #total E consumption
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterOutMain"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Main production #total E production
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterInMain"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: DSMR timestamp # when a Smart Meter with P1-port is present, the below data is coming from the Smart Meter
    state_topic: "aurum/smartMeterTimestamp"
  - platform: mqtt
    name: E net consumption
    unit_of_measurement: "W"
    state_topic: "aurum/powerElectricity"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: E dal in totals
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterElectricityInLow"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: E dal uit totals
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterElectricityOutLow"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: E piek in totals
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterElectricityInHigh"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: E piek uit totals
    unit_of_measurement: "kWh"
    state_topic: "aurum/counterElectricityOutHigh"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Gas rate #works only with an analog gas meter
    unit_of_measurement: "m3/hr"
    state_topic: "aurum/rateGas"
    value_template: "{{ value_json | round(1) }}"
  - platform: mqtt
    name: Gas totals #total gas consumption
    unit_of_measurement: "m3"
    state_topic: "aurum/counterGas"
    value_template: "{{ value_json | round(1) }}"
```


