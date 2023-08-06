"""MQTT Switch entity module."""
import json

from mqtt_hass_base.entity.common import MqttEntity
from mqtt_hass_base.error import MQTTHassBaseError

SWITCH_STATES = {
    "OFF": "OFF",
    "off": "OFF",
    0: "OFF",
    "0": "OFF",
    None: "OFF",
    "ON": "ON",
    "on": "ON",
    1: "ON",
    "1": "ON",
}


class MqttSwitch(MqttEntity):
    """MQTT Switch entity class."""

    _component = "switch"

    def __init__(
        self,
        name,
        mqtt_root_topic: str,
        logger,
        device_payload,
        subscriptions,
        icon: str,
        optimistic: bool,
    ):
        """Create a new MQTT sensor entity object."""
        MqttEntity.__init__(
            self, name, mqtt_root_topic, logger, device_payload, subscriptions
        )
        self._icon = icon
        self._optimistic = optimistic

    def register(self):
        """Register the current entity to Hass.

        Using the MQTT discovery feature of Home Assistant.
        """
        config_payload = {
            "availability": {
                "payload_available": "online",
                "payload_not_available": "offline",
                "topic": self.availability_topic,  # required
            },
            "command_topic": self.command_topic,
            "device": self.device_payload,
            "icon": self._icon,
            # "json_attributes_template": "",
            "json_attributes_topic": self.json_attributes_topic,
            "name": self.name,
            "optimistic": self._optimistic,
            "payload_off": "OFF",
            "payload_on": "ON",
            "qos": 0,
            "retain": False,
            "state_topic": self.state_topic,
        }

        if self._unique_id:
            config_payload["unique_id"] = self._unique_id

        self.logger.debug("%s: %s", self.config_topic, json.dumps(config_payload))
        self._mqtt_client.publish(
            topic=self.config_topic, retain=True, payload=json.dumps(config_payload)
        )

    def send_state(self, state, attributes=None):
        """Send the current state of the switch to Home Assistant."""
        if state not in SWITCH_STATES:
            msg = "Bad switch state {} . Should be in {}".format(state, SWITCH_STATES)
            self.logger.error(msg)
            raise MQTTHassBaseError(msg)
        payload = SWITCH_STATES.get(state)
        self._mqtt_client.publish(topic=self.state_topic, retain=True, payload=payload)

    def send_on(self, attributes=None):
        """Send the ON state of the switch to Home Assistant."""
        self.send_state("ON", attributes=attributes)

    def send_off(self, attributes=None):
        """Send the OFF state of the switch to Home Assistant."""
        self.send_state("OFF", attributes=attributes)
