import collections
import logging
import random
from datetime import datetime
from typing import Iterable, Text, Dict, Any

import attr
import faust

from replay_output_experiment.app import app

from replay_output_experiment.page_views.models import BalanceUpdate, RequestTransfer, DATETIME_BASIC_FORMAT, \
    balances_str
from simple_settings import settings
import asyncio
from faust.types import EventT

logger = logging.getLogger(__name__)


ACCOUNTS = ['a', 'b', 'c', 'd', 'e']

def random_requests(count=1) -> Iterable[RequestTransfer]:
    while count > 0:
        src = random.choice(ACCOUNTS)
        dst = random.choice([a for a in ACCOUNTS if a != src])
        yield RequestTransfer(src, dst, random.randint(1, 10))
        count -= 1


transfers_topic = app.topic(settings.TRANSFERS_TOPIC, key_type=Text, value_type=RequestTransfer, partitions=1)
balances_topic = app.topic(settings.BALANCES_TOPIC, key_type=Text, value_type=BalanceUpdate,
                           # retention=,  # With compaction are old messages also dropped after retention has passed?
                           compacting=True, partitions=1)

# Copied from tables/manager.py
replay_queue = app.FlowControlQueue(
    maxsize=app.conf.stream_buffer_maxsize,
    loop=asyncio.get_event_loop(),
    clear_on_resume=False,
)
replay_channel = balances_topic.clone_using_queue(replay_queue)


class MyTable(faust.Table):
    def update_balance(self, account: Text, quantity_delta: int, timestamp: Text) -> None:
        key = f'balance/{account}'
        if key in self:
            new_balance = self[key].quantity + quantity_delta
        else:
            new_balance = quantity_delta
        self[key] = BalanceUpdate(account=account, quantity=new_balance, timestamp_committed=timestamp)

    #
    # Overrides methods in tables/base.py:Collection
    def _to_key(self, k: Any) -> Any:
        print(f'Reading key {repr(k)} of type {type(k)}')
        if isinstance(k, list):
            assert False, 'Unexpected'
        return k

    def _to_value(self, v: Any) -> Any:
        return v


balances_table = MyTable(app=app, name='balances', default=None, partitions=1, changelog_topic=balances_topic,
                         key_type=Text, value_type=BalanceUpdate)

app.tables.add(balances_table)


#@app.task()
#async def do_replay():
#    print('seeking on replay channel')
#    app.consumer.seek_wait({replay_channel.active_partitions, 0})
#    print('Seek returned')
#    async for event in replay_channel:
##        event: EventT = await replay_queue.get()
#        message = event.message
#        print(f'Topic {message.topic} Offset {message.offset} {message.key}: {message.value}')


@attr.s(auto_attribs=True, slots=True)
class Executor:
    async def execute_transfer(self, transfer: RequestTransfer):
        timestamp_now = datetime.utcnow().isoformat()
        balances_table.update_balance(
            account=transfer.src_account,
            quantity_delta=-transfer.quantity,
            timestamp=timestamp_now)
        balances_table.update_balance(
            account=transfer.dst_account,
            quantity_delta=transfer.quantity,
            timestamp=timestamp_now)

        print(f'Transfer of {transfer.quantity} from {transfer.src_account} to {transfer.dst_account} at {timestamp_now}')
        print('Balance table: ' + balances_str(balances_table))
        print(f'Transfer at {timestamp_now} finished.')

exec = Executor()




@app.timer(10)
async def producer():
    for rand_req in random_requests():
        await transfers_topic.send(key=datetime.utcnow().strftime(DATETIME_BASIC_FORMAT), value=rand_req)


@app.agent(transfers_topic)
async def process_transfers(transfers):
    async for transfer in transfers:
        await exec.execute_transfer(transfer)



