import sys

import nats
from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.api import (
    StreamConfig,
    RetentionPolicy,
    StorageType,
    DiscardPolicy,
)


async def connect_to_nats(servers: str | list[str]) -> tuple[Client, JetStreamContext]:
    nc: Client = await nats.connect(servers=servers)
    js: JetStreamContext = nc.jetstream()

    stream_config = StreamConfig(
        name="CurrenciesStream",
        subjects=["currencies"],
        retention=RetentionPolicy.INTEREST,
        discard=DiscardPolicy.OLD,
        storage=StorageType.FILE,
        allow_rollup_hdrs=True,
    )

    await js.add_stream(stream_config)

    print("Successfully connect to NATS server!", file=sys.stderr)

    return nc, js