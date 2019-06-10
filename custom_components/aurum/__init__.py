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
        json_attributes = ['powerBattery', 'counterOutBattery', 'counterInBattery', 'powerMCHP', 'counterOutMCHP', 'counterInMCHP', \
                           'powerSolar', 'counterOutSolar', 'counterInSolar', 'powerEV', 'counterOutEV', 'counterInEV', \
                           'powerMain', 'counterOutMain', 'counterInMain', 'smartMeterTimestamp', 'powerElectricity' \
                           'counterElectricityInLow', 'counterElectricityOutLow', 'counterElectricityInHigh' \
                           'counterElectricityOutHigh', 'rateGas', 'counterGas']
        payload_0 = {
                     'name':'powerBattery'
                     'unit_of_meas':'W'
                     'icon':'mdi:power'
                     'state_topic':'aurum',
           
           
           
{\"unit_of_measurement\":\"%\",
 \"icon\":\"mdi:water\",
 \"value_template\":\"{{ value_json.$i }}\",
 \"state_topic\":\"ink2mqtt/CanonMG5300\",
 \"json_attributes_topic\":\"ink2mqtt/CanonMG5300\",
 \"name\":\"Canon MG5300 $i Ink Level\",
 \"unique_id\":\"Canon MG5300 series_"$i"_ink2mqtt\",
 \"device\":
      {\"identifiers\":\"Canon MG5300 series\",
       \"name\":\"Canon MG5300 series\",
       \"sw_version\":\"2.030\",
       \"model\":\"MG5300 series\",
       \"manufacturer\":\"Canon\"
       }
 }    
                     
        try:
           url = 'http://{}/measurements/output.xml'.format(device)
           tree = ET.parse(ur.urlopen(url))
           root = tree.getroot()
        except Exception as exception:
           _LOGGER.error(
               "Unable to fetch data from AURUM. %s", exception)    
        else:
           for child in root:
               if(child is not None):
                   parameter = child.tag
                   payload = { EXAMPLE! NEEDS UPDATING!
                              "name":"Livingroom",
                              'unit_of_meas':'
                              "mode_cmd_t":"homeassistant/climate/livingroom/thermostatModeCmd",
                              "mode_stat_t":"homeassistant/climate/livingroom/state",
                              "mode_stat_tpl":"",
                              "avty_t":"homeassistant/climate/livingroom/available",
                              "pl_avail":"online",
                              "pl_not_avail":"offline",
                              "temp_cmd_t":"homeassistant/climate/livingroom/targetTempCmd",
                              "temp_stat_t":"homeassistant/climate/livingroom/state",
                              "temp_stat_tpl":"",
                              "curr_temp_t":"homeassistant/climate/livingroom/state",
                              "curr_temp_tpl":"",
                              "min_temp":"15",
                              "max_temp":"25",
                              "temp_step":"0.5",
                              "modes":["off", "heat"]
                             }
                   mqttc.publish('homeassistant/sensor/aurum/{}'.format(parameter)'/config', payload, qos=0, retain=True)
   
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
           for child in root:
               if(child is not None):
                   parameter = child.tag
                   value = child.get('value')
                   mqttc.publish('aurum/{}'.format(parameter), value, qos=0, retain=True)
                     
    async_init_aurum_data()
    async_track_time_interval(hass, async_get_aurum_data, scan_interval)

    return True
