Support for power production statistics from the AURUM Meetstekker web-page.

Configuration (example):
aurum:
   device: 192.168.0.110      # ip adress of the meetstekker
   broker: 192.168.0.111      # ip adress of the MQTT broker
   password: mqtt_password   # MQTT broker password
   username: mqtt_user       # MQTT username
   scan_interval: 20         # reporting interval, default 60 seconds (note: the Dutch Smart Meter refreshes every 10 seoconds)
