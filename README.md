Support for reading power production and consumption values and counters from the AURUM Meetstekker web-page.

Place the files ```__init__.py``` and ```manifest.json``` in the custom_components/aurum directory and add the following 
to the configuration.yaml file (example):

```
aurum:
   device: 192.168.0.110                  # ip adress of the meetstekker
   broker: 192.168.0.111                  # ip adress of the MQTT broker
   username: mqtt_user                    # MQTT username
   password: mqtt_password                # MQTT broker password
   select: [6,7,8,15,16,17,18,19,20,22]   # optional, example
   client: MQTT client-id                 # optional, default is 'aurum2mqtt'
   scan_interval: 20                      # reporting interval, optional, default 60 seconds (note: the Dutch Smart Meter refreshes every 10 seoconds)

```

There are in total 23 sensors available:
```
- Battery power            #power-flow on the AC-side of the inverter-charger
  unit_of_measurement: "W"
- Consumed from Battery    #total provided AC power from the batteries
  unit_of_measurement: "kWh"
- Stored in Battery `      #total stored AC power into the batteries
  unit_of_measurement: "kWh"
- uCHP power               #power-flow from any electricity-producing device, other than from solar energy
  unit_of_measurement: "W"
- uCHP production          #total uCHP production
  unit_of_measurement: "kWh"
- uCHP consumption         #total uCHP consumption
  unit_of_measurement: "kWh"
- PV power                 #power-flow of the solar-inverterconnection
  unit_of_measurement: "W"
- PV consumption           #total solar-inverter consumption
  unit_of_measurement: "kWh"
- PV production            #total solar-inverter production
  nit_of_measurement: "kWh"
- EV power                 #power-flow of the Electrical Vehicle connection
  unit_of_measurement: "W"
- EV consumption           #total EV consumption
  unit_of_measurement: "kWh"
- EV production            #total EV production
  unit_of_measurement: "kWh"
- Main power               #power-flow of the electrical connection connected to the main meter
  (When there is no Smart Meter with P1-port, a suitable electricity-meter can be read out instead)
  unit_of_measurement: "W"
- Main consumption         #total Electricity consumption
  unit_of_measurement: "kWh"
- Main production          #total Electricity production
  unit_of_measurement: "kWh"
- DSMR timestamp           #When a Smart Meter with P1-port is present, this and the below data is coming from the Smart Meter
- E net consumption        #power-flow of the electrical connection connected to the DSMR meter with p1-port
  unit_of_measurement: "W"
- E low in totals          #total Electricity consumption - low tariff
  unit_of_measurement: "kWh"
- E low out totals         #total Electricity export - low tariff
  unit_of_measurement: "kWh"
- E high in totals         #total Electricity consumption - high tariff
  unit_of_measurement: "kWh"
- E high out totals        #total Electricity export - high tariff
  unit_of_measurement: "kWh"
- Gas rate                 #gas-flow, works only with an analog gas meter, needs a special add on
  unit_of_measurement: "m3/hr"
- Gas totals               #total gas consumption
  unit_of_measurement: "m3"
```
Not all sensort might be active. Look at http://'ip-address-of-the-Aurum-unit'/measurements/output.xml to find out which sensors show actual values. Then modify the numbers in the config-line ```select: [6,7,...]``` to match your installation.

The selected sensors are automatically detected by Home Assistant via MQTT discovery.

Please note: the MQTT messages are transmitted with the retain-function active. This makes these sensors compatible with the home Assistant Utility Meter: https://www.home-assistant.io/components/utility_meter/
