"""MQTT Sensor entity module."""
import json

from mqtt_hass_base.const import DEVICE_CLASSES
from mqtt_hass_base.entity.common import MqttEntity
from mqtt_hass_base.error import MQTTHassBaseError


class MqttSensor(MqttEntity):
    """MQTT Sensor entity class."""

    _component = "sensor"

    def __init__(
        self,
        name,
        mqtt_root_topic: str,
        logger,
        device_payload,
        subscriptions,
        device_class=None,
        expire_after=0,
        force_update=False,
        icon="",
        unit="",
    ):
        """Create a new MQTT sensor entity object."""
        MqttEntity.__init__(self, name, mqtt_root_topic, logger, device_payload)
        self._device_class = device_class
        if device_class not in DEVICE_CLASSES:
            msg = "Bad device class {}. Should be in {}".format(
                device_class, DEVICE_CLASSES
            )
            self.logger.error(msg)
            raise MQTTHassBaseError(msg)
        self._expire_after = expire_after
        self._force_update = force_update
        self._icon = icon
        self._unit = unit

    def register(self):
        """Register the current entity to Home Assistant.

        Using the MQTT discovery feature of Home Assistant.
        """
        config_payload = {
            "availability_topic": self.availability_topic,
            "device": self.device_payload,
            "expire_after": self._expire_after,
            "force_update": self._force_update,
            # "json_attributes_template": "",
            "json_attributes_topic": self.json_attributes_topic,
            "name": self.name,
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 0,
            "state_topic": self.state_topic,
        }
        if self._device_class:
            config_payload["device_class"] = self._device_class
        if self._icon:
            config_payload["icon"] = self._icon
        if self._unit:
            config_payload["unit_of_measurement"] = self._unit
        if self._unique_id:
            config_payload["unique_id"] = self._unique_id

        self.logger.debug("%s: %s", self.config_topic, json.dumps(config_payload))
        self._mqtt_client.publish(
            topic=self.config_topic, retain=True, payload=json.dumps(config_payload)
        )

    def send_state(self, state, attributes=None):
        """Send the current state of the sensor to Home Assistant."""
        if isinstance(state, (bytes, str)):
            state = state[:255]
        self._mqtt_client.publish(topic=self.state_topic, retain=True, payload=state)
        if attributes is not None:
            self.send_attributes(attributes)
