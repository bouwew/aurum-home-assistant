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

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_DEVICE, CONF_PASSWORD, CONF_USERNAME, 
    CONF_SCAN_INTERVAL, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers.event import async_track_time_interval

__version__ = '0.2.0'

_LOGGER = logging.getLogger(__name__)

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
   import paho.mqtt.client as mqtt
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
   
   async def async_init_aurum_data():
      """Get the topics from the AURUM API and send to the MQTT Broker."""
      payload_powerBattery = {
                     'name':'powerBattery',
                     'device_class':'meter',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerBattery}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterOutBattery = {
                     'name':'counterOutBattery',                     
                     'device_class':'meter',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutBattery}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterInBattery = {
                     'name':'counterInBattery',
                     'device_class':'meter',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInBattery}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_powerMCHP = {
                     'name':'powerMCHP',
                     'device_class':'meter',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerMCHP}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterOutMCHP = {
                     'name':'counterOutMCHP',
                     'device_class':'meter',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutMCHP}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterInMCHP = {
                     'name':'counterInMCHP',
                     'device_class':'meter',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInMCHP}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_powerSolar = {
                     'name':'powerSolar',
                     'device_class':'meter',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerSolar}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterOutSolar = {
                     'name':'counterOutSolar',
                     'device_class':'meter',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutSolar}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterInSolar = {
                     'name':'counterInSolar',
                     'device_class':'meter',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInSolar}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_powerEV = {
                     'name':'powerEV',
                     'device_class':'meter',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerEV}}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors'
                    }
      payload_counterOutEV = {
                      'name':'counterOutEV',
                      'device_class':'meter',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterOutEV}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterInEV = {
                      'name':'counterInEV',
                      'device_class':'meter',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterInEV}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }      
      payload_powerMain = {
                      'name':'powerMain',
                      'device_class':'meter',
                      'unit_of_meas':'W',
                      'value_template':'{{ value_json.powerMain}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterOutMain = {
                      'name':'counterOutMain',
                      'device_class':'meter',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterOutMain}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterInMain = {
                      'name':'counterInMain',
                      'device_class':'meter',
                      'unit_of_meas':'kWh',
                      'value_template':'{{value_json.counterInMain}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_smartMeterTimestamp = {
                      'name':'smartMeterTimestamp',
                      'device_class':'time_date',
                      "unit_of_meas":"",
                      'value_template':'{{value_json.smartMeterTimestamp}}',
                      'icon':'mdi:av-timer',
                      'state_topic':'aurum/sensors'
                    }          
      payload_powerElectricity = {
                      'name':'powerElectricity',
                      'device_class':'meter',
                      'unit_of_meas':'W',
                      'value_template':'{{ value_json.powerElectricity}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterElectricityInLow = {
                      'name':'counterElectricityInLow',
                      'device_class':'meter',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityInLow}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterElectricityOutLow = {
                      'name': 'counterElectricityOutLow',
                      'device_class':'meter',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityOutLow}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                     }
      payload_counterElectricityInHigh = {
                      'name':'counterElectricityInHigh',
                      'device_class':'meter',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityInHigh}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterElectricityOutHigh = {
                      'name':'counterElectricityOutHigh',
                      'device_class':'meter',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityOutHigh}}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors'
                     }
      payload_rateGas = {
                      'name':'rateGas',
                      'device_class':'meter',
                      'unit_of_meas':'m3/h',
                      'value_template':'{{ value_json.rateGas}}',
                      'icon':'mdi:fire',
                      'state_topic':'aurum/sensors'
                    }
      payload_counterGas = {
                      'name':'counterGas',
                      'device_class':'meter',
                      'unit_of_meas':'m3',
                      'value_template':'{{ value_json.counterGas}}',
                      'icon':'mdi:fire',
                      'state_topic':'aurum/sensors'
                     }      
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
                 mqttc.publish('homeassistant/sensor/aurum/{}'.format(parameter)'/config', globals()[payload], qos=0, retain=True)
   
   async def async_get_aurum_data(event_time):
       """Get the latest data from the AURUM API and send to the MQTT Broker."""
       try:
          url = 'http://{}/measurements/output.xml'.format(device)
          tree = ET.parse(ur.urlopen(url))
          root = tree.getroot()
       except Exception as exception:
          _LOGGER.error(
              "Unable to fetch data from AURUM. %s", exception)    
       else:
          data=[]         
          for child in root:
              if(child is not None):
                  parameter = child.tag
                  value = child.get('value')
                  j_str = json.dumps({parameter:value})
                  j_str = j_str.replace("{", "").replace("\"", "").replace("}", "")
                  data.append(j_str)
          mqtt_message=json.dumps(data)
          mqtt_message = mqtt_message.replace("[", "{").replace("]", "}")
          mqttc.publish('aurum/sensors', mqtt_message, qos=0, retain=True)
                     
   async_init_aurum_data()
   async_track_time_interval(hass, async_get_aurum_data, scan_interval)

   return True
