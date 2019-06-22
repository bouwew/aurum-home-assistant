"""
Support for power production statistics from the AURUM Meetstekker web-page.

For more details about this platform, please refer to the documentation at
https://github.com/bouwew/aurum-home-assistant/

Configuration (example):

aurum:
   device: 192.168.0.110      # ip adress of the meetstekker
   broker: 192.168.0.111      # ip adress of the MQTT broker
   password: mqtt_password    # MQTT broker password
   username: mqtt_user        # MQTT username
   client: aurum              # MQTT client-id, optional, default set to 'aurum'
   scan_interval: 20          # reporting interval, optional, default 60 seconds (note: the Dutch Smart Meter refreshes every 10 seoconds)
"""
import logging
import voluptuous as vol
import urllib.request as ur
import xml.etree.ElementTree as ET
import homeassistant.helpers.config_validation as cv
import paho.mqtt.client as mqtt

from homeassistant.const import (
    CONF_DEVICE, CONF_PASSWORD, CONF_USERNAME, 
    CONF_SCAN_INTERVAL, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

__version__ = '0.1.6'

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'aurum'

CONF_BROKER = 'broker'
CONF_CLIENT = 'client'
DEFAULT_CL = 'aurum'
SCAN_INTERVAL = timedelta(seconds=60)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEVICE): cv.string,
        vol.Required(CONF_BROKER): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
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
    client = conf.get(CONF_CLIENT)
    scan_interval = conf.get(CONF_SCAN_INTERVAL)

    client_id = client
    port = 1883
    keepalive = 300

    mqttc = mqtt.Client(client_id, protocol=mqtt.MQTTv311)
    mqttc.username_pw_set(username, password=password)
    mqttc.connect(broker, port=port, keepalive=keepalive)

    async def async_stop_aurum(event):
        """Stop the Aurum MQTT component."""
        mqttc.disconnect()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, async_stop_aurum)

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
                   mqttc.publish('homeassistant/sensor/aurum/{}'.format(parameter), value, qos=0, retain=True)

    async_track_time_interval(hass, async_get_aurum_data, scan_interval)

    return True
