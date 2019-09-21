"""Xiaomi aqara double key switch device."""
import logging

from zigpy.profiles import zha
from zigpy.zcl.clusters.general import (
    AnalogInput,
    Basic,
    Groups,
    Identify,
    MultistateInput,
    Ota,
    Scenes,
)

from .. import LUMI, BasicCluster, PowerConfigurationCluster, XiaomiCustomDevice
from ... import CustomCluster
from ...const import (
    ATTR_ID,
    BUTTON,
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
    VALUE,
    ZHA_SEND_EVENT,
)

ENDPOINT_MAP = {1: "left", 2: "right", 3: "both"}
PRESS_TYPE = {0: "long press", 1: "single", 2: "double"}
STATUS_TYPE_ATTR = 0x0055  # decimal = 85
XIAOMI_CLUSTER_ID = 0xFFFF
XIAOMI_DEVICE_TYPE = 0x5F01
XIAOMI_DEVICE_TYPE2 = 0x5F02
XIAOMI_DEVICE_TYPE3 = 0x5F03

_LOGGER = logging.getLogger(__name__)


class RemoteB286ACN01(XiaomiCustomDevice):
    """Aqara double key switch device."""

    class MultistateInputCluster(CustomCluster, MultistateInput):
        """Multistate input cluster."""

        cluster_id = MultistateInput.cluster_id

        def __init__(self, *args, **kwargs):
            """Init."""
            self._current_state = None
            super().__init__(*args, **kwargs)

        def _update_attribute(self, attrid, value):
            super()._update_attribute(attrid, value)
            if attrid == STATUS_TYPE_ATTR:
                self._current_state = PRESS_TYPE.get(value)
                button = ENDPOINT_MAP.get(self.endpoint.endpoint_id)
                event_args = {
                    BUTTON: button,
                    PRESS_TYPE: self._current_state,
                    ATTR_ID: attrid,
                    VALUE: value,
                }
                action = "{}_{}".format(button, self._current_state)
                self.listener_event(ZHA_SEND_EVENT, self, action, event_args)
                # show something in the sensor in HA
                super()._update_attribute(0, action)

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=24321
        # device_version=1
        # input_clusters=[0, 3, 25, 65535, 18]
        # output_clusters=[0, 4, 3, 5, 25, 65535, 18]>
        MODELS_INFO: [(LUMI, "lumi.remote.b286acn01"), (LUMI, "lumi.sensor_86sw2")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: XIAOMI_DEVICE_TYPE,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Ota.cluster_id,
                    XIAOMI_CLUSTER_ID,
                    MultistateInputCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Ota.cluster_id,
                    XIAOMI_CLUSTER_ID,
                    MultistateInputCluster.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=2 profile=260 device_type=24322
            # device_version=1
            # input_clusters=[3, 18]
            # output_clusters=[4, 3, 5, 18]>
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: XIAOMI_DEVICE_TYPE2,
                INPUT_CLUSTERS: [
                    Identify.cluster_id,
                    MultistateInputCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    MultistateInputCluster.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=3 profile=260 device_type=24323
            # device_version=1
            # input_clusters=[3, 12]
            # output_clusters=[4, 3, 5, 12]>
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: XIAOMI_DEVICE_TYPE3,
                INPUT_CLUSTERS: [Identify.cluster_id, AnalogInput.cluster_id],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    AnalogInput.cluster_id,
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                DEVICE_TYPE: XIAOMI_DEVICE_TYPE,
                INPUT_CLUSTERS: [
                    BasicCluster,
                    PowerConfigurationCluster,
                    Identify.cluster_id,
                    Ota.cluster_id,
                    XIAOMI_CLUSTER_ID,
                    MultistateInputCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Ota.cluster_id,
                    XIAOMI_CLUSTER_ID,
                    MultistateInputCluster,
                ],
            },
            2: {
                DEVICE_TYPE: XIAOMI_DEVICE_TYPE2,
                INPUT_CLUSTERS: [Identify.cluster_id, MultistateInputCluster],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    MultistateInputCluster,
                ],
            },
            3: {
                DEVICE_TYPE: XIAOMI_DEVICE_TYPE3,
                INPUT_CLUSTERS: [Identify.cluster_id, MultistateInputCluster],
                OUTPUT_CLUSTERS: [
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    AnalogInput.cluster_id,
                    MultistateInputCluster,
                ],
            },
        }
    }