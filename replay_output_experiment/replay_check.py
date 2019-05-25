from collections import defaultdict
from typing import Text

import faust

from simple_settings import settings
from logging.config import dictConfig
from datetime import datetime
from replay_output_experiment.page_views.models import DATETIME_BASIC_FORMAT, BalanceUpdate, RequestTransfer, \
    balances_str


# Run with
# docker-compose exec -e SIMPLE_SETTINGS=replay_output_experiment.settings replay_output_experiment bash -c "cd /repo_root && faust -A replay_output_experiment.replay_check worker --web-port 8000"


app = faust.App(
    version=1,  # fmt: off
    autodiscover=False,
    origin="replay_output_experiment",
    id=f'app-{datetime.utcnow().strftime(DATETIME_BASIC_FORMAT)}',
    #id="1",
    broker=settings.KAFKA_BOOTSTRAP_SERVER,
    logging_config=dictConfig(settings.LOGGING),
)

balances_topic = app.topic(settings.BALANCES_TOPIC, key_type=Text, value_type=BalanceUpdate)
transfers_topic = app.topic(settings.TRANSFERS_TOPIC, key_type=Text, value_type=RequestTransfer)


@app.agent(balances_topic)
async def process_balances(balances_stream):
    local_balances = defaultdict(int)
    async for balance in balances_stream:
        local_balances[balance.account] = balance.quantity
        #print(f'Balance update sum of all balances: {sum(local_balances.values())}')
        print(f'Balance update of {balance.account} at {balance.timestamp_committed}: ' +
              balances_str(local_balances))


@app.agent(transfers_topic)
async def process_transfers(transfers_stream):
    local_balances = defaultdict(int)
    async for transfer in transfers_stream:
        local_balances[transfer.src_account] -= transfer.quantity
        local_balances[transfer.dst_account] += transfer.quantity
        #print(f'transfer sum of all balances: {sum(local_balances.values())}')
        print(f'Transfer {transfer}: ' + balances_str(local_balances))


if __name__ == '__main__':
    app.main()
