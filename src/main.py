import asyncio
from functools import partial
import json
import logging
import os
from typing import Optional
import websockets

from dataclasses import dataclass

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class HubitatElevationEvent:
    source: str
    name: str
    displayName: str
    value: float
    type: Optional[str]
    unit: str
    deviceId: int
    hubId: int
    installedAppId: int
    descriptionText: str

    def __post_init__(self):
        self.value = float(self.value)


hs_ws_url = os.environ["HUBITAT_ELEVATION_WEBSOCKET_URL"]
influxdb_url = os.environ["INFLUXDB_URL"]
token = os.environ["INFLUXDB_TOKEN"]
org = os.environ["INFLUXDB_ORG"]
bucket = os.environ["INFLUXDB_BUCKET"]

client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


async def write_event(record):
    return asyncio.get_running_loop().run_in_executor(
        None, partial(write_api.write, bucket, record=record)
    )


async def he_event():
    async with websockets.connect(hs_ws_url) as websocket:
        loop = asyncio.get_running_loop()

        async for message in websocket:
            try:
                event = HubitatElevationEvent(**json.loads(message))
                logger.info(
                    "%s (%s): %s"
                    % (event.displayName, event.deviceId, event.descriptionText)
                )
            except Exception as ex:
                logger.error("Failed parsing message from HE websocket: %s" % message)

            p = (
                Point("home")
                .tag("device", event.displayName)
                .field(event.name, event.value)
            )
            await write_event(p)


asyncio.run(he_event())
