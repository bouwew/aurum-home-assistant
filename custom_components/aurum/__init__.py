"""
Support for power production statistics from the AURUM Meetstekker web-page.

For more details about this platform, please refer to the documentation at
https://github.com/bouwew/aurum-home-assistant/

Configuration (example):

aurum:
   device: 192.168.0.110                  # ip adress of the meetstekker
   broker: 192.168.0.111                  # ip adress of the MQTT broker
   password: mqtt_password                # MQTT broker password
   username: mqtt_user                    # MQTT username
   select: [6,7,8,15,16,17,18,19,20,22]   # optional, example
   client: MQTT client-id                 # optional, default is 'aurum2mqtt'
   scan_interval: 20                      # reporting interval, optional, default 60 seconds (note: the Dutch Smart Meter refreshes every 10 seoconds)
   
PLAN: change the code so that the sensors are autodiscovered by HA!

"""
import logging
from datetime import timedelta

import voluptuous as vol

import urllib.request as ur
import xml.etree.ElementTree as ET
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json

from operator import itemgetter

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_DEVICE, CONF_PASSWORD, CONF_USERNAME, 
    CONF_SCAN_INTERVAL, EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers.event import async_track_time_interval

__version__ = '0.2.4'

_LOGGER = logging.getLogger(__name__)

REGISTERED = 0

CONF_BROKER = 'broker'
CONF_CLIENT = 'client'
CONF_LIST = 'select'

DOMAIN = 'aurum2mqtt'
DEFAULT_CL = 'aurum2mqtt'
DEFAULT_SELECT = list(range(23))

SCAN_INTERVAL = timedelta(seconds=60)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEVICE): cv.string,
        vol.Required(CONF_BROKER): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_LIST, default=DEFAULT_SELECT): vol.All(cv.ensure_list, [cv.positive_int]),
        vol.Optional(CONF_CLIENT, default=DEFAULT_CL): cv.string,
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
   select = conf.get(CONF_LIST)
   client = conf.get(CONF_CLIENT)
   scan_interval = conf.get(CONF_SCAN_INTERVAL)

   client_id = client
   auth = {'username':username, 'password':password}
   port = 1883
   keepalive = 300

   async def async_get_aurum_data(event_time):   
      """Get the topics from the AURUM API and send to the MQTT Broker."""
      payload_powerBattery = {
                     'name':'aurum_battery_power',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerBattery }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_powerBattery_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterOutBattery = {
                     'name':'aurum_battery_counter_out',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutBattery }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_counterOutBattery_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }

      payload_counterInBattery = {
                     'name':'aurum_battery_counter_in',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInBattery }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_counterInBattery_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_powerMCHP = {
                     'name':'aurum_mchp_power',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerMCHP }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_powerMCHP_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterOutMCHP = {
                     'name':'aurum_mchp_counter_out',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutMCHP }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_counterOutMCHP_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterInMCHP = {
                     'name':'aurum_mchp_counter_in',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInMCHP }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_counterInMCHP_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_powerSolar = {
                     'name':'aurum_solar_power',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerSolar }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_powerSolar_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterOutSolar = {
                     'name':'aurum_solar_counter_out',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterOutSolar }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_counterOutSolar_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterInSolar = {
                     'name':'aurum_solar_counter_in',
                     'unit_of_meas':'kWh',
                     'value_template':'{{ value_json.counterInSolar }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_counterInSolar_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_powerEV = {
                     'name':'aurum_EV_power',
                     'unit_of_meas':'W',
                     'value_template':'{{ value_json.powerEV }}',
                     'icon':'mdi:flash',
                     'state_topic':'aurum/sensors',
                     'unique_id':'aurum_powerEV_sensor',
                     'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterOutEV = {
                      'name':'aurum_ev_counter_out',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterOutEV }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterOutEV_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterInEV = {
                      'name':'aurum_ev_counter_in',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterInEV }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterInEV_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }      
      payload_powerMain = {
                      'name':'aurum_main_power',
                      'unit_of_meas':'W',
                      'value_template':'{{ value_json.powerMain }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_powerMain_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterOutMain = {
                      'name':'aurum_main_counter_out',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterOutMain }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterOutMain_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterInMain = {
                      'name':'aurum_main_counter_in',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterInMain }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterInMain_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_smartMeterTimestamp = {
                      'name':'aurum_smartmeter_timestamp',
                      "unit_of_meas":"",
                      'value_template':'{{ value_json.smartMeterTimestamp }}',
                      'icon':'mdi:av-timer',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_smartMeterTimestamp_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }          
      payload_powerElectricity = {
                      'name':'aurum_elec_power',
                      'unit_of_meas':'W',
                      'value_template':'{{ value_json.powerElectricity }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_powerElectricity_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterElectricityInLow = {
                      'name':'aurum_elec_counter_in_low',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityInLow }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterElectricityInLow_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterElectricityOutLow = {
                      'name':'aurum_elec_counter_out_low',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityOutLow }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterElectricityOutLow_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                     }
      payload_counterElectricityInHigh = {
                      'name':'aurum_elec_counter_in_high',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityInHigh }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterElectricityInHigh_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterElectricityOutHigh = {
                      'name':'aurum_elec_counter_out_high',
                      'unit_of_meas':'kWh',
                      'value_template':'{{ value_json.counterElectricityOutHigh }}',
                      'icon':'mdi:flash',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterElectricityOutHigh_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                     }
      payload_rateGas = {
                      'name':'aurum_gas_rate',
                      'unit_of_meas':'m3/h',
                      'value_template':'{{ value_json.rateGas }}',
                      'icon':'mdi:fire',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_rateGas_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                    }
      payload_counterGas = {
                      'name':'aurum_gas_counter',
                      'unit_of_meas':'m3',
                      'value_template':'{{ value_json.counterGas }}',
                      'icon':'mdi:fire',
                      'state_topic':'aurum/sensors',
                      'unique_id':'aurum_counterGas_sensor',
                      'device':{
                              'identifiers':'Aurum Meetstekker',
                              'name':'Aurum Meetstekker',
                              'model':'Meetstekker',
                              'manufacturer':'Aurum'
                              }
                     }
      global REGISTERED
      try:
         url = 'http://{}/measurements/output.xml'.format(device)
         tree = ET.parse(ur.urlopen(url))
         root = tree.getroot()
      except Exception as exception:
         _LOGGER.error("Unable to fetch data from AURUM. %s", exception)    
      else:
         if REGISTERED == 0:
            x = 0
            for child in root:
               if(child is not None):
                  parameter = child.tag
                  payload = "payload_"+str(parameter)
                  payload = locals()[payload]
                  payload = json.dumps(payload)
                  payload = payload.replace(": ", ":")
                  if x in select:
                     publish.single('homeassistant/sensor/aurum/{}/config'.format(parameter), payload, qos=0, retain=True, hostname=broker, port=port, auth=auth, client_id=client, protocol=mqtt.MQTTv311)
                  x = x+1
         REGISTERED = 1
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
         data = itemgetter(*select)(data)
         mqtt_message = json.dumps(data)
         payload = mqtt_message.replace("[", "{").replace("]", "}").replace(': ', '":"')
         publish.single('aurum/sensors', payload, qos=0, retain=True, hostname=broker, port=port, auth=auth, client_id=client, protocol=mqtt.MQTTv311)

   async_track_time_interval(hass, async_get_aurum_data, scan_interval)

   return True
