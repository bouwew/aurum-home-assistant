"""
Support for power production statistics from the AURUM Meetstekker web-page.

For more details about this platform, please refer to the documentation at
https://github.com/bouwew/aurum-home-assistant/

Configuration (example):

aurum:
   device: 192.168.0.110      # ip adress of the meetstekker
   broker: 192.168.0.111      # ip adress of the MQTT broker
   password: mqtt_password   # MQTT broker password
   username: mqtt_user       # MQTT username
   scan_interval: 20         # reporting interval, default 60 seconds (note: the Dutch Smart Meter refreshes every 10 seoconds)
   
PLAN: change the code so that the sensors are autodiscovered by HA!

"""
import logging
from datetime import timedelta

import voluptuous as vol

import urllib.request as ur
import xml.etree.ElementTree as ET
import paho.mqtt.client as mqtt
import json

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_DEVICE, CONF_PASSWORD, CONF_USERNAME, 
    CONF_SCAN_INTERVAL, EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers.event import async_track_time_interval

__version__ = '0.2.0'

_LOGGER = logging.getLogger(__name__)

REGISTERED = 0

CONF_BROKER = 'broker'

DOMAIN = 'aurum'

SCAN_INTERVAL = timedelta(seconds=60)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEVICE): cv.string,
        vol.Required(CONF_BROKER): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL):
            cv.time_period,
    }),
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
   """Initialize the AURUM MQTT consumer"""
   conf = config[DOMAIN]
   device = conf.get(CONF_DEVICE)
   broker = conf.get(CONF_BROKER)
   username = conf.get(CONF_USERNAME)
   password = conf.get(CONF_PASSWORD)
   scan_interval = conf.get(CONF_SCAN_INTERVAL)

   client_id = 'HomeAssistant'
   port = 1883
   keepalive = 55

   mqttc = mqtt.Client(client_id, protocol=mqtt.MQTTv311)
   mqttc.username_pw_set(username, password=password)
   mqttc.connect(broker, port=port, keepalive=keepalive)

   async def async_stop_aurum(event):
      """Stop the Aurum MQTT component."""
      mqttc.disconnect()

   hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, async_stop_aurum)
   
   async def async_get_aurum_data(event_time):   
      """Get the topics from the AURUM API and send to the MQTT Broker."""
      payload_powerBattery = {
                     'name':'aurum_powerBattery',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerBattery}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterOutBattery = {
                     'name':'aurum_counterOutBattery',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutBattery}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterInBattery = {
                     'name':'aurum_counterInBattery',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInBattery}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_powerMCHP = {
                     'name':'aurum_powerMCHP',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerMCHP}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterOutMCHP = {
                     'name':'aurum_counterOutMCHP',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutMCHP}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterInMCHP = {
                     'name':'aurum_counterInMCHP',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInMCHP}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_powerSolar = {
                     'name':'aurum_powerSolar',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerSolar}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterOutSolar = {
                     'name':'aurum_counterOutSolar',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutSolar}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterInSolar = {
                     'name':'aurum_counterInSolar',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInSolar}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_powerEV = {
                     'name':'aurum_powerEV',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerEV}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterOutEV = {
                      'name':'aurum_counterOutEV',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterOutEV}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterInEV = {
                      'name':'aurum_counterInEV',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterInEV}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }      
      payload_powerMain = {
                      'name':'aurum_powerMain',
                      'unit_of_meas':'W',
                      'value_template':'{{ value_json.powerMain}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterOutMain = {
                      'name':'aurum_counterOutMain',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterOutMain}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterInMain = {
                      'name':'aurum_counterInMain',
                      'unit_of_meas':'kWh',
                      'value_template':'{{value_json.counterInMain}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_smartMeterTimestamp = {
                      'name':'aurum_smartMeterTimestamp',
                      "unit_of_meas":"",
                      'value_template':'{{value_json.smartMeterTimestamp}}',
                      'icon':'mdi:av-timer',
                      'state_topic':'aurum/sensors'
                    }          
      payload_powerElectricity = {
                      'name':'aurum_powerElectricity',
                      'unit_of_meas':'W',
                      'value_template':'{{ value_json.powerElectricity}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterElectricityInLow = {
                      'name':'aurum_counterElectricityInLow',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityInLow}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterElectricityOutLow = {
                      'name':'aurum_counterElectricityOutLow',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityOutLow}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                     }
      payload_counterElectricityInHigh = {
                      'name':'aurum_counterElectricityInHigh',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityInHigh}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterElectricityOutHigh = {
                      'name':'aurum_counterElectricityOutHigh',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityOutHigh}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                     }
      payload_rateGas = {
                      'name':'aurum_rateGas',
                      'unit_of_meas':'m3/h',
                      'value_template':'{{ value_json.rateGas}}',
                      'icon':'mdi:fire',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterGas = {
                      'name':'aurum_counterGas',
                      'unit_of_meas':'m3',
                      'value_template':'{{ value_json.counterGas}}',
                      'icon':'mdi:fire',
                      'state_topic':'aurum/sensors'
                     }
      global REGISTERED
      if REGISTERED == 0:
         try:
            url = 'http://{}/measurements/output.xml'.format(device)
            tree = ET.parse(ur.urlopen(url))
            root = tree.getroot()
         except Exception as exception:
            _LOGGER.error("Unable to fetch data from AURUM. %s", exception)    
         else:
            for child in root:
               if(child is not None):
                  parameter = child.tag
                  payload = "payload_"+str(parameter)
                  payload = locals()[payload]
                  payload = json.dumps(payload)
                  mqttc.publish('homeassistant/sensor/aurum/{}/config'.format(parameter), payload, qos=0, retain=True)
         REGISTERED = 1
      else:
         """Get the latest data from the AURUM API and send to the MQTT Broker."""
         try:
            url = 'http://{}/measurements/output.xml'.format(device)
            tree = ET.parse(ur.urlopen(url))
            root = tree.getroot()
         except Exception as exception:
            _LOGGER.error("Unable to fetch data from AURUM. %s", exception)    
         else:
            data=[]
            for child in root:
               if(child is not None):
                  parameter = child.tag
                  value = child.get('value')
                  try:
                     value = float(value)
                     value = round(value, 2)
                     value = str(value)
                  except:
                     pass
                  j_str = json.dumps({parameter:value})
                  j_str = j_str.replace('{"', "").replace('"}', "").replace('"', "")
                  data.append(j_str)
            mqtt_message=json.dumps(data)
            mqtt_message = mqtt_message.replace("[", "{").replace("]", "}").replace(': ', '":"')
            mqttc.publish('aurum/sensors', mqtt_message, qos=0, retain=True)

   async_track_time_interval(hass, async_get_aurum_data, scan_interval)

   return True
